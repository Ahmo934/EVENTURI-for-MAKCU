import dxcam
import tkinter as tk

def get_screen_size():
    root = tk.Tk()
    root.withdraw()
    w, h = root.winfo_screenwidth(), root.winfo_screenheight()
    root.destroy()
    return w, h
SCREEN_WIDTH, SCREEN_HEIGHT = get_screen_size()
BOX_SIZE = 100  

def get_region():
    return (
        SCREEN_WIDTH // 2 - BOX_SIZE // 2,
        SCREEN_HEIGHT // 2 - BOX_SIZE // 2,
        SCREEN_WIDTH // 2 + BOX_SIZE // 2,
        SCREEN_HEIGHT // 2 + BOX_SIZE // 2
    )

camera = dxcam.create(output_color="BGR")

def get_frame():
    return camera.grab(region=get_region())
