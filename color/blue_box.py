import cv2
import numpy as np
from camera import take_picture_from_camera

def detect_blue_box():
    # Read the image
    image = cv2.imread(take_picture_from_camera())

    # Convert the image to the HSV color space
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Define the lower and upper ranges for the blue color
    lower_blue = np.array([90, 50, 50])
    upper_blue = np.array([130, 255, 255])

    # Threshold the image to get only the blue color
    mask = cv2.inRange(hsv, lower_blue, upper_blue)

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

        return x
        # Display the image with the bounding box
        #cv2.imshow("Largest Blue Object", image)
        #cv2.waitKey(0)
        #cv2.destroyAllWindows()
    else:
        print("No blue object found in the image.")
        return -1