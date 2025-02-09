# File: input.py
# Author: Luke Wagner
# 2/8/2025
#
# Contains all input/output definitions for the ESP32

from machine import Pin, ADC

### I/O #############################################################
# ALL PIN NUMBERS ARE GPIO NUMBERS!

led0 = Pin(2, Pin.OUT) # Onboard LED

### LEFT SIDE
#--------------------------------------------------------------------
# Two (small) pushbuttons
button0 = Pin(4, Pin.IN)
button1 = Pin(16, Pin.IN)

# LEDs
led1 = Pin(18, Pin.OUT)
led2 = Pin(19, Pin.OUT)
led3 = Pin(21, Pin.OUT)

# Joystick: Button-press
button6 = Pin(17, Pin.IN)

# UNUSED: GPIO22, GPIO23

#--------------------------------------------------------------------
### RIGHT SIDE

# Joystick: Vertical and Horizontal
vert = ADC(Pin(32)) # ADC1_4
vert.atten(ADC.ATTN_11DB)       #Full range: 3.3v
horiz = ADC(Pin(33)) # ADC1_5
horiz.atten(ADC.ATTN_11DB)       #Full range: 3.3v

# 4 larger pushbuttons
button2 = Pin(14, Pin.IN)
button3 = Pin(27, Pin.IN)
button4 = Pin(26, Pin.IN)
button5 = Pin(25, Pin.IN)

# UNUSED: GPIO13

#--------------------------------------------------------------------

leds = [led0, led1, led2, led3]

buttons = [button0, button1, button2, button3, button4, button5, button6]

def button_pressed(num):
    try:
        button = buttons[num]
    except:
        button = None
    
    if button is not None:
        return button.value() == 1
    else:
        return False

def write_led(num, value):
    try:
        led = leds[num]
    except:
        led = None
        
    if led is not None:
        led.value(value)