from pynput.mouse import Listener, Button
import keyboard
import win32api
import win32con
import pygetwindow as gw
import pyautogui
import time
import threading
from datetime import datetime
target_pixel = None
clicking_enabled = True
toggle_key_pressed = False
TARGET_COLOR = [(117, 253, 117),(117, 254, 117)]  # Set the RGB value you are looking for


target_pixel_chosen = threading.Event()

def on_click(x, y, button, pressed):
    global target_pixel
    if pressed and button == Button.left:
        target_pixel = (x, y)
        print("Target pixel set at", target_pixel)
        target_pixel_chosen.set()
        return False

def timestamp():
    ts = datetime.now()
    ts = ts.strftime("%H:%M:%S")
    return ts

def activate_chrome_window():
    chrome_window = gw.getWindowsWithTitle("Google Chrome")[0]
    if chrome_window:
        chrome_window.activate()

def click(x, y):
    win32api.SetCursorPos((x, y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)

def toggle_clicking():
    global clicking_enabled, toggle_key_pressed
    clicking_enabled = not clicking_enabled
    toggle_key_pressed = True
    print(timestamp(),"Autoclicker", "enabled" if clicking_enabled else "disabled")

def search_for_cookie():
    target_pixel_chosen.wait()
    while True:
        if clicking_enabled:
            cookie_location = pyautogui.locateOnScreen('cookie.png', grayscale= True, confidence=0.6 )
            if cookie_location:
                cookie_x = cookie_location.left + (cookie_location.width // 2)
                cookie_y = cookie_location.top + (cookie_location.height // 2)              
                print(timestamp(),"Cookie found at", cookie_x, cookie_y)
                time.sleep(0.1)
                click(cookie_x, cookie_y)
        time.sleep(3)  # Wait for 10 seconds before the next search

def search_for_color():
    target_pixel_chosen.wait()
    while True:
        if clicking_enabled:
            # Define the region (left, top, width, height)
            search_region = (1687, 342, 70, 701)  # Set this to your desired region
            print("Searching region:", search_region)
            for x in range(search_region[0], search_region[0] + search_region[2], 3):  
                for y in range(search_region[1] + search_region[3], search_region[1], -3):
                    pixel_color = pyautogui.pixel(x, y)
                    for color in TARGET_COLOR:
                        if pixel_color == color:                         
                            print(timestamp(),"Target color found at", x, y)                            
                            click(x, y)
                            break
        print(timestamp(),"finished searching")
        time.sleep(8)  # Wait for 1 seconds before the next search

def start_auto_clicker():
    global toggle_key_pressed
    print("Autoclicker started. Press 'Q' to toggle clicking.")
    while True:
        if keyboard.is_pressed('q'):
            if not toggle_key_pressed:
                toggle_clicking()
        else:
            toggle_key_pressed = False

        if clicking_enabled and target_pixel:
            activate_chrome_window()
            click(target_pixel[0], target_pixel[1])

def main():
    listener = Listener(on_click=on_click)
    listener.start()

    search_thread1 = threading.Thread(target=search_for_color)
    search_thread1.daemon = True
    search_thread1.start()

    search_thread2 = threading.Thread(target=search_for_cookie)
    search_thread2.daemon = True
    search_thread2.start()

    start_auto_clicker()

if __name__ == "__main__":
    main()
