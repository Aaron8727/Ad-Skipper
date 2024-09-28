import cv2
import numpy as np
from PIL import ImageGrab

# Capture the screen
screenshot = ImageGrab.grab()
screenshot_np = np.array(screenshot)

# Convert to OpenCV format (BGR)
screenshot_cv = cv2.cvtColor(screenshot_np, cv2.COLOR_RGB2BGR)

# Example: drawing a rectangle at a known position
# Replace with the actual coordinates of your deadzone once determined
cv2.rectangle(screenshot_cv, (0, 0), (1800, 1080), (0, 255, 0), 2)  # Draw green rectangle

# Show the screenshot with the rectangle
cv2.imshow('Screenshot with Deadzone', screenshot_cv)
cv2.waitKey(0)
cv2.destroyAllWindows()
