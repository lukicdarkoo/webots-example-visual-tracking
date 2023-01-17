"""This controller moves the red ball around the robot."""

from math import sin, cos, pi
from controller import Supervisor


supervisor = Supervisor()
timestep = int(supervisor.getBasicTimeStep())

ball = supervisor.getFromDef('BALL')
ball_translation = ball.getField('translation')

angle = 0
while supervisor.step(timestep) != -1:
    x = cos(angle)
    y = sin(angle)
    ball_translation.setSFVec3f([x, y, 0.2])
    
    angle += 0.01
