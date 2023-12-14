# from picamera import PiCamera
# from time import sleep
import cv2

def takePicture():
    dir = "/home/admin/Desktop/pic.jpg"
    # camera = PiCamera()
    # camera.start_preview(alpha=192)
    # sleep(1)
    # camera.capture(dir)
    return dir

def take_picture_from_camera():
    # Open the camera
    cap = cv2.VideoCapture(0)  # 0 represents the default camera

    # Check if the camera is opened successfully
    if not cap.isOpened():
        print("Failed to open the camera")
        return

    # Capture a frame from the camera
    ret, frame = cap.read()

    # Check if the frame was captured successfully
    if not ret:
        print("Failed to capture frame")
        return

    # Save the captured frame as an image
    cv2.imwrite("C:/Projects/embedded-final/resources/captured_img.jpg", frame)

    # Release the camera
    cap.release()

    return "C:/Projects/embedded-final/resources/captured_img.jpg"
    #print("Picture taken successfully")

# Call the function to take a picture
if __name__ == '__main__':
    take_picture_from_camera()