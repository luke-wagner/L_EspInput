# File: iotest.py
# Author: Luke Wagner
# 2/8/2025
#
# Tests all button inputs and joystick controls
# Sets LEDs as output from tests

import time

from espinput.iodefs import *

button_count = button_count()
led_count = led_count()

while True:
    any_button_pressed = False

    for i in range(button_count):
        if button_pressed(i):
            any_button_pressed = True
            print("Button %d pressed" % i)
    
    if (any_button_pressed or joystick_left_held() or joystick_right_held or 
    joystick_up_held or joystick_down_held()):
        for i in range(led_count):
            write_led(i, 1) # Turn on all LEDs
    else:
        for i in range(led_count):
            write_led(i, 0) # Turn off all LEDs
    
    time.sleep(0.1)
