# File: ledcontrols.py
# Author: Luke Wagner
# 3/13/2025
#
# High level functions for controlling the LEDs - uses functions from input.py

import time
import uasyncio as asyncio

import espinput.input as input

def all_on():
    input.write_led(1, 1)
    input.write_led(2, 1)
    input.write_led(3, 1)

def all_off():
    input.write_led(1, 0)
    input.write_led(2, 0)
    input.write_led(3, 0)

async def show_loading():
    global loading
    loading = True

    while loading == True:
        input.write_led(1, 1)
        input.write_led(2, 0)
        input.write_led(3, 0)
        await(asyncio.sleep(0.3))
        input.write_led(1, 0)
        input.write_led(2, 1)
        input.write_led(3, 0)
        await(asyncio.sleep(0.3))
        input.write_led(1, 0)
        input.write_led(2, 0)
        input.write_led(3, 1)
        await(asyncio.sleep(0.3))

    all_off()

async def interrupt_loading(loading_task):
    global loading
    loading = False
    await loading_task
        

async def flash_twice():
    for i in range(2):
        all_on()
        await(asyncio.sleep(0.25))
        all_off()
        await(asyncio.sleep(0.25))

async def power_down_anim():
    input.write_led(3, 1)
    input.write_led(2, 0)
    input.write_led(1, 0)
    await(asyncio.sleep(0.3))
    input.write_led(3, 0)
    input.write_led(2, 1)
    input.write_led(1, 0)
    await(asyncio.sleep(0.3))
    input.write_led(3, 0)
    input.write_led(2, 0)
    input.write_led(1, 1)
    await(asyncio.sleep(0.3))
    input.write_led(3, 0)
    input.write_led(2, 0)
    input.write_led(1, 0)


# Simulate a load process on the device
# Start by showing a loading animation
# After 5 seconds, stop the load animation and flash the LEDs twice (signal connected)
async def main():
    loading_task = asyncio.create_task(show_loading())
    for i in range(5):
        print("Waiting...")
        await(asyncio.sleep(1))
    await interrupt_loading(loading_task)
    await flash_twice()


if __name__ == "__main__":
    asyncio.run(main())