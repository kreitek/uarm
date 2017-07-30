#!/usr/bin/env python3

from Uarm import Uarm
from sys import platform

if platform == "win32":
    arm = Uarm('COM7', baudrate=115200)
else:
    arm = Uarm('/dev/ttyACM0', debug=True)

arm.speed = 7000  # set the default speed from now on

if False:  # Test
    arm.move(180, 180, 30)  # Move to an absolute x, y, z position
    arm.pause(1)
    arm.move(180, -180, 30)  # Move to an absolute x, y, z position
    arm.pause(1)
    arm.move(255, 0, 150)  # Move to an absolute x, y, z position
    arm.pause(1)
    arm.move(150, 0, 30)  # Move to an absolute x, y, z position

if False:
    # arm.mode(0)  # default mode for pump or gripper
    arm.move(150, 0, 70)  # Move to an absolute x, y, z position
    arm.pause(1)
    arm.pump(True)
    # arm.gripper(True)
    arm.pause(1)
    arm.moverel(0,70,0)
    arm.pause(1)
    arm.pump(False)
    # arm.gripper(False)
    arm.move(150, 0, 70)

if True: # goes down until reach some object
    # arm.mode(0)  # default mode for pump or gripper
    arm.move(150, 0, 100)  # Move to an absolute x, y, z position
    arm.pumpswitch(True)
    arm.moverel(0, 0, +50)
    arm.pause(1)
    arm.moverel(0, 70, 0)
    arm.pause(1)
    arm.wrist(125)
    arm.moverel(0, 0, -40)
    arm.pumpswitch(False)
    arm.pause(1)
    arm.moverel(0, 0, +50)
    arm.wrist(90)
    arm.move(150, 0, 70)

# arm.sendraw("G2204 X0 Y0 Z50 F1000") # send custom gcode

print("Current speed: ", arm.speed)
print("Last index: ", arm.index)
input("press any key to disconect")
arm.close()
