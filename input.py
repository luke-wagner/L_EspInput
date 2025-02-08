from machine import Pin

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

# Joystick control? - TBD

# UNUSED: GPIO17, GPIO22, GPIO23

#--------------------------------------------------------------------
### RIGHT SIDE

# 4 larger pushbuttons
button2 = Pin(26, Pin.IN)
button3 = Pin(25, Pin.IN)
button4 = Pin(33, Pin.IN)
button5 = Pin(32, Pin.IN)

# UNUSED: GPIO13, GPIO14, GPIO27

#--------------------------------------------------------------------

leds = [led0, led1, led2, led3]

buttons = [button0, button1, button2, button3, button4, button5]

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