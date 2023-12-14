# from picamera import PiCamera
# from time import sleep
import cv2

class Pc_Cam:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
    
    def get_cap(self):
        return self.cap
    
    def take_picture_from_camera(self):
        # Check if the camera is opened successfully
        if not self.cap.isOpened():
            print("Failed to open the camera")
            return
        
        # Capture a frame from the camera
        ret, frame = self.cap.read()
        
        print(frame.shape)
        
        # Check if the frame was captured successfully
        if not ret:
            print("Failed to capture frame")
            return
        
        # Save the captured frame as an image
        cv2.imwrite(".\captured_images\captured_image.jpg", frame)
        
        return ".\captured_images\captured_image.jpg"
        #print("Picture taken successfully")    

class Rp_Cam():
#     def __init__(self):
#         cam = PiCamera()
#         cam.start_preview(alpha=192)
        
    def take_picture_from_camera(self):
        dir = "/home/admin/Desktop/pic.jpg"
        # sleep(1)
        self.cam.capture(dir)
        return dir

# Call the function to take a picture
if __name__ == '__main__':
    cam = Pc_Cam()
    import time
    while True:
        time.sleep(0.1)
        cam.take_picture_from_camera()