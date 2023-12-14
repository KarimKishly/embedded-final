from object_logic.Color import Color
import cv2
import numpy as np
from camera import Pc_Cam, Rp_Cam

cam = Pc_Cam()

def detect_object(color: Color, img_index:int=None) -> int:
    # Read the image
    if img_index is not None:
        image = cv2.imread(f"actual_boxes/angle{str(img_index)}.jpg")
    else:
        image = cv2.imread(cam.take_picture_from_camera())

    # Convert the image to the HSV color space
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Define the lower and upper ranges for the red color
    if color == Color.RED:
        mask1 = cv2.inRange(hsv, np.array([0, 100, 20]), np.array([10, 255, 255]))
        mask2 = cv2.inRange(hsv, np.array([160, 100, 20]), np.array([255, 255, 255]))
        mask = cv2.bitwise_xor(mask1, mask2)
    if color == Color.GREEN:
        mask = cv2.inRange(hsv, np.array([30, 100, 20]), np.array([100, 255, 255]))
    if color == Color.BLUE:
        mask = cv2.inRange(hsv, np.array([80, 100, 20]), np.array([115, 255, 255]))

    # Find contours in the mask
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    # Filter contours based on their area
    filtered_contours = [cnt for cnt in contours if cv2.contourArea(cnt) > 4500]

    # Sort the filtered contours based on their area in descending order
    filtered_contours.sort(key=lambda cnt: cv2.contourArea(cnt), reverse=True)
    try:
        # Get the largest contour
        largest_contour = filtered_contours[0]
        
        # Get the bounding box coordinates around the largest contour
        # x, y, w, h = cv2.boundingRect(largest_contour)
        
        # cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
        
        rect = cv2.minAreaRect(largest_contour)
        box = cv2.boxPoints(rect)
        box = np.intp(box)
        cv2.drawContours(image,[box],0,(0,0,255),2)
        
        
        cv2.imshow("Largest Desired Color Object", image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        return rect.center
    except:
        print("No desired object found in the image.")
        return -1




if __name__ == '__main__':
    detect_object(Color.RED)

