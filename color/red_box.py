import cv2
import numpy as np
from camera import take_picture_from_camera

def detect_red_box():
    # Read the image
    image = cv2.imread(take_picture_from_camera())

    # Convert the image to the HSV color space
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Define the lower and upper ranges for the red color
    lower_red = np.array([0, 50, 50])
    upper_red = np.array([10, 255, 255])

    # Threshold the image to get only the red color
    mask = cv2.inRange(hsv, lower_red, upper_red)

    # Find contours in the mask
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Filter contours based on their area
    filtered_contours = [cnt for cnt in contours if cv2.contourArea(cnt) > 100]

    # Sort the filtered contours based on their area in descending order
    filtered_contours.sort(key=lambda cnt: cv2.contourArea(cnt), reverse=True)

    if filtered_contours:
        # Get the largest contour
        largest_contour = filtered_contours[0]

        # Get the bounding box coordinates around the largest contour
        x, y, w, h = cv2.boundingRect(largest_contour)

        # Draw a bounding box around the largest contour
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.imshow("Largest Red Object", image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        return x
        # Display the image with the bounding box

    else:
        print("No red object found in the image.")
        return -1