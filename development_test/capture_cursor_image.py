from mss import mss
from PIL import Image
import time

def capture_mouse_cursor():
    with mss() as sct:
        # Capture the cursor using the _cursor_impl method
        cursor_img = sct._cursor_impl()

        # Extract pixel data and create a PIL Image
        img = Image.frombytes("RGB", cursor_img.size, cursor_img.rgb)

        # Display the PIL Image
        img.show()  # Opens the image in the default image viewer

        # Alternatively, save the image to a file
        img.save("mouse_default.png")  # Save the image as PNG format

if __name__ == "__main__":
    time.sleep(3)
    capture_mouse_cursor()
