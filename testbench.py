import cv2
import pyautogui
import time
import numpy as np
from PIL import ImageGrab

# Define a region of the screen where the ad typically appears
# You need to replace these values with the actual coordinates (left, top, width, height) of the ad region
AD_REGION = (1460, 3, 1886, 789)  # Example coordinates for the BlueStacks window region

# Function to detect the template (e.g., arrow or X button) within a specific region of the screen
def detect_template(template_paths, region=None):
    # Capture a screenshot of a specific region
    if region:
        screenshot = ImageGrab.grab(bbox=region)  # Grab only the region specified
    else:
        screenshot = ImageGrab.grab()  # Grab the entire screen if no region is specified

    screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

    # Try to match each template in the list of templates
    for template_path in template_paths:
        template = cv2.imread(template_path, cv2.IMREAD_COLOR)

        # Perform template matching
        result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

        # If match quality is high (adjust the threshold as needed), return the location of the template
        threshold = 0.95  # Adjust this if detection is too sensitive or not sensitive enough
        if max_val >= threshold:
            x, y = max_loc
            template_w, template_h = template.shape[1], template.shape[0]
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
    'images/x 6.JPG'
]  # Paths to the X button templates

arrow_button_templates = [
    'images/arrow.JPG',
    'images/arrow 2.JPG',
    'images/arrow 3.JPG',
    'images/arrow 4.JPG'
]  # Paths to the arrow button templates

play_next_ad_template = [
    'images/play_next_ad_button.JPG',
    'images/play_next_ad_button 2.JPG',
    'images/play_next_ad_button 3.JPG'
]  # Paths to the play next ad templates

while True:
    # Try to detect any of the arrow button variants first, only within the specified region
    arrow_pos = detect_template(arrow_button_templates, region=AD_REGION)

    # If an arrow button is detected, click it and wait 3 seconds
    if arrow_pos:
        print("Arrow detected, clicking it...")
        click_position(arrow_pos)
        time.sleep(3)  # Wait for 3 seconds after clicking the arrow

    # Try to detect any of the X button variants next, only within the specified region
    x_button_pos = detect_template(x_button_templates, region=AD_REGION)

    # If an X button is detected, click it
    if x_button_pos:
        print("X button detected, closing the ad...")
        click_position(x_button_pos)

    # Try to detect any of the play next ad buttons, only within the specified region
    nextad_button_pos = detect_template(play_next_ad_template, region=AD_REGION)

    # If a play next ad button is detected, click it
    if nextad_button_pos:
        print("Next ad button detected, clicking the button...")
        click_position(nextad_button_pos)

    # Wait before checking again (adjust as needed)
    time.sleep(1)
