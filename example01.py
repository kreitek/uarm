#!/usr/bin/env python3

from Uarm import Uarm
from sys import platform

if platform == "win32":
    arm = Uarm('COM7', baudrate = 9600)
else:
    arm = Uarm('/dev/pts/1')
arm.move(10, 20, 30)
arm.move(100, 200, 300)
arm.move(1000, 2000, 3000)
arm.speed = 4500
print("Current speed: ", arm.speed)
print("Last index: ", arm.index)
arm.close()
