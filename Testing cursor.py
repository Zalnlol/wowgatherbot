import pyautogui
import random
import time
import keyboard

def move_mouse_within_rectangle(left, top, width, height):
    try:
        prev_x = None
        while True:
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
            
            # Break the loop
            if keyboard.is_pressed('esc'):
                break
            
            # Update previous x-coordinate
            prev_x = x
            
            # Add a slight delay before the next movement
            time.sleep(random.uniform(0.1, 0.5))
    except KeyboardInterrupt:
        print("Movement stopped by user.")

# Example usage:
# Replace the coordinates with the coordinates of your rectangle box
# (left, top, width, height)
move_mouse_within_rectangle(620, 357, 692, 369)
