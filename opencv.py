import cv2
import numpy as np

def detect_red_objects(image_path):
    # Load the image
    image = cv2.imread(image_path)

    # Define the grid size
    grid_rows = 3
    grid_cols = 3

    # Calculate the grid cell size
    height, width, _ = image.shape
    cell_height = height // grid_rows
    cell_width = width // grid_cols

    # Convert the image from BGR to HSV color space
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Define the lower and upper bounds for the red color range
    lower_red = np.array([0, 100, 100])
    upper_red = np.array([10, 255, 255])
    lower_red2 = np.array([160, 100, 100])
    upper_red2 = np.array([179, 255, 255])

    # Create a mask based on the red color range
    mask_red = cv2.inRange(hsv, lower_red, upper_red)
    mask_red2 = cv2.inRange(hsv, lower_red2, upper_red2)
    mask_red_combined = cv2.bitwise_or(mask_red, mask_red2)

    # Initialize variables to track the zone with the most red
    max_red_count = 0
    max_red_zone = None

    # Iterate over each zone in the grid
    for row in range(grid_rows):
        for col in range(grid_cols):
            # Calculate the coordinates for the current zone
            top = row * cell_height
            bottom = (row + 1) * cell_height
            left = col * cell_width
            right = (col + 1) * cell_width

            # Extract the zone from the combined red mask
            zone = mask_red_combined[top:bottom, left:right]

            # Count the number of red pixels in the zone
            red_count = cv2.countNonZero(zone)

            # Check if the current zone has more red pixels than the previous maximum
            if red_count > max_red_count:
                max_red_count = red_count
                max_red_zone = (row, col)

    # Display the original image and the red objects
    #cv2.imshow("Original Image", image)
    #cv2.imshow("Red Objects", mask_red_combined)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()

    # Print the zone with the most red
    if max_red_zone is not None:
        print(f"{max_red_zone[0]*3 + max_red_zone[1] + 1}")
        return max_red_zone[0] * 3 + max_red_zone[1] + 1
    else:
        print("No red objects detected.")
        return -1