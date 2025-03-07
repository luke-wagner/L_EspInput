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

    if joystick_right_held():
        print("RIGHT")
        write_led(2, 1)
    else:
        write_led(2, 0)

    if joystick_left_held():
        print("LEFT")
        write_led(3, 1)
    else:
        write_led(3, 0)
    
    if joystick_down_held():
        print("DOWN")
        write_led(0, 1)
    else:
        write_led(0, 0)

    if joystick_up_held():
        print("UP")
        write_led(1, 1)
    else:
        write_led(1, 0)

    time.sleep(0.1)
