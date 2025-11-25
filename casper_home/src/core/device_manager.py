"""

Every device gets consistent topic paths:

home/device/<id>/state
home/device/<id>/status
home/device/<id>/event/<event_type>
home/device/<id>/command  (consumed by CommandHandler)


This is now deterministic across all adapters.

"""

import time
from typing import Dict, List, Optional, Type

from casper_home.src.devices.base_device import BaseDevice


################################################### NEW Novermber 24, 2025

class DeviceManager:
    def __init__(self, config, logger, event_bus):
        self.config = config
        self.logger = logger
        self.event_bus = event_bus
        
        self.registry: Dict[str, BaseDevice] = {}

        self.adapters = []
        self.devices = {}   # device_id → device instance

    # -------------------------------------------------
    async def start(self):
        self.logger.info("[DeviceManager] Starting…")
        await self.discover_all()
        self.logger.info("[DeviceManager] Ready.")

    # -------------------------------------------------
    async def discover_all(self):
        """
        Poll all adapters and register the devices they discover.
        """
        devices = []

        for adapter in self.adapters:
            found = await adapter.discover()
            devices.extend(found)

        # Register devices
        for device in devices:
            self.devices[device.device_id] = device
            self.logger.info(f"[DeviceManager] Registered device {device.device_id}")
    
    def register_device(self, device: BaseDevice):
        """Register a single device instance."""
        self.registry[device.get("device_id")] = device
    
    # -------------------------------------------------
    def topic(self, device_id, suffix):
        """
        Generate structured topic names.
        """
        return f"home/device/{device_id}/{suffix}"

    # -------------------------------------------------
    async def publish_state(self, device_id, state_dict):
        topic = self.topic(device_id, "state")
        await self.event_bus.mqtt.publish(topic, state_dict)

    async def publish_event(self, device_id, event_type, data):
        topic = self.topic(device_id, f"event/{event_type}")
        await self.event_bus.mqtt.publish(topic, data)

    async def publish_status(self, device_id, data):
        topic = self.topic(device_id, "status")
        await self.event_bus.mqtt.publish(topic, data)

    # -------------------------------------------------
    async def execute_command(self, device_id, command):
        """
        Forward command dict to device adapter.
        """
        device = self.devices.get(device_id)

        if not device:
            self.logger.error(f"[DeviceManager] Unknown device: {device_id}")
            return

        await device.execute(command)




################################################### NEW November 11, 2025
'''
import asyncio
import logging

from casper_home.src.adapters.tplink_adapter import TPLinkAdapter
from casper_home.src.adapters.ewelink_adapter import EWeLinkAdapter


class DeviceManager:
    """
    DeviceManager coordinates all adapters and devices.
    It handles discovery, registration, and event-driven commands via MQTT/EventBus.
    """
    def __init__(self, config, logger=None, event_bus=None):
        self.config = config
        self.logger = logger or logging.getLogger("DeviceManager")
        self.event_bus = event_bus
        self.adapters = []
        self.devices = {}

    async def start(self):
        """Initialize adapters, run discovery, and subscribe to event topics."""
        self.logger.info("Starting DeviceManager...")

        # Initialize Adapters
        self.adapters = [
            #TPLinkAdapter(self.config, self.logger),
            TPLinkAdapter(),
            #EWeLinkAdapter(self.config, self.logger)
            EWeLinkAdapter()
        ]

        await self.discover_all()
        #print('ping 11')
        # Subscribe to all device command topics
        if self.event_bus:
            self.logger.info("Subscribing to command topics...")
            await self._subscribe_to_commands()

        self.logger.info("DeviceManager started successfully.")

    async def discover_all(self):
        """Discover devices from all adapters."""
        discovered = []
        for adapter in self.adapters:
            self.logger.info(f"Discovering devices via {adapter.__class__.__name__}...")
            results = await adapter.discover()
            for dev in results:
                #print('dev: ', dev)
                #self.devices[dev['id']] = dev
                self.devices[dev["name"]] = dev
                discovered.append(dev)
                if self.event_bus:
                    # Publish device discovered event
                    await self.event_bus.emit(
                        f"ua/{dev['type']}/{dev['name']}/state",
                        {"event": "device_discovered", "device": dev}
                    )
        self.logger.info(f"Discovered {len(discovered)} devices.")
        return discovered

    async def _subscribe_to_commands(self):
        """Subscribe to all device command topics for unified event handling."""
        async def handle_command(message):
            try:
                device_id = message.get("device_id")
                command = message.get("command")
                params = message.get("params", {})

                device = self.devices.get(device_id)
                if not device:
                    self.logger.warning(f"Unknown device in command: {device_id}")
                    return

                adapter = next((a for a in self.adapters if a.name == device['adapter']), None)
                if not adapter:
                    self.logger.warning(f"No adapter found for {device['adapter']}")
                    return

                self.logger.info(f"Executing {command} on {device_id}")
                result = await adapter.execute(device, command, params)

                # Publish confirmation
                await self.event_bus.emit(
                    f"ua/{device['adapter']}/{device['id']}/state",
                    {"event": "command_executed", "device_id": device_id, "result": result}
                )

            except Exception as e:
                self.logger.error(f"Error handling command: {e}")

        # Generic wildcard subscription
        self.event_bus.on("ua/+/+/command", handle_command)

    async def handle_command(self, message):
        """Optional direct entrypoint if commands are routed manually."""
        await self._subscribe_to_commands()(message)
'''

################################################### OLD


'''

class DeviceManager2:
    """
    Acts as the central registry for all smart devices and adapters.
    """

    def __init__(self):
        self.registry: Dict[str, BaseDevice] = {}
        self.adapters: List[Type] = []

    def register_adapter(self, adapter_cls: Type):
        """Register a device adapter class (like TPLinkAdapter or EWeLinkAdapter)."""
        self.adapters.append(adapter_cls)

    async def discover_all(self):
        """Run discovery for all registered adapters."""
        discovered = []
        for adapter_cls in self.adapters:
            adapter = adapter_cls()
            discovered_devices = await adapter.discover()
            for device in discovered_devices:
                self.register_device(device)
                
            discovered.extend(discovered_devices)
            
        return discovered

    def register_device(self, device: BaseDevice):
        """Register a single device instance."""
        self.registry[device.get("device_id")] = device

    def get_device_by_name(self, name: str) -> Optional[BaseDevice]:
        for dev in self.registry.values():
            if dev.get("name").lower() == name.lower():
                return dev
        
        return None

    async def control_device(self, name: str, action: str):
        """Perform an action (turn_on, turn_off, toggle) on a named device."""
        device = self.get_device_by_name(name)
        if not device:
            raise ValueError(f"No device found with name: {name}")

        #if not hasattr(device, action):
        #    raise ValueError(f"Device {name} does not support action: {action}")

        #method = getattr(device, action)
        #if asyncio.iscoroutinefunction(method):
        #    return await method()
        #else:
        #    return method()
        
        # TODO: Look up manufacturer for type of input, example: sonnoff inputs as True/False and tp-link is 0/1
        from casper_home.src.devices import ewelink_device
        device_id = device["identifiers"]["device_id"]
        await ewelink_device.sync_toggle_device(device_id=device_id, state=True)
        time.sleep(2)
        await ewelink_device.sync_toggle_device(device_id=device_id, state=False)
        

    def list_devices(self):
        return list(self.registry.values())



'''
