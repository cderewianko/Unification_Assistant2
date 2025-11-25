

import re
import json
import asyncio


class EventBus:
    """
    A lightweight MQTT event router supporting MQTT-style wildcards:
    - '+' matches a single topic level
    - '#' matches all remaining levels
    """

    def __init__(self, mqtt_client, logger):
        self.mqtt = mqtt_client
        self.logger = logger
        self.routes = []  # list of (pattern, regex, callback)
        
        self.global_callback = self._handle_mqtt_message

        # receive all messages from MQTT and route internally
        #self.mqtt.set_global_callback(self._handle_mqtt_message)

    # -------------------------------------------------
    # Public subscription method
    # -------------------------------------------------
    def subscribe(self, pattern, callback):
        """
        Register a wildcard route.

        Example:
            event_bus.subscribe("home/device/+/command", handler)
        """
        regex = self._compile_mqtt_pattern(pattern)
        self.routes.append((pattern, regex, callback))

        # ensure MQTT receives all messages that may match the pattern
        self.mqtt.subscribe(pattern, callback=None)  # subscribe raw; routing is internal

        self.logger.info(f"[EventBus] Registered route: {pattern}")
    
    #def set_global_callback(self, callback):
    #    """Callback invoked for ALL incoming MQTT messages, regardless of topic."""
    #    self.global_callback = callback

    # -------------------------------------------------
    # Pattern compiler
    # -------------------------------------------------
    def _compile_mqtt_pattern(self, pattern):
        """
        Convert MQTT wildcard to a Python regex.
        """
        regex = re.escape(pattern)
        regex = regex.replace(r'\+', r'[^/]+')     # + matches one level
        regex = regex.replace(r'\#', r'.*')        # # matches everything
        return re.compile("^" + regex + "$")

    # -------------------------------------------------
    # Global MQTT message handler
    # -------------------------------------------------
    async def _handle_mqtt_message(self, topic, payload):
        """
        Called by MQTTClient when any message arrives.
        """
        for pattern, regex, callback in self.routes:
            if regex.match(topic):
                try:
                    if asyncio.iscoroutinefunction(callback):
                        await callback(topic, payload)
                    else:
                        callback(topic, payload)
                except Exception as e:
                    self.logger.error(f"[EventBus] Error in handler for {pattern}: {e}")
