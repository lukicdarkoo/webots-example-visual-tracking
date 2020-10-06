from controller import Robot, Motor

TIME_STEP = 64

# create the Robot instance.
robot = Robot()

# get the motor devices
leftMotor = robot.getMotor('left wheel motor')
rightMotor = robot.getMotor('right wheel motor')
# set the target position of the motors
leftMotor.setPosition(10.0)
rightMotor.setPosition(10.0)

while robot.step(TIME_STEP) != -1:
   pass
