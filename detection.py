import cv2
import numpy as np
from config import config, DEFAULT_CONFIG
COLOR_RANGES = config.color_ranges

def mask_frame(frame, color):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower = np.array(COLOR_RANGES[color]['lower'], dtype=np.uint8)
    upper = np.array(COLOR_RANGES[color]['upper'], dtype=np.uint8)
    mask = cv2.inRange(hsv, lower, upper)
    mask = cv2.erode(mask, None, iterations=1)
    mask = cv2.dilate(mask, None, iterations=10)
    return mask

def detect_fake_full_body(
    frame, color='purple', body_height=48, body_width=22, min_width=8, max_width_ratio=0.45, debug=False
):
    mask = mask_frame(frame, color)
    h, w = mask.shape
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3,3))
    closed = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

    for y in range(h):
        xs = np.where(closed[y] > 0)[0]
        width = xs[-1] - xs[0] if len(xs) > 1 else 1
        if len(xs) > 0 and min_width <= width <= (w * max_width_ratio):
            x = int(np.mean(xs))
            full_body_mask = np.zeros_like(mask)
            cv2.ellipse(
                full_body_mask,
                (x, y + body_height // 2),
                (body_width, body_height // 2),
                0, 0, 360, 255, -1
            )
            full_body_mask[y, xs] = 255  

            aim_y = y + body_height // 2
            target = (x, aim_y)

            debug_images = None
            if debug:
                debug_images = {
                    "mask": mask,
                    "closed": closed,
                    "full_body_mask": full_body_mask
                }
            return target, full_body_mask, debug_images

    return None, mask, None

