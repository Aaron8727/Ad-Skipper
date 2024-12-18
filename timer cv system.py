import cv2
import pyautogui
import time
import numpy as np
from PIL import ImageGrab

# Define the deadzone (where the white circle and X are located)
# You need to adjust these values based on the actual coordinates in the image
deadzone_x1, deadzone_y1 = 0, 0  # Top-left corner of the deadzone
deadzone_x2, deadzone_y2 = 1800, 1080  # Bottom-right corner of the deadzone

# Function to detect the template (e.g., arrow or X button) on the right side of the screen
def detect_template(template_paths, threshold=0.8, check_deadzone=True):
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
        template = cv2.imread(template_path, cv2.IMREAD_COLOR)
        template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)

        # Try different scales for the template (multi-scale matching)
        for scale in np.linspace(0.7, 1.3, 10):  # Scale range from 70% to 130%, adjust as needed
            resized_template = cv2.resize(template_gray, None, fx=scale, fy=scale, interpolation=cv2.INTER_LINEAR)

            if resized_template.shape[1] > right_half.shape[1] or resized_template.shape[0] > right_half.shape[0]:
                continue  # Skip if resized template is larger than the screenshot

            # Perform template matching on the right half
            result = cv2.matchTemplate(right_half, resized_template, cv2.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

            # If match quality is high enough, check the coordinates
            if max_val >= threshold:
                print(f"Detected {template_path} at scale {scale} with confidence {max_val}")
                x, y = max_loc
                template_w, template_h = resized_template.shape[1], resized_template.shape[0]
                # Adjust the x-coordinate to account for cropping (right half only)
                detected_x = x + width // 2 + template_w // 2
                detected_y = y + template_h // 2

                # Check if the detected point is inside the deadzone, but only if `check_deadzone` is True
                if check_deadzone and deadzone_x1 <= detected_x <= deadzone_x2 and deadzone_y1 <= detected_y <= deadzone_y2:
                    print("Detected position is in the deadzone, ignoring...")
                    continue

                return (detected_x, detected_y)

    return None  # No match found

# Function to click on a position on the screen
def click_position(position):
    pyautogui.moveTo(position)
    pyautogui.click()

# Function to press the home and reset buttons
def press_home_and_reset(home_template, reset_template):
    # Detect and press the home button
    home_pos = detect_template([home_template], check_deadzone=False)
    if home_pos:
        print("Home button detected, clicking it...")
        click_position(home_pos)
        time.sleep(1)

    # Detect and press the reset button
    reset_pos = detect_template([reset_template], check_deadzone=False)
    if reset_pos:
        print("Reset button detected, clicking it...")
        click_position(reset_pos)
        time.sleep(1)

# Main loop
x_button_templates = [
    'images/x_button.JPG',
    'images/x_button2.JPG',
    'images/x_button3.JPG',
    'images/x_button4.JPG',
    'images/x_button5.JPG',
    'images/x_button6.JPG',
    'images/x_button7.jpg'
]  # Paths to the X button templates

arrow_button_templates = [
    'images/arrow.JPG',
    'images/arrow2.jpg',
    'images/arrow3.jpg',
    'images/arrow4.JPG'
]  # Paths to the arrow button templates

play_next_ad_template = [
    'images/button.JPG',
]  # Paths to the play next ad button templates

home_template = 'images/home_button.JPG'  # Path to home button template
reset_template = 'images/reset_button.JPG'  # Path to reset button template

# Start time tracking for detecting "play next ad" button
start_time = time.time()

while True:
    # Try to detect any of the arrow button variants first
    arrow_pos = detect_template(arrow_button_templates, check_deadzone=True)

    # If an arrow button is detected, click it and wait 3 seconds
    if arrow_pos:
        print("Arrow detected, clicking it...")
        click_position(arrow_pos)
        time.sleep(3)  # Wait for 3 seconds after clicking the arrow

    # Try to detect any of the X button variants next
    x_button_pos = detect_template(x_button_templates, check_deadzone=True)

    # If an X button is detected, click it
    if x_button_pos:
        print("X button detected, closing the ad...")
        click_position(x_button_pos)

    # Try to detect any of the play next ad buttons without checking the deadzone
    nextad_button_pos = detect_template(play_next_ad_template, check_deadzone=False)

    # If a "next ad" button is detected, click it and reset the timer
    if nextad_button_pos:
        print("Next ad button detected, clicking the button...")
        click_position(nextad_button_pos)
        start_time = time.time()  # Reset the timer since the button was found

    # Check if 30 seconds have passed without detecting the "next ad" button
    if time.time() - start_time >= 30:
        print("30 seconds passed without detecting the play next ad button, pressing home and reset buttons...")
        press_home_and_reset(home_template, reset_template)
        start_time = time.time()  # Reset the timer after pressing the buttons

    # Wait before checking again (adjust as needed)
    time.sleep(1)
