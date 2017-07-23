#!/usr/bin/env python3

from Uarm import Uarm
from sys import platform

if platform == "win32":
    brazo = Uarm('COM7', baudrate = 9600)
else:
    brazo = Uarm('/dev/tty0', baudrate = 9600)
brazo.move(10, 20, 30)
brazo.move(100, 200, 300)
brazo.move(1000, 2000, 3000)
brazo.speed = 4500
velocidad = brazo.speed
print(str(velocidad))
brazo.close()
