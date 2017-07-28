#!/usr/bin/env python3

from Uarm import Uarm
from sys import platform

if platform == "win32":
    arm = Uarm('COM7', baudrate=115200)
else:
    arm = Uarm('/dev/ttyACM0')

print(dir(arm))

arm.mode(0)  # default mode for pump or gripper

arm.move(0, 0, 0)  # Move to an absolute x, y, z position

arm.speed = 2000  # set the default speed from now on

arm.move(50, 75, -25)  # Move to an absolute x, y, z position

arm.pump(True)
# arm.gripper(True)

arm.pause(3)

arm.pump(False)
# arm.gripper(False)

arm.moverel(-50, 0, 0)  # Move to a relative x, y, z position

# arm.sendraw("G2204 X0 Y0 Z50 F1000") # send custom gcode

print("Current speed: ", arm.speed)
print("Last index: ", arm.index)
input("press any key to disconect")
arm.close()
