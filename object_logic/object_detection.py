from object_logic.Color import Color
import cv2
import numpy as np
from camera import Pc_Cam, Rp_Cam

cam = Rp_Cam()
cap = cam.cam

def detect_object(color: Color, min_area=None, max_area=None, img_index:int=None) -> int:
    if min_area is None:
        min_area = 4500
    if max_area is None:
        max_area = 300000
    for frame in cap.capture_continuous(cam.take_picture_from_camera(), format="bgr", use_video_port=True):
        image = frame.array
        # Read the image
        # if img_index is not None:
        #     image = cv2.imread(f"actual_boxes/angle{str(img_index)}.jpg")
        # else:
        #     image = cv2.imread(cam.take_picture_from_camera())

        # Convert the image to the HSV color space
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        # Define the lower and upper ranges for the red color
        if color == Color.RED:
            mask1 = cv2.inRange(hsv, np.array([0, 100, 20]), np.array([0, 255, 255]))
            mask2 = cv2.inRange(hsv, np.array([160, 100, 20]), np.array([190, 255, 255]))
            mask = cv2.bitwise_xor(mask1, mask2)
        if color == Color.GREEN:
            mask = cv2.inRange(hsv, np.array([30, 100, 20]), np.array([70, 255, 255]))
        if color == Color.BLUE:
            mask = cv2.inRange(hsv, np.array([80, 100, 20]), np.array([115, 255, 255]))
        if color == Color.BLACK:
                mask = cv2.inRange(hsv, np.array([50, 0, 0]), np.array([180, 260, 50]))
                #### Pixelation
                height, width = mask.shape[:2]
                w, h = (64, 64)
                temp = cv2.resize(mask, (w, h), interpolation=cv2.INTER_LINEAR)
                mask = cv2.resize(temp, (width, height), interpolation=cv2.INTER_NEAREST)
                ####

        # Find contours in the mask
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

        # Filter contours based on their area
        filtered_contours = [cnt for cnt in contours if (max_area > cv2.contourArea(cnt) > min_area)]

        # Sort the filtered contours based on their area in descending order
        filtered_contours.sort(key=lambda cnt: cv2.contourArea(cnt), reverse=True)
        if(len(filtered_contours) > 0):
            largest_contour = filtered_contours[0]
            rect = cv2.minAreaRect(largest_contour)
            box = cv2.boxPoints(rect)
            box = np.intp(box)
            cv2.drawContours(image,[box],0,(0,0,255),2)
            M = cv2.moments(box)
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            center = (cX, cY)
            area = cv2.contourArea(box)
        else:
            print("No desired object found in the image.")
            center = (-1, -1)
            area = -1
        mask_3 = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
        stacked = np.hstack((mask_3,image))
        cv2.imwrite('./captured_images/Result2.jpg',cv2.resize(stacked,None,fx=0.8,fy=0.8))
        
        return center[0], center[1], area
            
        



if __name__ == '__main__':
    detect_object(Color.RED)

