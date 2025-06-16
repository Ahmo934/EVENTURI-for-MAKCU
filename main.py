import time
import numpy as np
import threading
from mouse import Mouse, button_states
from capture import get_frame, get_region, SCREEN_WIDTH, SCREEN_HEIGHT
from detection import detect_fake_full_body
import cv2
from config import config

_aimbot_running = False
_aimbot_thread = None
debug_windows_open = False
def adaptive_speed(dx, dy, min_speed=2, max_speed=24):
    distance = np.hypot(dx, dy)
    speed = int(min_speed + (max_speed - min_speed) * min(1.0, distance / 60))
    if distance == 0:
        return 0, 0
    step_dx = int(dx * speed / distance)
    step_dy = int(dy * speed / distance)
    return step_dx, step_dy

def aimbot_loop():
    global _aimbot_running
    mouse = Mouse()
    last_button_state = False
    last_shot_time = 0

    while _aimbot_running:
        frame = get_frame()
        if frame is None:
            continue

        target, mask, dbg = detect_fake_full_body(
            frame, 
            config.target_color, 
            body_height=config.body_height, 
            body_width=config.body_width, 
            debug=True
        )

        display = frame.copy()
        if target:
            cv2.drawMarker(display, target, (0,255,0), markerType=cv2.MARKER_CROSS, markerSize=16, thickness=2)
            cv2.circle(display, target, 8, (0,255,255), 2)
        if config.debug:
            cv2.imshow("Aimbot: Detection", display)
            cv2.imshow("Aimbot: Mask+Body", mask)
            debug_windows_open = True
        else:
            if debug_windows_open:
                cv2.destroyAllWindows()
                debug_windows_open = False
        if dbg:
            if 'original_mask' in dbg:
                cv2.imshow("Aimbot: Raw Mask", dbg['original_mask'])
            if 'closed_mask' in dbg:
                cv2.imshow("Aimbot: Closed Mask", dbg['closed_mask'])
            if 'body_mask' in dbg:
                cv2.imshow("Aimbot: Body Only", dbg['body_mask'])

        if cv2.waitKey(1) & 0xFF == 27:  
            _aimbot_running = False
            break


        current_time = time.time()
        button_index = config.mouse_button
        trigger_pressed = button_states[button_index] and not last_button_state

        if target and button_states[button_index]:
            screen_center_x = SCREEN_WIDTH // 2
            screen_center_y = SCREEN_HEIGHT // 2
            target_screen_x = get_region()[0] + target[0]
            target_screen_y = get_region()[1] + target[1] + config.aim_offset_y
            dx = target_screen_x - screen_center_x
            dy = target_screen_y - screen_center_y

            if config.mode == "normal":
                step_dx, step_dy = adaptive_speed(dx, dy, min_speed=config.normal_min_speed, max_speed=config.normal_max_speed)
                mouse.move(step_dx, step_dy)
            elif config.mode == "bezier":
                mouse.move_bezier(dx, dy, config.bezier_segments, config.bezier_ctrl_x, config.bezier_ctrl_y)
            elif config.mode == "silent" and trigger_pressed and (current_time - last_shot_time) > config.silent_cooldown:
                move_dx = int(dx * config.silent_speed)
                move_dy = int(dy * config.silent_speed)
                mouse.move_bezier(move_dx, move_dy, config.silent_segments, config.silent_ctrl_x, config.silent_ctrl_y)
                time.sleep(0.012)
                mouse.click()
                time.sleep(0.010)
                mouse.move_bezier(-move_dx, -move_dy, config.silent_segments, config.silent_ctrl_x, config.silent_ctrl_y)
                last_shot_time = current_time

        last_button_state = button_states[button_index]
        time.sleep(0.001)


def start_aimbot():
    global _aimbot_running, _aimbot_thread
    if not _aimbot_running:
        _aimbot_running = True
        _aimbot_thread = threading.Thread(target=aimbot_loop, daemon=True)
        _aimbot_thread.start()

def stop_aimbot():
    global _aimbot_running, _aimbot_thread
    _aimbot_running = False
    _aimbot_thread = False

