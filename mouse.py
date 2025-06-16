import threading
import serial
from serial.tools import list_ports
import time
# === Globals ===
makcu = None
makcu_lock = threading.Lock()
button_states = {i: False for i in range(5)}
is_connected = False
last_value = 0
baud_change_command = bytearray([0xDE, 0xAD, 0x05, 0x00, 0xA5, 0x00, 0x09, 0x3D, 0x00])

# === Serial Setup ===
def find_com_port():
    for port in list_ports.comports():
        if "VID:PID=1A86:55D3" in port.hwid.upper():
            return port.device
    print("[ERROR] MAKCU not found in available COM ports.")
    return None

def connect_to_makcu():
    global makcu, is_connected
    port = find_com_port()
    if not port:
        return False

    try:
        makcu = serial.Serial(port, 115200, timeout=0.1)
        time.sleep(1)
        makcu.write(baud_change_command)
        makcu.close()
        print("[INFO] Makcu initialized with 4 Million baud rate.")
        makcu = serial.Serial(port, 4000000, timeout=0.1)
        makcu.baudrate = 4000000

        with makcu_lock:
            makcu.write(b"km.buttons(1)\r")
            makcu.flush()

        is_connected = True
        return True

    except serial.SerialException as e:
        print(f"[ERROR] Failed to connect to MAKCU: {e}")
        return False

def count_bits(n: int) -> int:
    return bin(n).count("1")

def listen_makcu():
    global last_value, button_states
    while is_connected:
        try:
            if makcu.in_waiting > 0:
                byte = makcu.read(1)
                if not byte:
                    continue
                value = byte[0]

                if value > 31 or (value != 0 and count_bits(value) != 1):
                    continue

                newly_pressed = (value ^ last_value) & value
                newly_released = (value ^ last_value) & last_value

                for i in range(5):
                    if newly_pressed == (1 << i):
                        button_states[i] = True
                    elif newly_released == (1 << i):
                        button_states[i] = False

                last_value = value

        except serial.SerialException as e:
            print(f"[ERROR] SerialException in listener thread: {e}")
            break
def send_move_command(dx: int, dy: int):
    if not is_connected:
        return

    with makcu_lock:
        command = f"km.move({dx},{dy}\r)"
        makcu.write(command.encode())
        makcu.flush()

def send_move_command_bezeir(dx: int, dy: int, segments: int, ctrl_x: int, ctrl_y: int):
    if not is_connected:
        return

    with makcu_lock:
        command = f"km.move({dx},{dy},{segments},{ctrl_x},{ctrl_y}\r)"
        if dx <= 1 and dy <= 1:
            command = f"km.move({dx},{dy}\r)"

        makcu.write(command.encode())
        makcu.flush()

def send_click_command():
    if not is_connected:
        return

    with makcu_lock:
        makcu.write(b"km.left(1)\r km.left(0)\r")
        makcu.flush()

def test_move():
    if not is_connected:
        return
    
    with makcu_lock:
        makcu.write(b"km.move(20,20)\r")
        makcu.flush()

class Mouse:
    def __init__(self):
        if not connect_to_makcu():
            print("[ERROR] Could not connect to MAKCU.")
        else:
            listener_thread = threading.Thread(target=listen_makcu, daemon=True)
            listener_thread.start()

    def move(self, x: float, y: float):
        send_move_command(int(x), int(y))

    def move_bezier(self, x: float, y: float, segments: int = 10, ctrl_x: float = 0, ctrl_y: float = 0):
        send_move_command_bezeir(int(x), int(y), int(segments),int(ctrl_x), int(ctrl_y))

    def click(self):
        send_click_command()

