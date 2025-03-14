# File: LEDController.py
# Author: Luke Wagner
# 3/13/2025
#
# LEDController class implements high-level functions for controlling the board's LEDs
# -- LED functions run in parallel, and only one can run at a time.
# -- Whenever a LED function is called from the main thread, the current function is interrupted, and the new one starts execution.
# -- Uses low-level functions from input.py for control of LEDs
#
# Example usage in main() function below
#

import uasyncio as asyncio

from espinput.input import write_led

class LEDController:
    def __init__(self):
        self.current_task = None
        self.current_func_name = None
        self.loop = asyncio.get_event_loop()
        
        # Start the watcher task
        self.loop.create_task(self._watcher_task())
        
        # Queue of pending functions to run
        self._pending_func = None
        self._pending_args = None
        self._pending_kwargs = None
    
    async def _watcher_task(self):
        """Task that monitors for new function requests and handles interruptions"""
        while True:
            # Check if there's a pending function to run
            if self._pending_func is not None:
                # Cancel the current task if it exists
                if self.current_task is not None:
                    try:
                        self.current_task.cancel()
                        # Wait a short time for cancellation to take effect
                        await asyncio.sleep_ms(50)
                    except Exception as e:
                        print(f"Error cancelling task: {e}")
                
                # Start the new function
                func = self._pending_func
                args = self._pending_args
                kwargs = self._pending_kwargs
                self.current_func_name = func.__name__
                
                # Clear the pending function info
                self._pending_func = None
                self._pending_args = None
                self._pending_kwargs = None
                
                # Create a new task for the function
                self.current_task = self.loop.create_task(self._run_function(func, args, kwargs))
            
            # Yield to allow other tasks to run
            await asyncio.sleep_ms(10)
    
    async def _run_function(self, func, args, kwargs):
        """Run a function and handle any exceptions"""
        try:
            await func(*args, **kwargs)
            print(f"Function {self.current_func_name} completed")
        except asyncio.CancelledError:
            print(f"Function {self.current_func_name} was interrupted")
        except Exception as e:
            print(f"Error in {self.current_func_name}: {e}")
        finally:
            if self.current_func_name == func.__name__:
                self.current_func_name = None
                self.current_task = None
    
    def call_function(self, func, *args, **kwargs):
        """Queue a function to run, interrupting any current function"""
        # Store the function and arguments to be picked up by the watcher
        self._pending_func = func
        self._pending_args = args
        self._pending_kwargs = kwargs
        
        # Return immediately (non-blocking)
        return True
    
    # Wrapper functions for calling through the control manager
    def all_on(self):
        return self.call_function(self.__all_on)
    
    def all_off(self):
        return self.call_function(self.__all_off)
    
    def show_loading(self):
        return self.call_function(self.__show_loading)
    
    def flash_twice(self):
        return self.call_function(self.__flash_twice)
    
    def power_down_anim(self):
        return self.call_function(self.__power_down_anim)
    

    #############################################################################
    ## The LED Functions:
    ## Invisible outside this file. Must create a public wrapper function above
    ##  for any new functions.
    #############################################################################

    async def __all_on(self):
        write_led(1, 1)
        write_led(2, 1)
        write_led(3, 1)

    async def __all_off(self):
        write_led(1, 0)
        write_led(2, 0)
        write_led(3, 0)

    async def __show_loading(self):
        while True:
            write_led(1, 1)
            write_led(2, 0)
            write_led(3, 0)
            await(asyncio.sleep(0.3))
            write_led(1, 0)
            write_led(2, 1)
            write_led(3, 0)
            await(asyncio.sleep(0.3))
            write_led(1, 0)
            write_led(2, 0)
            write_led(3, 1)
            await(asyncio.sleep(0.3))
            
    async def __flash_twice(self):
        await self.__all_off()
        await (asyncio.sleep(0.25))

        for i in range(2):
            await self.__all_on()
            await(asyncio.sleep(0.25))
            await self.__all_off()
            await(asyncio.sleep(0.25))

    async def __power_down_anim(self):
        write_led(3, 1)
        write_led(2, 0)
        write_led(1, 0)
        await(asyncio.sleep(0.3))
        write_led(3, 0)
        write_led(2, 1)
        write_led(1, 0)
        await(asyncio.sleep(0.3))
        write_led(3, 0)
        write_led(2, 0)
        write_led(1, 1)
        await(asyncio.sleep(0.3))
        write_led(3, 0)
        write_led(2, 0)
        write_led(1, 0)


# Example usage: Simulate a load process on the device
# 1. Start by showing a loading animation
# 2. After 5 seconds, stop the load animation and flash the LEDs twice (signal connected)
async def main():
    controller = LEDController()
    controller.show_loading()
    for i in range(5):
        print("Waiting...")
        await(asyncio.sleep(1))
    controller.flash_twice()
    await(asyncio.sleep(3)) # wait for flash_twice() to finish, TODO: Make all functions awaitable

if __name__ == "__main__":
    asyncio.run(main())
