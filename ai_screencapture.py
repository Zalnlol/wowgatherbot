import win32gui
import win32con
import tkinter as tk
import mss
import pyautogui
import cv2 as cv
import numpy as np
import time
import multiprocessing
import keyboard
import move
import nav
import map_reader

import random
import math



class ScreenCaptureAgent:

    def __init__(self) -> None:
        self.img = None
        self.img_health_HSV = None
        self.enemy_cast_bar_HSV = None
        self.capture_process = None
        self.fps = None
        self.enable_cv_preview = True

        self.zone = None

        self.enable_gather = True
        self.template_herb = cv.imread('Herb_Icon.png')
        self.template_ore = cv.imread('Ore_Icon.png')
        self.nav_loc = None
        self.nav_loc_match = None


        self.img_health = None
        self.healthbar_top_left = (127,64)
        self.healthbar_bottom_right = (295,84)

        self.enemy_cast_bar = None
        self.enemy_cast_bar_top_left = (550,210)
        self.enemy_cast_bar_bottom_right = (743,220)

        self.enemy_cast_bar_text = None
        self.enemy_cast_bar_text_top_left = (564,226)
        self.enemy_cast_bar_text_bottom_right = (733,236)

        self.minimap = None
        self.minimap_top_left = (1609,91)
        self.minimap_bottom_right = (1887,369)

        self.center_screen = (960, 540)
        self.center_screen_topleft = (955, 535)
        self.center_screen_bottomright = (965, 545)


        self.w, self.h = pyautogui.size()
        print("Width = " + str(self.w) + " Height = " + str(self.h))
        self.monitor = {"top": 0, "left": 0, "width": self.w, "height": self.h}




    def capture_screen(self):
        fps_report_time = time.time()
        fps_report_delay = 5
        n_frames = 1
        with mss.mss() as sct:
            while(True):
                self.capturedImage = sct.grab(self.monitor)
                self.capturedImage = np.array(self.capturedImage)

                self.img_health = self.capturedImage[
                self.healthbar_top_left[1]:self.healthbar_bottom_right[1],
                self.healthbar_top_left[0]:self.healthbar_bottom_right[0]
                ]
                self.img_health_HSV = cv.cvtColor(self.img_health,cv.COLOR_BGR2HSV)

                self.enemy_cast_bar = self.capturedImage[
                self.enemy_cast_bar_top_left[1]:self.enemy_cast_bar_bottom_right[1],
                self.enemy_cast_bar_top_left[0]:self.enemy_cast_bar_bottom_right[0]
                ]
                self.enemy_cast_bar_HSV = cv.cvtColor(self.enemy_cast_bar,cv.COLOR_BGR2HSV)

                self.enemy_cast_bar_text = self.capturedImage[
                self.enemy_cast_bar_text_top_left[1]:self.enemy_cast_bar_text_bottom_right[1],
                self.enemy_cast_bar_text_top_left[0]:self.enemy_cast_bar_text_bottom_right[0]
                ]

                self.minimap = self.capturedImage[
                self.minimap_top_left[1]:self.minimap_bottom_right[1],
                self.minimap_top_left[0]:self.minimap_bottom_right[0]
                ]
                self.minimap_HSV = cv.cvtColor(self.minimap,cv.COLOR_BGR2HSV)

                if self.enable_gather:
                    nav_loc_herb = cv.matchTemplate(self.minimap_HSV, self.template_herb, cv.TM_CCOEFF_NORMED)

                    ## Define width and height of the template images
                    icon_w_herb = self.template_herb.shape[1]
                    icon_h_herb = self.template_herb.shape[0]

                    ## Find the location of the best match for each template
                    min_val_herb, max_val_herb, min_loc_herb, max_loc_herb = cv.minMaxLoc(nav_loc_herb)
                    self.nav_loc = max_loc_herb
                    
                    if max_val_herb >= 0.4:
                        cv.rectangle(self.minimap, max_loc_herb, (max_loc_herb[0] + icon_w_herb, max_loc_herb[1] + icon_h_herb), (0, 255, 255), 2)
                        cv.putText(self.minimap,"Nav Tar: " + str(self.nav_loc) + f"{self.nav_loc_match}",(0, 200), cv.FONT_HERSHEY_DUPLEX,0.5,(255,50,230),1,cv.LINE_AA)

                        if self.nav_loc:
                            turn_angle = np.round(nav.get_nav_turn_angle(self.nav_loc) * 360 / 3.14, 2)
                            pitch_angle = np.round(nav.get_nav_elevation_angle(self.nav_loc) * 360 / 3.14, 2)
                            cv.putText(self.minimap,"Turn: " + str(turn_angle) + "deg",(0, 250), cv.FONT_HERSHEY_DUPLEX,0.5,(255,50,230),1,cv.LINE_AA)
                            cv.putText(self.minimap,"Pitch: " + str(pitch_angle) + "deg",(0, 300), cv.FONT_HERSHEY_DUPLEX,0.5,(255,50,230),1,cv.LINE_AA)
                            
                            if turn_angle > 5:
                                move.bump_left(0.01)
                            elif turn_angle < -5:
                                move.bump_right(0.01)
                            else:
                                continue
                            
                            if pitch_angle > 5:
                                move.bump_forward(0.1)
                                # continue
                            elif pitch_angle < 5:
                                move.sit(2)
                                ## Replace the coordinates with the coordinates of your rectangle box (left, top, width, height)
                                # cursor_search(620, 357, 692, 369)
                            

                    else:
                        print('No gather node detected')
                        # cv.putText(small,"Nav Target: "+ str(self.nav_loc) + f" {self.nav_loc_match}%",(30, 200), cv.FONT_HERSHEY_DUPLEX,1,(0,255,0),1,cv.LINE_AA)


                if self.enable_cv_preview:
                    small = cv.resize(self.capturedImage, (0, 0), fx=0.5, fy=0.5)
                    if self.fps is None:
                        fps_text = ""
                    else:
                        fps_text = f'FPS: {self.fps:.2f}'

                    cv.putText(small,fps_text,(30, 30), cv.FONT_HERSHEY_DUPLEX,1,(255,50,230),1,cv.LINE_AA)
                    cv.putText(small,"Health: " + str(hue_match_pct(self.img_health_HSV,80,115)),(30, 100), cv.FONT_HERSHEY_DUPLEX,1,(0,0,255),1,cv.LINE_AA)

                    cv.putText(small,"Enemy Cast %: "+ str(hue_match_pct(self.enemy_cast_bar_HSV,34,52)),(30, 150), cv.FONT_HERSHEY_DUPLEX,1,(0,0,255),1,cv.LINE_AA)
                    enemy_cast_percent = hue_match_pct(self.enemy_cast_bar_HSV,34,52)
                    if(int(enemy_cast_percent) > 80 and int(enemy_cast_percent) < 90):
                        print("Enemy Casting % " + str(hue_match_pct(self.enemy_cast_bar_HSV,34,52)))
                        ## interrupt_enemy()
                    
                    # cv.imshow("Computer Vision", small)

                    # cv.imshow("Enemy Cast Bar", self.enemy_cast_bar)
                    # cv.imshow("Enemy Cast Bar Text", self.ewnemy_cast_bar_text)
                    cv.imshow("Minimap", self.minimap)
                    make_window_always_on_top('Minimap')
                    cv.waitKey(1)






                # elapsed_time = time.time() - fps_report_time
                # if elapsed_time >= fps_report_delay:
                #     self.fps = n_frames / elapsed_time
                #     print("FPS:" + str(self.fps))
                #     n_frames = 0
                #     fps_report_time = time.time()
                # n_frames += 1
                    



                
class bcolors:
    PINK = '\033[95m'
    CYAN = '\033[96m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    ENDC = '\033[0m'

def convert_hue(hue):
    ratio = 361 / 180
    return np.round(hue / ratio, 2)

def interrupt_enemy():
    # Check if Alt is pressed
    if not keyboard.is_pressed('alt' or keyboard.is_pressed('ctrl') or keyboard.is_pressed('shift')):
        pyautogui.press('f2')
    # If Alt is pressed, it will skip pressing F2


def toggle_ui():
    # Press and hold the Alt key
    pyautogui.keyDown('alt')
    time.sleep(0.3)

    # Press the 'x' key
    pyautogui.keyDown('x')
    time.sleep(0.3)

    # Release the 'x' key
    pyautogui.keyUp('x')
    time.sleep(0.3)

    # Release the Alt key
    pyautogui.keyUp('alt')


def cursor_search(left, top, width, height):
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
# cursor_search(620, 357, 692, 369)




def hue_match_pct(img, hue_low, hue_high):
    match_pixels = 0
    no_match_pixels = 0
    for pixel in img:
        for h,s,v in pixel:
            if convert_hue(hue_low) <= h <= convert_hue(hue_high):
                match_pixels += 1
            else:
                no_match_pixels += 1
        total_pixels = match_pixels + no_match_pixels
        return np.round(match_pixels/total_pixels, 2)*100

def make_window_always_on_top(window_name):
    hwnd = win32gui.FindWindow(None, window_name)
    win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0,
                          win32con.SWP_NOMOVE | win32con.SWP_NOSIZE | win32con.SWP_NOACTIVATE)


def print_menu():
    print(f'{bcolors.CYAN}Command Menu{bcolors.ENDC}')
    print(f'{bcolors.GREEN}\tr - run\t\t Start screen capture{bcolors.ENDC}')
    print(f'{bcolors.PINK}\ts - stop\t Stop program{bcolors.ENDC}')
    print(f'{bcolors.YELLOW}\tq - quit\t Quit program{bcolors.ENDC}')

if __name__ == "__main__":
    screen_agent = ScreenCaptureAgent()
    while(True):
        #Print menu
        print_menu()
        user_input = input().strip().lower()
        if(user_input == 'quit' or user_input == 'q'):
            if screen_agent.capture_process is not None:
                screen_agent.capture_process.terminate()
            break
        elif(user_input == 'run' or user_input == 'r'):
            if screen_agent.capture_process is not None:
                print(f'{bcolors.YELLOW}Capture process is already running{bcolors.ENDC}')
                continue
            screen_agent.capture_process = multiprocessing.Process(
                target=screen_agent.capture_screen,
                args=(),
                name="Screen Capture Process"
            )
            screen_agent.capture_process.start()
        elif(user_input == 'stop' or user_input == 's'):
            if screen_agent.capture_process is None:
                print(f'{bcolors.YELLOW}Capture process is not running{bcolors.ENDC}')
                continue
            screen_agent.capture_process.terminate()
            screen_agent.capture_process = None
        else:
            print(f'{bcolors.RED}Invalid command{bcolors.ENDC}')

    #Get User Input


    #Start / Stop / Quit
print('Done')