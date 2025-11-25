
import asyncio
import json
import logging
import paho.mqtt.client as mqtt
from fnmatch import fnmatch


#############################################################################
# Attempt 1
#def on_message(client, userdata, msg):
#    print(f"Received on {msg.topic}: {msg.payload.decode()}")
#
#
#client = mqtt_DEPRECATED.Client(client_id="casper-brain")
#    #callback_api_version="1.1"
##)
#client.on_message = on_message
#client.connect("localhost", 1883)
#client.subscribe("casper/test")
#
#client.loop_start()
#client.publish("casper/test", "hello from brain")
#
#print('client: ', client)
#
#print('Completed Test')
#
#############################################################################


#############################################################################
# Attempt 2

'''
class MQTTClient:
    def __init__(self, host="localhost", port=1883, logger=None):
        self.host = host
        self.port = port
        self.logger = logger or logging.getLogger("MQTTClient")
        self.client = mqtt.Client()
        print('self.client: ', self.client)
        self.loop = asyncio.get_event_loop()
        print('self.loop: ', self.loop)
        self.subscriptions = {}

        self.client.on_connect = self._on_connect
        self.client.on_message = self._on_message
        self.client.on_disconnect = self._on_disconnect

    def _on_connect(self, client, userdata, flags, rc):
        self.logger.info(f"Connected to MQTT Broker ({self.host}:{self.port}) with result code {rc}")
        for topic in self.subscriptions:
            self.client.subscribe(topic)
            self.logger.info(f"Re-subscribed to topic: {topic}")

    def _on_message(self, client, userdata, msg):
        payload = msg.payload.decode("utf-8")
        try:
            data = json.loads(payload)
        except json.JSONDecodeError:
            self.logger.warning(f"Invalid JSON on {msg.topic}: {payload}")
            return

        callback = self.subscriptions.get(msg.topic)
        #if callback:
        #    self.loop.call_soon_threadsafe(asyncio.create_task, callback(data))
        
        if asyncio.iscoroutinefunction(callback):
            self.loop.call_soon_threadsafe(lambda: asyncio.create_task(callback(data)))
        else:
            self.loop.call_soon_threadsafe(callback, data)

    def _on_disconnect(self, client, userdata, rc):
        print('client, userdata, rc: ', client, userdata, rc)
        self.logger.warning("Disconnected from MQTT Broker.")

    async def connect(self):
        def run():
            print('self.host: ', self.host)
            print('self.port: ', self.port)
            self.client.connect(self.host, self.port, 60)
            #self.client.loop_forever()
            self.client.loop_start()

        #self.loop.run_in_executor(None, run)
        await self.loop.run_in_executor(None, run)

    def subscribe(self, topic, callback):
        self.subscriptions[topic] = callback
        self.client.subscribe(topic)

    async def publish(self, topic, payload):
        msg = json.dumps(payload)
        self.client.publish(topic, msg)

'''

#############################################################################
# Attempt 3

'''
class MQTTClient:
    def __init__(self, host="localhost", port=1883, logger=None):
        self.host = host
        self.port = port
        self.logger = logger or logging.getLogger("MQTTClient")
        self.client = mqtt.Client()
        self.loop = asyncio.get_event_loop()
        self.subscriptions = {}
        self.connected = asyncio.Event()

        self.client.on_connect = self._on_connect
        self.client.on_message = self._on_message
        self.client.on_disconnect = self._on_disconnect

    def _on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            self.logger.info(f"Connected to MQTT Broker ({self.host}:{self.port})")
            self.connected.set()
            for topic in self.subscriptions:
                self.client.subscribe(topic)
                self.logger.info(f"Re-subscribed to topic: {topic}")
                
        else:
            self.logger.error(f"MQTT connection failed with code {rc}")

    def _on_message(self, client, userdata, msg):
        payload = msg.payload.decode("utf-8")
        try:
            data = json.loads(payload)
            
        except json.JSONDecodeError:
            self.logger.warning(f"Invalid JSON on {msg.topic}: {payload}")
            return

        callback = self.subscriptions.get(msg.topic)
        if callback:
            if asyncio.iscoroutinefunction(callback):
                self.loop.call_soon_threadsafe(lambda: asyncio.create_task(callback(data)))
            
            else:
                self.loop.call_soon_threadsafe(callback, data)

    def _on_disconnect(self, client, userdata, rc):
        self.logger.warning(f"Disconnected from MQTT Broker (rc={rc})")
        self.connected.clear()

    async def connect(self):
        def run():
            self.client.connect(self.host, self.port, 60)
            self.client.loop_start()

        await self.loop.run_in_executor(None, run)
        await asyncio.wait_for(self.connected.wait(), timeout=5)

    def subscribe(self, topic, callback):
        self.subscriptions[topic] = callback
        if self.connected.is_set():
            self.client.subscribe(topic)

    async def publish(self, topic, payload):
        msg = json.dumps(payload)
        self.client.publish(topic, msg)

    async def test_connection(self):
        """Simple round-trip check to confirm pub/sub works."""
        result = asyncio.Future()

        async def on_test_message(data):
            if data.get("ping") == "pong":
                result.set_result(True)

        self.subscribe("test/verify", on_test_message)
        await self.publish("test/verify", {"ping": "pong"})

        try:
            await asyncio.wait_for(result, timeout=3)
            self.logger.info("MQTT connection verified successfully.")
            return True
        except asyncio.TimeoutError:
            self.logger.error("MQTT connection test failed (no echo received).")
            return False
'''

# Attempt 4


class MQTTClient:
    def __init__(self, host="localhost", port=1883, logger=None):
        self.host = host
        self.port = port
        self.logger = logger or logging.getLogger("MQTTClient")
        
        self.global_callback = None

        self.client = mqtt.Client()
        self.loop = asyncio.get_event_loop()

        # Store subscriptions as:  { topic_pattern: callback }
        # Supports wildcards for + and # using fnmatch.
        self.subscriptions = {}

        # Additional list for introspection
        self.subscription_list = []  # (topic_pattern, callback)

        self.connected = asyncio.Event()

        # Bind base callbacks
        self.client.on_connect = self._on_connect
        self.client.on_message = self._on_message
        self.client.on_disconnect = self._on_disconnect

    # -----------------------------
    # MQTT EVENT HANDLERS
    # -----------------------------

    def _on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            self.logger.info(f"Connected to MQTT Broker ({self.host}:{self.port})")
            self.connected.set()

            # Resubscribe to all topics after reconnect
            for topic, _ in self.subscription_list:
                self.client.subscribe(topic)
                self.logger.info(f"Re-subscribed to topic: {topic}")
        else:
            self.logger.error(f"MQTT connection failed with code {rc}")

    def _on_disconnect(self, client, userdata, rc):
        self.logger.warning(f"Disconnected from MQTT Broker (rc={rc})")
        self.connected.clear()
    
    def _on_message(self, client, userdata, msg):
        payload = msg.payload.decode("utf-8")
        try:
            data = json.loads(payload)
        except json.JSONDecodeError:
            self.logger.warning(f"Invalid JSON on {msg.topic}: {payload}")
            return
        
        # NEW: Global catch-all handler
        if self.global_callback:
            self.loop.call_soon_threadsafe(
                lambda: asyncio.create_task(self.global_callback(msg.topic, data))
            )
        
        # Existing handler for specific topics
        callback = self.subscriptions.get(msg.topic)
        if callback:
            if asyncio.iscoroutinefunction(callback):
                self.loop.call_soon_threadsafe(lambda: asyncio.create_task(callback(data)))
            else:
                self.loop.call_soon_threadsafe(callback, data)
    
    def _on_message2(self, client, userdata, msg):
        """Match incoming topics against registered wildcard subscriptions."""
        payload = msg.payload.decode("utf-8")

        try:
            data = json.loads(payload)
        except json.JSONDecodeError:
            self.logger.warning(f"Invalid JSON on {msg.topic}: {payload}")
            return

        # Find matching subscription(s)
        for pattern, callback in self.subscriptions.items():
            if fnmatch(msg.topic, pattern):  # Supports MQTT wildcards
                if asyncio.iscoroutinefunction(callback):
                    self.loop.call_soon_threadsafe(
                        lambda: asyncio.create_task(callback(data))
                    )
                else:
                    self.loop.call_soon_threadsafe(callback, data)

    # -----------------------------
    # CORE METHODS
    # -----------------------------

    async def connect(self):
        """Connect and start background thread."""
        def run():
            self.client.connect(self.host, self.port, 60)
            self.client.loop_start()

        await self.loop.run_in_executor(None, run)
        await asyncio.wait_for(self.connected.wait(), timeout=5)

    def subscribe(self, topic_pattern, callback):
        """
        Subscribe to a topic or wildcard pattern.
        Supports:
            home/device/+/command
            home/#
        """
        self.subscriptions[topic_pattern] = callback
        self.subscription_list.append((topic_pattern, callback))

        if self.connected.is_set():
            self.client.subscribe(topic_pattern)
            self.logger.info(f"Subscribed: {topic_pattern}")

    async def publish(self, topic, payload):
        msg = json.dumps(payload)
        self.client.publish(topic, msg)

    # -----------------------------
    # INTROSPECTION HELPERS
    # -----------------------------

    def list_subscriptions(self):
        """Return full subscription table."""
        return self.subscription_list

    def print_subscriptions(self):
        """Console/log output of active subscriptions."""
        self.logger.info("Active MQTT Subscriptions:")
        for topic, callback in self.subscription_list:
            handler_name = (
                callback.__qualname__ if hasattr(callback, "__qualname__") else str(callback)
            )
            self.logger.info(f" • {topic} → {handler_name}")

    # -----------------------------
    # DIAGNOSTIC METHOD
    # -----------------------------

    async def test_connection(self):
        """Simple round-trip check to confirm pub/sub works."""
        result = asyncio.Future()

        async def on_test_message(data):
            if data.get("ping") == "pong":
                if not result.done():
                    result.set_result(True)

        self.subscribe("test/verify", on_test_message)
        await self.publish("test/verify", {"ping": "pong"})

        try:
            await asyncio.wait_for(result, timeout=3)
            self.logger.info("MQTT connection verified successfully.")
            return True
        except asyncio.TimeoutError:
            self.logger.error("MQTT connection test failed (no echo received).")
            return False

