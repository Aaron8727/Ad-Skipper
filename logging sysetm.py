import cv2
import pyautogui
import time
import numpy as np
from PIL import ImageGrab

# Define the deadzone (where the white circle and X are located)
deadzone_x1, deadzone_y1 = 0, 0  # Top-left corner of the deadzone
deadzone_x2, deadzone_y2 = 1850, 1080  # Bottom-right corner of the deadzone
#define 2nd deadzone
deadzone_x3, deadzone_y3 =0,100
deadzone_x4, deadzone_y4 = 1920,1080

whitezone_x1, whitezone_y1 = 1508, 400  # Top-left corner of the whitezone (adjust as needed)
whitezone_x2, whitezone_y2 = 1885, 550  # Bottom-right corner of the whitezone (adjust as needed)

# Function to detect the template (e.g., arrow or X button) on the right side of the screen
def detect_template(template_paths, threshold=0.85, check_deadzone=True):
    # Capture a screenshot
    screenshot = ImageGrab.grab()
    screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
    screenshot_gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)

    # Get the dimensions of the screenshot
    height, width = screenshot_gray.shape

    # Crop the screenshot to only the right half
    right_half = screenshot_gray[:, width // 2:]

    # Try to match each template in the list of templates
    for template_path in template_paths:
        #print(f"Trying to match template: {template_path}")
        template = cv2.imread(template_path, cv2.IMREAD_COLOR)
        template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)

        # Try different scales for the template (multi-scale matching)
        for scale in np.linspace(0.5,1.5,13):  # Scale range from 70% to 130%, adjust as needed
            resized_template = cv2.resize(template_gray, None, fx=scale, fy=scale, interpolation=cv2.INTER_LINEAR)

            if resized_template.shape[1] > right_half.shape[1] or resized_template.shape[0] > right_half.shape[0]:
                continue  # Skip if resized template is larger than the screenshot

            # Perform template matching on the right half
            result = cv2.matchTemplate(right_half, resized_template, cv2.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

            # If match quality is high enough, check the coordinates
            if max_val >= threshold:
                #print(f"Detected {template_path} at scale {scale} with confidence {max_val}")
                x, y = max_loc
                template_w, template_h = resized_template.shape[1], resized_template.shape[0]
                # Adjust the x-coordinate to account for cropping (right half only)
                detected_x = x + width // 2 + template_w // 2
                detected_y = y + template_h // 2


                # Check if the detected point is inside the deadzone, but only if `check_deadzone` is True
                if check_deadzone and deadzone_x1 <= detected_x <= deadzone_x2 and deadzone_y1 <= detected_y <= deadzone_y2:
                 #  print("detected in deadzone 1")
                    continue
                elif check_deadzone and deadzone_x3 <= detected_x <= deadzone_x4 and deadzone_y3 <= detected_y <= deadzone_y4:
                  # print("detected in deadzone 2")
                    continue
                print({template_path})
                return (detected_x, detected_y)

    print("No template detected.")
    return None  # No match found

# Function to click on a position on the screen
def click_position(position):
    pyautogui.moveTo(position)
    pyautogui.click()
def scroll_position_here(position):
    pyautogui.moveTo(position)
    pyautogui.scroll(-200)
    time.sleep(0.5)

def Press_likely_x_pos():
    likely_x_pos = (1876,43)
    likely_otherx_pos = (1873,71)
    likely_otherx1_pos = (1875,44)

    click_position(likely_x_pos)
    time.sleep(1)
    click_position(likely_otherx_pos)
    #time.sleep(1)
    #click_position(likely_otherx1_pos)

# Function to press the home and reset buttons using predetermined positions
def press_home_and_reset_predetermined():
    home_button_position = (1900, 650)  # Example: Predetermined home button position
    reset_button_position = (1815, 160)  # Example: Predetermined reset button position

    # Click on the home button
    print(f"Clicking on the predetermined home button position: {home_button_position}")
    click_position(home_button_position)
    time.sleep(1)

    # Click on the reset button
    print(f"Clicking on the predetermined reset button position: {reset_button_position}")
    click_position(reset_button_position)
    time.sleep(1)

def Reset_System():

    open_tabs_button_position = (1904, 683)
    close_tabs_button_position = (1831,68)
    reset_button_position = (1811, 162)

    click_position(open_tabs_button_position)
    time.sleep(1)

    click_position(close_tabs_button_position)
    time.sleep(1)

    click_position(reset_button_position)
    time.sleep(1)

def press_lime_open_ads():

    Lime_scooter_position = (1705,455)
    bottom_of_screen_scroll_pos = (1700,630)
    whats_this_button = (1749,397)
    see_ride_time_button = (1701,621)
    watch_ads_button = (1711,387)

    # Click on the  Lime_scooter_position
    time.sleep(3)
    print(f"Clicking on the predetermined home button position: {Lime_scooter_position}")
    click_position(Lime_scooter_position)
    time.sleep(2)
    # scroll down on bottom_of_screen_scroll_pos
    print(f"Clicking on the predetermined reset button position: {bottom_of_screen_scroll_pos}")
    scroll_position_here(bottom_of_screen_scroll_pos)
    time.sleep(2)
    # click on whats_this_button
    print(f"Clicking on the predetermined reset button position: {whats_this_button}")
    click_position(whats_this_button)
    time.sleep(2)
    # click on see_ride_time_button
    print(f"Clicking on the predetermined reset button position: {see_ride_time_button}")
    click_position(see_ride_time_button)
    time.sleep(2)
    # click on watch_ads_button
    print(f"Clicking on the predetermined reset button position: {watch_ads_button}")
    click_position(watch_ads_button)
    time.sleep(2)

# Main loop
x_button_templates = [
    'images/x_button.JPG',
    'images/x_button2.JPG',
   # 'images/x_button3.JPG',
    'images/x_button4.JPG',
    'images/x_button5.JPG',
    'images/x_button6.JPG',
    'images/x_button7.jpg',
    'images/x_button8.JPG',
    'images/x_button9.JPG',
    #'images/x_button10.JPG',
    'images/x_button11.JPG'
]  # Paths to the X button templates

arrow_button_templates = [
    'images/arrow.JPG',
    'images/arrow2.jpg',
    'images/arrow3.jpg',
    'images/arrow4.JPG',
    'images/arrow5.JPG'
]  # Paths to the arrow button templates

play_next_ad_template = [
    'images/button.JPG',
    'images/button3.JPG'
]  # Paths to the play next ad button templates

stupid_surveypage_template = [
    'images/surveypage.JPG',
    'images/surveypage google.JPG'
]  # Paths to the play next ad button templates
Lime_homescreen_template = [
    'images/homescreen.JPG'
]

# Start time tracking for detecting "play next ad" button
start_time = time.time()
start_total_time = time.time()
while True:
    # Print current time for debugging purposes
    elapsed_time = time.time() - start_time
    elapsed_total_time = time.time() - start_total_time
    print(f"\nElapsed time: {elapsed_time:.2f} seconds")

    # Check if 30 seconds have passed without detecting the "next ad" button
    if elapsed_time >= 40:
        print("40 seconds passed without detecting the play next ad button, pressing home and reset buttons...")
        press_home_and_reset_predetermined()  # Use the predetermined positions
        start_time = time.time()  # Reset the timer after pressing the buttons
    if elapsed_time >= 32:
        print("35 seconds passed trying likely x pos")
        Press_likely_x_pos()

    if elapsed_total_time >= 1500:
        print("system reset")
        Reset_System()
        start_total_time = time.time()
    #print(elapsed_total_time,"total seconds elapsed")

    homescreen_pos = detect_template(Lime_homescreen_template, check_deadzone=False)

    if homescreen_pos:
        print("homescreen detected")
        press_lime_open_ads()
        start_time = time.time()

    # Try to detect any of the play next ad buttons without checking the deadzone
    nextad_button_pos = detect_template(play_next_ad_template, check_deadzone=False)

    # If a "next ad" button is detected, click it and reset the timer
    if nextad_button_pos:
        detected_x, detected_y = nextad_button_pos
        if whitezone_x1 <= detected_x <= whitezone_x2 and whitezone_y1 <= detected_y <= whitezone_y2:
            print("Next ad button detected within whitezone, clicking the button...")
            click_position(nextad_button_pos)
            start_time = time.time()
        else:
            print("Next ad button detected but outside whitezone, skipping click.")

    # Try to detect any of the arrow button variants first
    arrow_pos = detect_template(arrow_button_templates, check_deadzone=True)

    # If an arrow button is detected, click it and wait 3 seconds
    if arrow_pos:
        print("Arrow detected, clicking it...")
        click_position(arrow_pos)
          # Wait for 3 seconds after clicking the arrow

    # Try to detect any of the X button variants next
    x_button_pos = detect_template(x_button_templates, check_deadzone=True)

    # If an X button is detected, click it
    if x_button_pos:
        print("X button detected, closing the ad...")
        click_position(x_button_pos)

    stupid_surveypage_pos = detect_template(stupid_surveypage_template, check_deadzone=False)

    if stupid_surveypage_pos:
        print("stupid surveypage detected, resettingn...")
        press_home_and_reset_predetermined()
        start_time = time.time()
        # Reset the timer since the button was found
    # Wait before checking again (adjust as needed)
    time.sleep(1)
