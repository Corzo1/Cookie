import pyautogui
import time

while True:
    x, y = pyautogui.position()
    pixel_color = pyautogui.pixel(x, y)
    print(f"Mouse position: ({x}, {y})  RGB: {pixel_color}")
    time.sleep(2)
