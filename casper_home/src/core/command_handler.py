

#import json
#from src.core.mqtt_client import MQTTClient
#from src.core.device_manager import DeviceManager


class CommandHandler:
    """
    Listens for device command topics and forwards commands
    to the DeviceManager.
    """

    def __init__(self, event_bus, device_manager, logger=None):
        self.event_bus = event_bus
        self.device_manager = device_manager
        self.logger = logger or device_manager.logger

    async def start(self):
        # Example route:
        # home/device/<id>/command
        topic_pattern = "home/device/+/command"

        self.event_bus.subscribe(topic_pattern, self.handle_command)
        self.logger.info(f"[CommandHandler] Subscribed to {topic_pattern}")

    # -------------------------------------------------
    async def handle_command(self, topic, payload):
        """
        topic: "home/device/<id>/command"
        payload: {"action": "toggle", "value": true}
        """
        device_id = topic.split("/")[2]  # extract wildcard match

        self.logger.info(f"[CommandHandler] Command for {device_id}: {payload}")

        try:
            await self.device_manager.execute_command(device_id, payload)
        except Exception as e:
            self.logger.error(f"[CommandHandler] Error handling command: {e}")
