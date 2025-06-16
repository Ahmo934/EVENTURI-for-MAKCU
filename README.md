# EVENTURI-for-MAKCU

**EVENTURI for MAKCU** is a modern, highly-configurable colorbot aimbot, designed for low-latency hardware-based mouse control (MAKCU device). It provides advanced color detection, adjustable region-of-interest, ultra-smooth aiming, and a beautiful, easy-to-use GUI.


## 🚀 Features

- **Super Fast DXCAM Capture:** Up to 200+ FPS screen region capture using dxcam.
- **Hardware Mouse Movement:** Full support for MAKCU device (up to 4M baud rate).
- **Flexible Detection:** HSV color-based detection.
- **Mode Toggle:** Instantly switch between Normal, Bezier, and Silent aim modes.
- **Live Config:** All parameters (colors, speeds, FOV, mouse buttons, offsets) are tweakable in the GUI and take effect instantly.
- **Profile Support:** Save/load unlimited configs, reset to defaults, quick toggle.

---

## ⚡️ Quick Start

1. ```bash
   git clone https://github.com/Ahmo934/EVENTURI-for-MAKCU.git
    cd eventuri-makcu

2. **Requirements:**
   - Windows 10/11 (only, no Linux support yet)
   - Python 3.9+ (Recommended: 3.11+)
   - MAKCU device with USB connection
   - Dependencies:
     - `opencv-python`
     - `numpy`
     - `dxcam`
     - `customtkinter`
     - `pyserial`

   Install with:
   ```bash
   pip install -r requirements.txt

   3. ```bash
       python gui.py

 **Note:**

 - To customize the colors your aimbot will detect, simply edit the HSV ranges in config.py.
   Find the section that looks like this:
   ```python
      "color_ranges": {
        "purple": {"lower": [140, 60, 100], "upper": [160, 255, 255]},
        "yellow": {"lower": [30, 125, 150], "upper": [35, 255, 255]},
    }
   
  and change to your desire color range.


- **Credits**
  Special thanks to everyone in the MAKCU community.

- **How it Works**
  - Detection: Uses HSV masking and fake-body filling for extremely robust target acquisition (works even on difficult backgrounds).

  - Aiming: Moves the mouse using the MAKCU device, supporting normal, bezier, and silent modes.

  - Config: All settings update live through the GUI; save/load presets instantly.

  - Debug: Real-time OpenCV preview (can be toggled on/off from GUI).

 **TODO:**
 - Add hsv color picker.

 - Fix Debug window.

 - Start/Stop Aimbot not working properly.
