import json
import os

DEFAULT_CONFIG = {
    "makcu_connected": False,
    "target_color": "purple",
    "box_size": 100,
    "color_ranges": {
        "purple": {"lower": [140, 60, 100], "upper": [160, 255, 255]},
        "yellow": {"lower": [30, 125, 150], "upper": [35, 255, 255]},
    },
    "aim_offset_y": 0,
    "mode": "bezier",  # "normal", "bezier", "silent"
    "mouse_button": 3,  # 0-4
    "body_height" : 30,
    "body_width" : 15,
    "debug": True,
    # Normal Move
    "normal_min_speed": 4,
    "normal_max_speed": 100,
    # Bezier Move
    "bezier_segments": 5,
    "bezier_ctrl_x": 20,
    "bezier_ctrl_y": 20,
    # Silent Aim
    "silent_segments": 5,
    "silent_ctrl_x": 20,
    "silent_ctrl_y": 20,
    "silent_speed": 5,
    "silent_cooldown": 0.18,
}

CONFIG_FILE = "aimbot_profile.json"

class Config:
    def __init__(self):
        self.reset_to_defaults()
    def reset_to_defaults(self):
        for k, v in DEFAULT_CONFIG.items():
            setattr(self, k, v if not isinstance(v, dict) else v.copy())
    def save(self, path=CONFIG_FILE):
        d = self.__dict__.copy()
        with open(path, "w") as f:
            json.dump(d, f, indent=2)
    def load(self, path=CONFIG_FILE):
        if not os.path.exists(path):
            return
        with open(path, "r") as f:
            d = json.load(f)
        for k in DEFAULT_CONFIG:
            if k in d:
                setattr(self, k, d[k])
    def as_dict(self):
        return self.__dict__.copy()

config = Config()
