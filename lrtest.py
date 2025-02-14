# File: lrtest.py
# Author: Luke Wagner
# 2/8/2025
#
# Test deriving left and right from joystick values

import time

from espinput.input import *

while True:
    vert_value = vert.read()
    horiz_value = horiz.read()

    if horiz_value > 3595:
        print("RIGHT")
        write_led(2, 1)
    else:
        write_led(2, 0)

    if horiz_value < 500:
        print("LEFT")
        write_led(3, 1)
    else:
        write_led(3, 0)
    
    if vert_value < 500:
        print("DOWN")
        write_led(0, 1)
    else:
        write_led(0, 0)

    if vert_value > 3595:
        print("UP")
        write_led(1, 1)
    else:
        write_led(1, 0)

    time.sleep(0.1)
