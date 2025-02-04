from machine import Pin

led0 = Pin(2, Pin.OUT)  # Onboard LED
led1 = Pin(25, Pin.OUT) # External LED 1
led2 = Pin(26, Pin.OUT) # External LED 2

leds = [led0, led1, led2]

button0 = Pin(4, Pin.IN)
button1 = Pin(16, Pin.IN)
button2 = Pin(17, Pin.IN)
button3 = Pin(5, Pin.IN)
button4 = Pin(18, Pin.IN)
button5 = Pin(19, Pin.IN)

buttons = [button0, button1, button2, button3, button4, button5]

def button_pressed(num):
    button = buttons[num]
    return button.value() == 1

def write_led(num, value):
    led = leds[num]
    led.value(value)
