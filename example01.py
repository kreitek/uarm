#!/usr/bin/env python3

from Uarm import Uarm

brazo = Uarm('COM7', baudrate = 9600)
brazo.move(10, 20, 30)
brazo.move(100, 200, 300)
brazo.move(1000, 2000, 3000)
brazo.set_speed(4500)
velocidad = brazo.get_speed()
print(str(velocidad))
brazo.close()


