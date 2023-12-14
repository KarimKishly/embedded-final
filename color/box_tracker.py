from color.Color import Color
import cv2
import numpy as np
from camera import take_picture_from_camera

def detect_box_center(color: Color) -> int:
    # Read the image
    image = cv2.imread(take_picture_from_camera())

    # Convert the image to the HSV color space
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Define the lower and upper ranges for the red color
    if color == Color.RED:
        lower_color_bound = np.array([0, 50, 50])
        upper_color_bound = np.array([10, 255, 255])
    if color == Color.GREEN:
        lower_color_bound = np.array([40, 50, 50])
        upper_color_bound = np.array([80, 255, 255])
    if color == Color.BLUE:
        lower_color_bound = np.array([90, 50, 50])
        upper_color_bound = np.array([130, 255, 255])

    # Threshold the image to get only the desired color
    mask = cv2.inRange(hsv, lower_color_bound, upper_color_bound)

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
        #cv2.imshow("Largest Desired Color Object", image)
        #cv2.waitKey(0)
        #cv2.destroyAllWindows()
        return x

    else:
        print("No desired object found in the image.")
        return -1

if __name__ == '__main__':
    detect_box_center(Color.RED)