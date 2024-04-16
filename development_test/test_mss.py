import mss
import cv2 as cv
import numpy as np
import win32gui
import win32ui
import win32con
from PIL import Image
import pyautogui

def get_window_rect(hwnd):
    # Get the client area dimensions
    rect = win32gui.GetClientRect(hwnd)
    # Get the top-left corner and width/height of the client area
    left, top, right, bottom = win32gui.GetClientRect(hwnd)
    # Convert client area coordinates to screen coordinates
    top_left = win32gui.ClientToScreen(hwnd, (left, top))
    bottom_right = win32gui.ClientToScreen(hwnd, (right, bottom))
    # Calculate the dimensions of the client area in screen coordinates
    width = bottom_right[0] - top_left[0]
    height = bottom_right[1] - top_left[1]
    return {"left": top_left[0], "top": top_left[1], "width": width, "height": height}

# Specify the name of the target window
target_window_name = "World of Warcraft"

# Get the handle (HWND) of the target window
hwnd = win32gui.FindWindow(None, target_window_name)

if hwnd == 0:
    print(f"Window '{target_window_name}' not found.")
    exit()

# Get the dimensions of the window client area in screen coordinates
monitor = get_window_rect(hwnd)

print(f"Capturing window '{target_window_name}'")


with mss.mss() as sct:
    while True:
        img = sct.grab(monitor)
        img = np.array(img)
        # small = cv.resize(img, (0, 0), fx=0.5, fy=0.5)
        # # Get mouse cursor position
        # cursor_pos = pyautogui.position()


        cursor_img = sct._cursor_impl()
        cv.imshow("Cursor", cursor_img)


        cv.imshow("Computer Vision", img)

        # Break loop and end test
        key = cv.waitKey(1)
        if key == ord('q'):
            break

cv.destroyAllWindows()
