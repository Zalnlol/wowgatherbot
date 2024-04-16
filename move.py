import time
import pyautogui
import random
import keyboard
from pynput.mouse import Listener, Controller

KEY_RUN_WALK = '\\'
KEY_JUMP = 'space'
KEY_LEFT = 'a'
KEY_RIGHT = 'd'
KEY_FORWARD = 'w'
KEY_BACKWARD = 'down'
KEY_STRAFE_LEFT = 'q'
KEY_STRAFE_RIGHT = 'e'
KEY_SIT = 'x'

def toggle_run():
    pyautogui.press(KEY_RUN_WALK)

def forward_start():
    pyautogui.keyDown(KEY_FORWARD)

def forward_stop():
    pyautogui.keyUp(KEY_FORWARD)

def backward_start():
    pyautogui.keyDown(KEY_BACKWARD)

def backward_stop():
    pyautogui.keyUp(KEY_BACKWARD)

def right_start():
    pyautogui.keyDown(KEY_RIGHT)

def right_stop():
    pyautogui.keyUp(KEY_RIGHT)

def left_start():
    pyautogui.keyDown(KEY_LEFT)

def left_stop():
    pyautogui.keyUp(KEY_LEFT)

def right_strafe_start():
    pyautogui.keyDown(KEY_STRAFE_RIGHT)

def right_strafe_stop():
    pyautogui.keyUp(KEY_STRAFE_RIGHT)

def left_strafe_start():
    pyautogui.keyDown(KEY_STRAFE_LEFT)

def left_strafe_stop():
    pyautogui.keyUp(KEY_STRAFE_LEFT)

def jump():
    pyautogui.press(KEY_JUMP)

def sit(t):
    pyautogui.keyDown(KEY_SIT)
    time.sleep(t)
    pyautogui.keyUp(KEY_SIT)

def fly_down_start():
    pyautogui.keyDown(KEY_SIT)

def fly_down_stop():
    pyautogui.keyUp(KEY_SIT)

def bump_forward(t):
    pyautogui.keyDown(KEY_FORWARD)
    time.sleep(t)
    pyautogui.keyUp(KEY_FORWARD)

def bump_backward(t):
    pyautogui.keyDown(KEY_BACKWARD)
    time.sleep(t)
    pyautogui.keyUp(KEY_BACKWARD)

def bump_left(t):
    pyautogui.keyDown(KEY_LEFT)
    time.sleep(t)
    pyautogui.keyUp(KEY_LEFT)

def bump_right(t):
    pyautogui.keyDown(KEY_RIGHT)
    time.sleep(t)
    pyautogui.keyUp(KEY_RIGHT)


# Function to check the current cursor icon
def check_cursor_icon():
    position = pyautogui.position()
    return pyautogui.screenshot().getpixel(position)[:3]  # Get RGB color at mouse position

# Function to be called when mouse moves
def on_move(x, y):
    # Check cursor icon and perform actions based on the icon
    cursor_color = check_cursor_icon()
    # Assuming the herb icon has a specific RGB color (e.g., orange)
    if cursor_color == (218, 173, 99):  # Adjust RGB values to match your herb icon color
        print("Herb detected! Perform action here...")

def cursor_search(left, top, width, height):
    try:
        start_time = time.time()
        prev_x = None
        
        while (time.time() - start_time) < 5:  # Maximum 5 seconds execution time
            # Generate random coordinates within the rectangle
            # Biasing the random selection towards the edges
            x_choices = [left, left + width]
            if prev_x is not None and prev_x in x_choices:
                x_choices.remove(prev_x)
            x = random.choice(x_choices)
            y = random.randint(top, top + height)
            
            # Generate a random duration with slight variations
            duration = random.uniform(0.1, 0.3)
            
            # Move the mouse to the generated coordinates smoothly and with variability
            pyautogui.moveTo(x, y, duration=duration)
            
            # Break the loop if 'esc' key is pressed
            if keyboard.is_pressed('esc'):
                break
            
            # Update previous x-coordinate
            prev_x = x
            
            # Add a slight delay before the next movement
            time.sleep(random.uniform(0.1, 0.5))
        
    except KeyboardInterrupt:
        print("Movement stopped by user.")

    # Ensure the mouse cursor returns to the original position after the loop exits
    pyautogui.moveTo(left + (width // 2), top + (height // 2), duration=0.2)

# Example usage:
# Replace the coordinates with the coordinates of your rectangle box
# (left, top, width, height)
# cursor_search(620, 357, 692, 369)


if __name__ == "__main__":
    time.sleep(5)
    while True:
        jump()
        time.sleep(1)
        forward_start()
        time.sleep(2)
        left_strafe_start()
        time.sleep(1)
        left_strafe_stop()
        time.sleep(1)

        right_strafe_start()
        time.sleep(1)
        right_strafe_stop()
        time.sleep(1)
        forward_stop()
        time.sleep(1)

        backward_start()
        time.sleep(2)
        backward_stop()
        time.sleep(1)