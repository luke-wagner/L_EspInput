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

from espinput.iodefs import write_led

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
        self._completion_event = None
        self._scheduling_lock = asyncio.Lock()  # Lock for thread-safe scheduling
    
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
                completion_event = self._completion_event
                self.current_func_name = func.__name__
                
                # Clear the pending function info
                self._pending_func = None
                self._pending_args = None
                self._pending_kwargs = None
                self._completion_event = None
                
                # Create a new task for the function
                self.current_task = self.loop.create_task(self._run_function(func, args, kwargs, completion_event))
            
            # Yield to allow other tasks to run
            await asyncio.sleep_ms(10)
    
    async def _run_function(self, func, args, kwargs, completion_event):
        """Run a function and handle any exceptions"""
        result = None
        try:
            result = await func(*args, **kwargs)
            print(f"Function {self.current_func_name} completed")
        except asyncio.CancelledError:
            print(f"Function {self.current_func_name} was interrupted")
        except Exception as e:
            print(f"Error in {self.current_func_name}: {e}")
        finally:
            if self.current_func_name == func.__name__:
                self.current_func_name = None
                self.current_task = None
            
            # Set the completion event if it exists
            if completion_event is not None:
                completion_event.set()
                
        return result
    
    async def schedule_function(self, func, *args, **kwargs):
        """Schedule a function to run, interrupting any current function"""
        async with self._scheduling_lock:
            #print(f"Scheduling function: {func.__name__}") # for debugging
            
            # Create an event that will be set when the function completes
            completion_event = asyncio.Event()
            
            # Store the function, arguments, and completion event
            self._pending_func = func
            self._pending_args = args
            self._pending_kwargs = kwargs
            self._completion_event = completion_event
            
            # Give the watcher task a chance to see the new function
            await asyncio.sleep_ms(20)
            
            # Return the event for awaiting if needed
            return completion_event
    
    # Wrapper functions for calling through the control manager
    # -- CALL ALL FUNCTIONS WITH await func_name(), use "wait_for_completion" param to specify 
    # --  whether to run synchronously or asynchronously.
    # -- Was previously using asyncio.create_task() to run functions asynchronously, but ran
    # --  into race conditions, as asyncio.create_task(func_name()) takes longer to initialize
    # --  than calling await func_name() directly. This was causing tasks to be scheduling in the
    # --  wrong order.
    async def all_on(self, wait_for_completion=True):
        completion_event = await self.schedule_function(self.__all_on)
        if wait_for_completion:
            await completion_event.wait()
        return completion_event
    
    async def all_off(self, wait_for_completion=True):
        completion_event = await self.schedule_function(self.__all_off)
        if wait_for_completion:
            await completion_event.wait()
        return completion_event
    
    async def show_loading(self, wait_for_completion=True):
        completion_event = await self.schedule_function(self.__show_loading)
        if wait_for_completion:
            await completion_event.wait()
        return completion_event
    
    async def flash_twice(self, wait_for_completion=True):
        completion_event = await self.schedule_function(self.__flash_twice)
        if wait_for_completion:
            await completion_event.wait()
        return completion_event
    
    async def power_down_anim(self, wait_for_completion=True):
        completion_event = await self.schedule_function(self.__power_down_anim)
        if wait_for_completion:
            await completion_event.wait()
        return completion_event

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
            await asyncio.sleep(0.3)
            write_led(1, 0)
            write_led(2, 1)
            write_led(3, 0)
            await asyncio.sleep(0.3)
            write_led(1, 0)
            write_led(2, 0)
            write_led(3, 1)
            await asyncio.sleep(0.3)
            
    async def __flash_twice(self):
        await self.__all_off()
        await asyncio.sleep(0.25)

        for i in range(2):
            await self.__all_on()
            await asyncio.sleep(0.25)
            await self.__all_off()
            await asyncio.sleep(0.25)

    async def __power_down_anim(self):
        write_led(3, 1)
        write_led(2, 0)
        write_led(1, 0)
        await asyncio.sleep(0.3)
        write_led(3, 0)
        write_led(2, 1)
        write_led(1, 0)
        await asyncio.sleep(0.3)
        write_led(3, 0)
        write_led(2, 0)
        write_led(1, 1)
        await asyncio.sleep(0.3)
        write_led(3, 0)
        write_led(2, 0)
        write_led(1, 0)


# Example usage: Simulate a load process on the device
# 1. Start by showing a loading animation
# 2. After 5 seconds, stop the load animation and flash the LEDs twice (signal connected)
# 3. Show power-down animation (simulates signal disconnected)
async def main():
    controller = LEDController()
    
    # Show loading animation, will run indefinitely until interrupted
    await controller.show_loading(wait_for_completion=False)
    
    for i in range(5):
        print("Waiting...")
        await asyncio.sleep(1)
    
    # Execute flash_twice and ensure it starts
    # Don't wait for flash_twice() to finish before continuing code execution
    await controller.flash_twice(wait_for_completion=False)
    
    # Now interrupt with power_down_anim, wait for animation to finish before program terminates
    await controller.power_down_anim()

if __name__ == "__main__":
    asyncio.run(main())