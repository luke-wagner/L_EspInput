import time

from espinput.input import *

button_count = len(buttons)
led_count = len(leds)

while True:
    any_button_pressed = False

    for i in range(button_count):
        if button_pressed(i):
            any_button_pressed = True
            print("Button %d pressed" % i)
    
    if any_button_pressed:
        for i in range(led_count):
            write_led(i, 1) # Turn on all LEDs
    else:
        for i in range(led_count):
            write_led(i, 0) # Turn off all LEDs
    
    time.sleep(0.1)