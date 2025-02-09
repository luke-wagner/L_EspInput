# File: adctest.py
# Author: Luke Wagner
# 2/8/2025
#
# Tests horizontal and vertical joystick values

import time

from espinput.input import *

while True:
    vert_value = vert.read()
    horiz_value = horiz.read()
    
    print("V: " + str(vert_value))
    print("H: " + str(horiz_value) + "\n")
    time.sleep(0.5)
