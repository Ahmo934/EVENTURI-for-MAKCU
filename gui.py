import customtkinter as ctk
import tkinter as tk
from config import config, DEFAULT_CONFIG
from tkinter import messagebox
from functools import partial
import main
from mouse import test_move, connect_to_makcu
import capture
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")


class EventuriGUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("EVENTURI for MAKCU")
        self.geometry("560x680")
        self.resizable(False, False)

        self._building = True
        self.build_ui()
        self._building = False
        self.refresh_fields()
    def build_ui(self):
        # Title and Status
        ctk.CTkLabel(self, text="EVENTURI for MAKCU", font=("Segoe UI Bold", 24)).pack(pady=(15, 2))
        self.status_label = ctk.CTkLabel(self, text="Disconnected", text_color="#ff1414", font=("Segoe UI", 12))
        self.status_label.pack(pady=(0, 8))

        # Makcu Controls
        makcu_frame = ctk.CTkFrame(self)
        makcu_frame.pack(pady=4, padx=10, fill="x")
        self.connect_btn = ctk.CTkButton(makcu_frame, text="Connect to MAKCU", command=self.on_connect)
        self.connect_btn.pack(side="left", padx=8, pady=7)
        self.test_btn = ctk.CTkButton(makcu_frame, text="Test Move Mouse", command=self.on_test_move)
        self.test_btn.pack(side="left", padx=8)

        # Main Config
        config_frame = ctk.CTkFrame(self)
        config_frame.pack(pady=10, padx=10, fill="x")
        ctk.CTkLabel(config_frame, text="Target Color:").grid(row=0, column=0, sticky="w")
        self.color_menu = ctk.CTkOptionMenu(config_frame, values=["purple", "yellow"], command=self.update_color)
        self.color_menu.grid(row=0, column=1, padx=5, pady=4)
        ctk.CTkLabel(config_frame, text="FOV :").grid(row=1, column=0, sticky="w")
        self.box_slider = ctk.CTkSlider(config_frame, from_=50, to=200, command=self.update_box_size)
        self.box_slider.grid(row=1, column=1, padx=5)
        self.debug_btn = ctk.CTkButton(config_frame, text="Hide Debug", command=self.show_debug_window)
        self.debug_btn.grid(row=1, column=2, padx=5)
        ctk.CTkButton(config_frame, text="Edit Color Range", command=self.edit_color_range).grid(row=0, column=2, padx=5)
        ctk.CTkLabel(config_frame, text="Aim Offset Y:").grid(row=2, column=0, sticky="w")
        self.offset_spin = ctk.CTkSlider(config_frame, from_=35, to=-35, number_of_steps=69, command=self.update_offset)
        self.offset_spin.grid(row=2, column=1, padx=5)

        # --- Mode Tabs ---
        self.mode_var = tk.StringVar(value=config.mode)
        mode_frame = ctk.CTkFrame(self)
        mode_frame.pack(padx=10, pady=8, fill="x")
        ctk.CTkLabel(mode_frame, text="Aimbot Mode:").pack(anchor="w")
        mode_row = ctk.CTkFrame(mode_frame)
        mode_row.pack()
        for name, val in [("Normal", "normal"), ("Bezier", "bezier"), ("Silent Aim", "silent")]:
            ctk.CTkRadioButton(mode_row, text=name, variable=self.mode_var, value=val, command=self.update_mode).pack(side="left", padx=8)
        
        # --- Dynamic Settings ---
        self.dynamic_section = ctk.CTkFrame(self)
        self.dynamic_section.pack(fill="both", expand=True, padx=10, pady=(4, 0))

        # --- Profile Buttons ---
        profile_row = ctk.CTkFrame(self)
        profile_row.pack(pady=8, padx=10, fill="x")
        ctk.CTkButton(profile_row, text="Save Profile", command=self.save_profile).pack(side="left", padx=5)
        ctk.CTkButton(profile_row, text="Load Profile", command=self.load_profile).pack(side="left", padx=5)
        ctk.CTkButton(profile_row, text="Reset to Defaults", command=self.reset_defaults).pack(side="left", padx=5)
        ctk.CTkButton(profile_row, text="Disable All", fg_color="#333", command=self.disable_all).pack(side="right", padx=5)
        aimbot_row = ctk.CTkFrame(self)
        aimbot_row.pack(pady=(0, 10), padx=10, fill="x")
        self.start_btn = ctk.CTkButton(aimbot_row, text="Start Aimbot", command=self.on_start_aimbot)
        self.start_btn.pack(side="left", padx=8)
        self.stop_btn = ctk.CTkButton(aimbot_row, text="Stop Aimbot", fg_color="#333", command=self.on_stop_aimbot)
        self.stop_btn.pack(side="left", padx=8)
        # Footer
        ctk.CTkLabel(self, text="Made with      ❤️ by Ahmo934 for Makcu Community", text_color="#39ff14", font=("Segoe UI", 13)).pack(side="bottom", pady=(0, 5))

        self.update_dynamic_section()  # Build dynamic section initially

    def on_connect(self):
        self.status_label.configure(text="Connected!", text_color="#39ff14")
        """if connect_to_makcu():
            config.makcu_connected = True
        else:
            config.makcu_connected = False"""
        

    def on_test_move(self):
        test_move()

    # --- Config Handlers ---
    def on_start_aimbot(self):
        main.start_aimbot()
        self.status_label.configure(text="Aimbot Running", text_color="#39ff14")
    def on_stop_aimbot(self):
        main.stop_aimbot()
        self.status_label.configure(text="Aimbot Stopped", text_color="#FF0000")
    def update_color(self, val):
        config.target_color = val
    def update_box_size(self, val):
        capture.BOX_SIZE = int (round(val))
        config.box_size = int(round(val))
    def update_offset(self, val):
        config.aim_offset_y = int(round(val))
    def update_mode(self):
        config.mode = self.mode_var.get()
        self.update_dynamic_section()
    def save_profile(self):
        config.save()
        messagebox.showinfo("Profile Saved", "Config saved!")
    def load_profile(self):
        config.load()
        self.refresh_fields()
    def reset_defaults(self):
        config.reset_to_defaults()
        self.refresh_fields()
    def disable_all(self):
        config.normal_move = False
        config.bezier_move = False
        config.silent_aim = False
        self.refresh_fields()
        self.status_label.configure(text="Aimbot Disabled", text_color="#FF0000")
    def edit_color_range(self):
        messagebox.showinfo("Advanced", "Color Range Editor coming soon!")
    def show_debug_window(self):
       messagebox.showinfo("TODO", "Not working Currently " \
       "Minimize Debug window manually.") 



    # --- Dynamic Settings (Mode-specific) ---
    def update_dynamic_section(self):
        for widget in self.dynamic_section.winfo_children():
            widget.destroy()
        mode = config.mode
        # Mouse Button Select
        ctk.CTkLabel(self.dynamic_section, text="Aimbot Mouse Button:").pack(anchor="w")
        btnrow = ctk.CTkFrame(self.dynamic_section)
        btnrow.pack(anchor="w", pady=4)
        if not hasattr(self, 'mouse_btn_var'):
            self.mouse_btn_var = tk.IntVar(value=config.mouse_button)
        else:
            self.mouse_btn_var.set(config.mouse_button)

        def mouse_btn_update():
            config.mouse_button = self.mouse_btn_var.get()

        for i, name in enumerate(["Left", "Right", "Middle", "Side 4", "Side 5"]):
            b = ctk.CTkRadioButton(
                btnrow,
                text=name,
                variable=self.mouse_btn_var,
                value=i,
                command=mouse_btn_update
            )
            b.pack(side="left", padx=5)
                # Mode-specific fields
        if mode == "normal":
            self.add_speed_section("Normal", "normal_min_speed", "normal_max_speed")
        elif mode == "bezier":
            self.add_bezier_section("bezier_segments", "bezier_ctrl_x", "bezier_ctrl_y")
        elif mode == "silent":
            self.add_bezier_section("silent_segments", "silent_ctrl_x", "silent_ctrl_y")
            self.add_silent_section()
    def add_speed_section(self, label, min_key, max_key):
        f = ctk.CTkFrame(self.dynamic_section)
        f.pack(fill="x", pady=4)
        ctk.CTkLabel(f, text=f"{label} Min Speed:").grid(row=0, column=0, sticky="w")
        smin = ctk.CTkSlider(f, from_=2, to=8, number_of_steps=6, command=lambda v: setattr(config, min_key, int(float(v))))
        smin.set(getattr(config, min_key))
        smin.grid(row=0, column=1)
        ctk.CTkLabel(f, text=f"{label} Max Speed:").grid(row=1, column=0, sticky="w")
        smax = ctk.CTkSlider(f, from_=16, to=120, number_of_steps=52, command=lambda v: setattr(config, max_key, int(float(v))))
        smax.set(getattr(config, max_key))
        smax.grid(row=1, column=1)
    def add_bezier_section(self, seg_key, cx_key, cy_key):
        f = ctk.CTkFrame(self.dynamic_section)
        f.pack(fill="x", pady=4)
        ctk.CTkLabel(f, text="Bezier Segments:").grid(row=0, column=0)
        sseg = ctk.CTkSlider(f, from_=0, to=20, number_of_steps=20, command=lambda v: setattr(config, seg_key, int(float(v))))
        sseg.set(getattr(config, seg_key))
        sseg.grid(row=0, column=1)
        ctk.CTkLabel(f, text="Ctrl X:").grid(row=1, column=0)
        scx = ctk.CTkSlider(f, from_=0, to=60, number_of_steps=60, command=lambda v: setattr(config, cx_key, int(float(v))))
        scx.set(getattr(config, cx_key))
        scx.grid(row=1, column=1)
        ctk.CTkLabel(f, text="Ctrl Y:").grid(row=2, column=0)
        scy = ctk.CTkSlider(f, from_=0, to=60, number_of_steps=60, command=lambda v: setattr(config, cy_key, int(float(v))))
        scy.set(getattr(config, cy_key))
        scy.grid(row=2, column=1)
    def add_silent_section(self):
        f = ctk.CTkFrame(self.dynamic_section)
        f.pack(fill="x", pady=4)
        ctk.CTkLabel(f, text="Silent Aim Speed:").grid(row=0, column=0)
        sspd = ctk.CTkSlider(f, from_=1, to=6, number_of_steps=5, command=lambda v: setattr(config, "silent_speed", int(float(v))))
        sspd.set(config.silent_speed)
        sspd.grid(row=0, column=1)
        ctk.CTkLabel(f, text="Cooldown:").grid(row=1, column=0)
        scd = ctk.CTkSlider(f, from_=0.00, to=0.5, number_of_steps=50, command=lambda v: setattr(config, "silent_cooldown", float(v)))
        scd.set(config.silent_cooldown)
        scd.grid(row=1, column=1)

    # --- Utility ---
    def refresh_fields(self):
        self._building = True
        self.color_menu.set(config.target_color)
        self.box_slider.set(config.box_size)
        self.offset_spin.set(config.aim_offset_y)
        self.mode_var.set(config.mode)
        self.update_dynamic_section()
        self._building = False

if __name__ == "__main__":
    app = EventuriGUI()
    app.mainloop()
