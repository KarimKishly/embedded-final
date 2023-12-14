import cv2
import matplotlib.pyplot as plt
import numpy as np
import time

RED = 0
BLUE = 1
GREEN = 2

def test_image(color, img_index, img_type):
    # cap = cv2.VideoCapture(0)
    while(1):
        # _, frame = cap.read()
        time.sleep(1)
        frame = cv2.imread(f"actual_boxes/angle{str(img_index)}.{img_type}")
        frame = cv2.resize(frame, (640, 480), interpolation=cv2.INTER_AREA)
        
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        if color == RED:
            mask1 = cv2.inRange(hsv, np.array([0, 100, 20]), np.array([10, 255, 255]))
            mask2 = cv2.inRange(hsv, np.array([160, 100, 20]), np.array([255, 255, 255]))
            mask = cv2.bitwise_xor(mask1, mask2)
        if color == GREEN:
            mask = cv2.inRange(hsv, np.array([30, 100, 20]), np.array([100, 255, 255]))
        if color == BLUE:
            mask = cv2.inRange(hsv, np.array([80, 100, 20]), np.array([115, 255, 255]))
        res = cv2.bitwise_and(frame,frame, mask= mask)
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        filtered_contours = [cnt for cnt in contours if cv2.contourArea(cnt) > 4500]

        box_center = -1
        try:
            filtered_contours.sort(key=lambda cnt: cv2.contourArea(cnt), reverse=True)
            
            rect = cv2.minAreaRect(filtered_contours[0])
            box = cv2.boxPoints(rect)
            box = np.intp(box)
            cv2.drawContours(frame,[box],0,(0,0,255),2)        
            M = cv2.moments(filtered_contours[0])
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            box_center = (cX, cY)
        except:
            pass
        
        res, mask, x_center_difference = detect_notch_line(hsv, frame, mask, res, box_center)
        if x_center_difference is None:
            print("black line or box not found")
        elif x_center_difference < -3:
            print("tilted left")
        elif x_center_difference > 3:
            print("tilted right")
        else:
            print("centered")
        
        mask_3 = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
        stacked = np.hstack((mask_3,frame,res))
        cv2.imshow('Result',cv2.resize(stacked,None,fx=0.8,fy=0.8))
        k = cv2.waitKey(1) & 0xFF
        if k == 27:
            break
    cv2.destroyAllWindows()
    # cap.release()


def detect_notch_line(hsv, frame, og_mask, og_res, box_center):
    mask = cv2.inRange(hsv, np.array([0, 0, 0]), np.array([180, 255, 100]))
    res = cv2.bitwise_and(frame,frame, mask= mask)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    filtered_contours = [cnt for cnt in contours if cv2.contourArea(cnt) > 10]
    line_notch_center = -1
    try:
        filtered_contours.sort(key=lambda cnt: cv2.contourArea(cnt), reverse=True)
        
        rect = cv2.minAreaRect(filtered_contours[0])
        box = cv2.boxPoints(rect)
        box = np.intp(box)
        cv2.drawContours(frame,[box],0,(0,255,0),2)
        M = cv2.moments(filtered_contours[0])
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
        line_notch_center = (cX, cY)
    except:
        pass
    
    res = cv2.bitwise_or(res, og_res)
    mask = cv2.bitwise_or(mask, og_mask)
    
    if line_notch_center != -1 and box_center != -1:
        return res, mask, line_notch_center[0] - box_center[0]
    else:
        return res, mask, None

if __name__ == "__main__":
    test_image(GREEN, img_index=6, img_type="jpg")