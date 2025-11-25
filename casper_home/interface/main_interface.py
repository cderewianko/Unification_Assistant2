

import tkinter as tk
import kasa
import asyncio



class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()
    
    def create_widgets(self):
        self.on_button = tk.Button(self)
        self.on_button["text"] = "On"
        self.on_button["command"] = self.toggle_lights
        self.on_button.pack(side="top")
    
    def toggle_lights(self):
        #pass  # This function will be filled accordingly
        toggle_device("192.168.1.194")
        #toggle_device("192.168.1.127")


def toggle_device(device_ip: str):
    """Toggle a Smart Plug or Switch on or off."""
    
    async def inner_check():
        # plug = SmartPlug(device_ip)
        plug = kasa.iot.IotPlug(device_ip)
        
        await plug.update()  # Get current state #  DO NOT REMOVE
        
        # Show current status
        print(f"Device: {plug.alias} ({device_ip}) is currently {'ON' if plug.is_on else 'OFF'}")
        
        # Toggle the device
        if plug.is_on:
            await plug.turn_off()
        else:
            await plug.turn_on()
        
        # Recheck state
        await plug.update()  # DO NOT REMOVE
        new_state = "ON" if plug.is_on else "OFF"
        print(f"Device: {plug.alias} is now {new_state}")
        
        # Log the event
        # await log_event()
        
        return plug.is_on
    
    return asyncio.run(inner_check())


# async def log_event():
#    logger = Logger.with_default_handlers(name='my_log')
#    async_handler = AsyncFileHandler('my_log.log', mode='w')
#    logger.add_handler(async_handler)
#    await logger.info('This is a log from aiologger')
#    await logger.shutdown()




root = tk.Tk()
app = Application(master=root)
app.mainloop()

