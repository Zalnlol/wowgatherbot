import time
import pyautogui

KEY_RUN_WALK = '\\'
KEY_JUMP = 'space'
KEY_LEFT = 'a'
KEY_RIGHT = 'd'
KEY_FORWARD = 'w'
KEY_BACKWARD = 's'
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

def sit():
    pyautogui.press(KEY_SIT)

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