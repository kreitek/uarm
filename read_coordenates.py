#!/bin/env python3

from Uarm import Uarm
from sys import platform

if platform == "win32":
    arm = Uarm('COM7')
else:
    arm = Uarm('/dev/ttyACM0', debug=True)

arm.attach_all(False) # Let you move the arm freely
arm.report_pos(3) # Prints the coorinates every 3 seconds

input("PRESS ENTER TO EXIT")
arm.close()
