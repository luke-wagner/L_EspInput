# File: input.py
# Author: Luke Wagner
# 2/8/2025
#
# Contains all input/output definitions for the ESP32

import micropython
from machine import Pin, ADC
import uasyncio as asyncio

### Constants
V_LOW_THRESHOLD = 500
V_HIGH_THRESHOLD = 3595
H_LOW_THRESHOLD = 500
H_HIGH_THRESHOLD = 3595

### Interrupt events   ##############################################
btn0_event = ("btn0_event", asyncio.Event())
btn1_event = ("btn1_event", asyncio.Event())

interrupt_events = [btn0_event, btn1_event]

### Interrupt handlers ##############################################
def _button0_handler(pin):
    btn0_event[1].set()    # Set this event to be handled in the main code

def _button1_handler(pin):
    btn1_event[1].set()    # Set this event to be handled in the main code

def button0_isr(pin):
    # We want to keep the actual ISR as short as possible.
    # Using a scheduler to handle the main code of the event
    micropython.schedule(_button0_handler, pin)

def button1_isr(pin):
    # We want to keep the actual ISR as short as possible.
    # Using a scheduler to handle the main code of the event
    micropython.schedule(_button1_handler, pin)

### I/O #############################################################
# ALL PIN NUMBERS ARE GPIO NUMBERS!

led0 = Pin(2, Pin.OUT) # Onboard LED

### LEFT SIDE
#--------------------------------------------------------------------
# Two (small) pushbuttons
button0 = Pin(4, Pin.IN) # Power button
button1 = Pin(16, Pin.IN) # Reset button

button0.irq(trigger=Pin.IRQ_FALLING, handler=button0_isr)
button1.irq(trigger=Pin.IRQ_FALLING, handler=button1_isr)

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

def joystick_left_held():
    return horiz.read() < H_LOW_THRESHOLD

def joystick_right_held():
    return horiz.read() > H_HIGH_THRESHOLD

def joystick_up_held():
    return vert.read() > V_HIGH_THRESHOLD

def joystick_down_held():
    return vert.read() < V_LOW_THRESHOLD