
import asyncio

from mqtt_DEPRECATED.mqtt_client import MQTTClient
from casper_home.src.core.device_manager import DeviceManager
from casper_home.src.devices.tplink_device import TpLinkDevice

from startup import startup_process


async def main():
    manager = DeviceManager()
    mqtt = MQTTClient()
    mqtt.connect()
    

    # Register sample device
    plug = TpLinkDevice("plug_1", "Living Room Light", "livingroom", "192.168.1.101")
    manager.register_device(plug)

    # Subscribe to toggle commands
    def on_mqtt_message(topic, payload):
        if payload.lower() == "toggle":
            asyncio.create_task(manager.toggle_device("Living Room Light"))
    mqtt.subscribe("home/livingroom/light", on_mqtt_message)

    print("✅ Device Manager running...")
    
#startup_process.initialize_sequence()


asyncio.run(main())
