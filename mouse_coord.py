import pyautogui
import time

while(True):
    # Get the current mouse position
    x, y = pyautogui.position()
    print(f"Current mouse position is {x}, {y}")
    time.sleep(1)
