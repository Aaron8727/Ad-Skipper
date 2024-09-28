import cv2
import pyautogui
import time
import numpy as np
from PIL import ImageGrab


# Function to detect the template (e.g., arrow or X button) on the screen using multi-scale template matching
def detect_template(template_paths, threshold=0.77):
    # Capture a screenshot
    screenshot = ImageGrab.grab()
    screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
    screenshot_gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)

    # Try to match each template in the list of templates
    for template_path in template_paths:
        template = cv2.imread(template_path, cv2.IMREAD_COLOR)
        template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
        template_w, template_h = template_gray.shape[1], template_gray.shape[0]

        # Try different scales for the template (multi-scale matching)
        for scale in np.linspace(0.9, 1.1, 10):  # Scale range from 70% to 130%, adjust as needed
            resized_template = cv2.resize(template_gray, None, fx=scale, fy=scale, interpolation=cv2.INTER_LINEAR)

            if resized_template.shape[1] > screenshot_gray.shape[1] or resized_template.shape[0] > screenshot_gray.shape[0]:
                continue  # Skip if resized template is larger than the screenshot

            # Perform template matching
            result = cv2.matchTemplate(screenshot_gray, resized_template, cv2.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

            # If match quality is high enough, return the location of the template
            if max_val >= threshold:
                print(f"Detected {template_path} at scale {scale} with confidence {max_val}")
                x, y = max_loc
                template_w, template_h = resized_template.shape[1], resized_template.shape[0]
                return (x + template_w // 2, y + template_h // 2)

    return None  # No match found


# Function to click on a position on the screen
def click_position(position):
    pyautogui.moveTo(position)
    pyautogui.click()


# Main loop
x_button_templates = [
    'images/x.JPG',
    'images/x 2.JPG',
    'images/x 3.JPG',
    'images/x 4.JPG',
    'images/x 5.JPG',
    'images/x 6.JPG',
    'images/x 7.JPG',
    'images/x 8.JPG'
]  # Paths to the X button templates

arrow_button_templates = [
    'images/arrow.JPG',
    'images/arrow 2.JPG',
    'images/arrow 3.JPG',
    'images/arrow 4.JPG',
    'images/arrow 5.JPG',
    'images/arrow 6.JPG',
    'images/arrow 7.JPG',
    'images/arrow 8.JPG',
    'images/arrow 9.JPG'
]  # Paths to the arrow button templates

play_next_ad_template = [
    'images/play_next_ad_button.JPG',
    'images/play_next_ad_button 2.JPG',
    'images/play_next_ad_button 3.JPG',
    'images/play_next_ad_button 4.JPG',
    'images/play_next_ad_button 5.JPG'
]  # Paths to the arrow button templates

while True:
    # Try to detect any of the arrow button variants first
    arrow_pos = detect_template(arrow_button_templates)

    # If an arrow button is detected, click it and wait 3 seconds
    if arrow_pos:
        print("Arrow detected, clicking it...")
        click_position(arrow_pos)
        time.sleep(.1)  # Wait for 3 seconds after clicking the arrow

    # Try to detect any of the X button variants next
    x_button_pos = detect_template(x_button_templates)

    # If an X button is detected, click it
    if x_button_pos:
        print("X button detected, closing the ad...")
        click_position(x_button_pos)

    # Wait before checking again (adjust as needed)
    time.sleep(.1)

    # Try to detect any of the play next ad buttons
    nextad_button_pos = detect_template(play_next_ad_template)

    # If a "next ad" button is detected, click it
    if nextad_button_pos:
        print("Next ad button detected, clicking the button...")
        click_position(nextad_button_pos)

    # Wait before checking again (adjust as needed)
    time.sleep(.1)
