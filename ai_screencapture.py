import win32gui
import win32con
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
        self.template_herb = cv.imread('img/Herb_Icon.png')
        # self.template_ore = cv.imread('Ore_Icon.png')
        self.nav_loc = None
        self.nav_loc_match = None


        # self.img_health = None
        # self.healthbar_top_left = (127,64)
        # self.healthbar_bottom_right = (295,84)

        # self.enemy_cast_bar = None
        # self.enemy_cast_bar_top_left = (550,210)
        # self.enemy_cast_bar_bottom_right = (743,220)

        # self.enemy_cast_bar_text = None
        # self.enemy_cast_bar_text_top_left = (564,226)
        # self.enemy_cast_bar_text_bottom_right = (733,236)

        self.minimap = None
        self.minimap_center = (1750,231)
        self.minimap_top_left = (1600,81)
        self.minimap_bottom_right = (1900,381)

        self.center_screen = (960, 540)
        self.center_screen_topleft = (955, 535)
        self.center_screen_bottomright = (965, 545)


        self.w, self.h = pyautogui.size()
        print("Width = " + str(self.w) + " Height = " + str(self.h))
        self.monitor = {"top": 0, "left": 0, "width": self.w, "height": self.h}


    def capture_screen(self):
        fps_report_time = time.time()
        fps_report_delay = 2
        n_frames = 1
        # Define a delay interval (in seconds) for printing the "No gather node detected" message
        last_print_time = 0  # Variable to track the time of the last print



        # self.sct = mss.mss(with_cursor=True)
        with mss.mss() as sct:
            while(True):
                
                self.capturedImage = sct.grab(self.monitor)
                self.capturedImage = np.array(self.capturedImage)

                # self.img_health = self.capturedImage[
                # self.healthbar_top_left[1]:self.healthbar_bottom_right[1],
                # self.healthbar_top_left[0]:self.healthbar_bottom_right[0]
                # ]
                # self.img_health_HSV = cv.cvtColor(self.img_health,cv.COLOR_BGR2HSV)

                # self.enemy_cast_bar = self.capturedImage[
                # self.enemy_cast_bar_top_left[1]:self.enemy_cast_bar_bottom_right[1],
                # self.enemy_cast_bar_top_left[0]:self.enemy_cast_bar_bottom_right[0]
                # ]
                # self.enemy_cast_bar_HSV = cv.cvtColor(self.enemy_cast_bar,cv.COLOR_BGR2HSV)

                # self.enemy_cast_bar_text = self.capturedImage[
                # self.enemy_cast_bar_text_top_left[1]:self.enemy_cast_bar_text_bottom_right[1],
                # self.enemy_cast_bar_text_top_left[0]:self.enemy_cast_bar_text_bottom_right[0]
                # ]

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
                    # gather_target = [None,'foundOnMap','moveToTarget','cursorSearching','foundOnCursor']
                    # gather_target = [0]
                    
                    if max_val_herb >= 0.5:
                        # gather_target = [1]
                        cv.rectangle(self.minimap, max_loc_herb, (max_loc_herb[0] + icon_w_herb, max_loc_herb[1] + icon_h_herb), (0, 255, 255), 2)
                        # cv.putText(self.minimap,"Nav Tar: " + str(self.nav_loc) + f"{self.nav_loc_match}",(0, 200), cv.FONT_HERSHEY_DUPLEX,0.5,(255,50,230),1,cv.LINE_AA)

                        if self.nav_loc:
                            # gather_target = [2]
                            turn_angle = np.round(nav.get_nav_turn_angle(self.nav_loc) * 360 / math.pi, 2)
                            pitch_angle = np.round(nav.get_nav_elevation_angle(self.nav_loc) * 360 / math.pi, 2)
                            cv.putText(self.minimap,"Turn: " + str(turn_angle) + "deg",(0, 250), cv.FONT_HERSHEY_DUPLEX,0.5,(255,50,230),1,cv.LINE_AA)
                            # cv.putText(self.minimap,"Pitch: " + str(pitch_angle) + "deg",(0, 225), cv.FONT_HERSHEY_DUPLEX,0.5,(255,50,230),1,cv.LINE_AA)
                            

                            if pitch_angle > 3:
                                move.bump_forward(0.2)  # Move forward when pitch angle is greater than 3
                                if turn_angle > 3:
                                    move.bump_left(0.01)  # Also turn left if turn angle is greater than 3
                                elif turn_angle < -3:
                                    move.bump_right(0.01)  # Or turn right if turn angle is less than -3
                                pass
                            elif -3 <= pitch_angle <= 3:
                                # Neutral pitch angle condition (between -5 and 5)
                                # gather_target = [3]
                                move.sit(5)
                                move.cursor_search(620, 357, 692, 369)
                                ##if found then click, wait for 4 seconds then set gather_target to [0]
                                if turn_angle > 3:
                                    # Turn left if turn angle is greater than 5
                                    move.bump_left(0.01)
                                elif turn_angle < -3:
                                    # Turn right if turn angle is less than -5
                                    move.bump_right(0.01)
                                else:
                                    # If no significant turn angle, just move forward
                                    move.bump_forward(0.2)

                    ## FPS DROP START HERE
                    # else:
                    #     if fps_report_time - last_print_time >= fps_report_delay:
                    #         print('No gather node detected')
                    #         move.bump_forward(0.5)
                    #         # cv.putText(small,"Nav Target: "+ str(self.nav_loc) + f" {self.nav_loc_match}%",(30, 200), cv.FONT_HERSHEY_DUPLEX,1,(0,255,0),1,cv.LINE_AA)

                    ## FPS DROP END HERE



                if self.enable_cv_preview:
                    small = cv.resize(self.capturedImage, (0, 0), fx=0.5, fy=0.5)
                    if self.fps is None:
                        fps_text = ""
                    else:
                        fps_text = f'FPS: {self.fps:.2f}'

                    # cv.putText(small,fps_text,(30, 30), cv.FONT_HERSHEY_DUPLEX,1,(255,50,230),1,cv.LINE_AA)


                    # cv.putText(small,"Health: " + str(hue_match_pct(self.img_health_HSV,80,115)),(30, 100), cv.FONT_HERSHEY_DUPLEX,1,(0,0,255),1,cv.LINE_AA)

                    # cv.putText(small,"Enemy Cast %: "+ str(hue_match_pct(self.enemy_cast_bar_HSV,34,52)),(30, 150), cv.FONT_HERSHEY_DUPLEX,1,(0,0,255),1,cv.LINE_AA)
                    # enemy_cast_percent = hue_match_pct(self.enemy_cast_bar_HSV,34,52)

                    # if(int(enemy_cast_percent) > 80 and int(enemy_cast_percent) < 90):
                    #     print("Enemy Casting % " + str(hue_match_pct(self.enemy_cast_bar_HSV,34,52)))
                    #     interrupt_enemy()
                    
                    # cv.imshow("Computer Vision", small)

                    # cv.imshow("Enemy Cast Bar", self.enemy_cast_bar)
                    # cv.imshow("Enemy Cast Bar Text", self.enemy_cast_bar_text)

                    
                    cv.imshow("Minimap", self.minimap)
                    make_window_always_on_top('Minimap')
                    cv.waitKey(1)

                elapsed_time = time.time() - fps_report_time
                if elapsed_time >= fps_report_delay:
                    self.fps = n_frames / elapsed_time
                    fps_text = 'FPS: {:.2f}'.format(self.fps)
                    print(fps_text)
                    # print(gather_target)
                    n_frames = 0
                    fps_report_time = time.time()
                n_frames += 1
                    
                
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
    # Check if Alt, Ctrl or Shift is pressed by player then bot will not interupt
    if not keyboard.is_pressed('alt' or keyboard.is_pressed('ctrl') or keyboard.is_pressed('shift')):
        pyautogui.press('f2')


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