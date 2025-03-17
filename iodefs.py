# File: iodefs.py
# Author: Luke Wagner
# 2/8/2025
#
# Contains low-level I/O definitions for direct access to board I/O

import micropython
from machine import Pin, ADC
import uasyncio as asyncio

### Constants
V_LOW_THRESHOLD = 500
V_HIGH_THRESHOLD = 3595
H_LOW_THRESHOLD = 500
H_HIGH_THRESHOLD = 3595

### Interrupt events   ##############################################
__btn0_event = ("__btn0_event", asyncio.Event())
__btn1_event = ("__btn1_event", asyncio.Event())

__interrupt_events = [__btn0_event, __btn1_event]

### Interrupt handlers ##############################################
def __button0_handler(pin):
    __btn0_event[1].set()    # Set this event to be handled in the main code

def __button1_handler(pin):
    __btn1_event[1].set()    # Set this event to be handled in the main code

def __button0_isr(pin):
    # We want to keep the actual ISR as short as possible.
    # Using a scheduler to handle the main code of the event
    micropython.schedule(__button0_handler, pin)

def __button1_isr(pin):
    # We want to keep the actual ISR as short as possible.
    # Using a scheduler to handle the main code of the event
    micropython.schedule(__button1_handler, pin)

### I/O #############################################################
# ALL PIN NUMBERS ARE GPIO NUMBERS!

__led0 = Pin(2, Pin.OUT) # Onboard LED

### LEFT SIDE
#--------------------------------------------------------------------
# Two (small) pushbuttons
__button0 = Pin(4, Pin.IN) # Power button
__button1 = Pin(16, Pin.IN) # Reset button

__button0.irq(trigger=Pin.IRQ_FALLING, handler=__button0_isr)
__button1.irq(trigger=Pin.IRQ_FALLING, handler=__button1_isr)

# LEDs
__led1 = Pin(18, Pin.OUT)
__led2 = Pin(19, Pin.OUT)
__led3 = Pin(21, Pin.OUT)

# Joystick: Button-press
__button6 = Pin(17, Pin.IN)

# UNUSED: GPIO22, GPIO23

#--------------------------------------------------------------------
### RIGHT SIDE

# Joystick: Vertical and Horizontal
__vert = ADC(Pin(32)) # ADC1_4
__vert.atten(ADC.ATTN_11DB)       #Full range: 3.3v
__horiz = ADC(Pin(33)) # ADC1_5
__horiz.atten(ADC.ATTN_11DB)       #Full range: 3.3v

# 4 larger pushbuttons
__button2 = Pin(14, Pin.IN)
__button3 = Pin(27, Pin.IN)
__button4 = Pin(26, Pin.IN)
__button5 = Pin(25, Pin.IN)

# UNUSED: GPIO13

#--------------------------------------------------------------------

__leds = [__led0, __led1, __led2, __led3]

__buttons = [__button0, __button1, __button2, __button3, __button4, __button5, __button6]

def led_count():
    return len(__leds)

def button_count():
    return len(__buttons)

def button_pressed(num):
    try:
        button = __buttons[num]
    except:
        button = None
    
    if button is not None:
        return button.value() == 1
    else:
        return False

def write_led(num, value):
    try:
        led = __leds[num]
    except:
        led = None
        
    if led is not None:
        led.value(value)

def joystick_left_held():
    return __horiz.read() > H_HIGH_THRESHOLD

def joystick_right_held():
    return __horiz.read() < H_LOW_THRESHOLD

def joystick_up_held():
    return __vert.read() > V_HIGH_THRESHOLD

def joystick_down_held():
    return __vert.read() < V_LOW_THRESHOLD


### Function aliases   ##############################################
power_button_pressed = button_pressed(1) # should be button_pressed(0), changed for version 1.0
power_button_event = __btn1_event        # should be __btn0_event

home_button_pressed = None               # button_pressed(1) -- leave unset for version 1.0
home_button_event = None                 # __btn1_event

select_button_pressed = button_pressed(4)