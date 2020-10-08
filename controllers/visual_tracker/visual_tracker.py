"""This controller makes the robot following the red ball."""

import cv2
import numpy as np
from controller import Robot


# P value for P controller
# High P value makes the robot more agressive
# Low P values makes the robot more sluggish
P_COEFFICIENT = 0.1

# Initialize the robot
robot = Robot()
timestep = int(robot.getBasicTimeStep())

# Initialize camera
camera = robot.getCamera('camera')
camera.enable(timestep)

# Initialize motors
motor_left = robot.getMotor('left wheel motor')
motor_right = robot.getMotor('right wheel motor')
motor_left.setPosition(float('inf'))
motor_right.setPosition(float('inf'))
motor_left.setVelocity(0)
motor_right.setVelocity(0)


def get_image_from_camera():
    """
    Take an image from the camera device and prepare it for OpenCV processing:
    - convert data type,
    - convert to RGB format (from BGRA), and
    - rotate & flip to match the actual image.
    """
    img = camera.getImageArray()
    img = np.asarray(img, dtype=np.uint8)
    img = cv2.cvtColor(img, cv2.COLOR_BGRA2RGB)
    img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
    return cv2.flip(img, 1)


# Main control loop
while robot.step(timestep) != -1:
    img = get_image_from_camera()

    # Segment the image by color in HSV color space
    img = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
    mask = cv2.inRange(img, np.array([50, 150, 0]), np.array([200, 230, 255]))

    # Find the largest segmented contour (red ball) and it's center
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    largest_contour = max(contours, key=cv2.contourArea)
    largest_contour_center = cv2.moments(largest_contour)
    center_x = int(largest_contour_center['m10'] / largest_contour_center['m00'])

    # Find error (ball distance from image center)
    error = camera.getWidth() / 2 - center_x

    # Use simple proportional controller to follow the ball
    motor_left.setVelocity(- error * P_COEFFICIENT)
    motor_right.setVelocity(error * P_COEFFICIENT)
