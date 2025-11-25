

import time
import paho.mqtt.client as mqtt


def test_mqtt_connection(host="localhost", port=1884, topic="test/connection", message="ping"):
    """Verify MQTT connectivity by publishing and receiving a test message."""

    received = {"ok": False}

    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print(f"Connected successfully to MQTT broker at {host}:{port}")
            client.subscribe(topic)
        else:
            print(f"Failed to connect, return code {rc}")

    def on_message(client, userdata, msg):
        print(f"Received message: {msg.payload.decode()} on topic {msg.topic}")
        if msg.payload.decode() == message:
            received["ok"] = True
        client.disconnect()

    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    
    try:
        client.connect(host, port, 60)
        client.loop_start()

        # Wait for connection before publishing
        time.sleep(1)
        print(f"Publishing test message '{message}' to topic '{topic}'")
        client.publish(topic, message)

        # Wait for message receipt
        timeout = 5
        for _ in range(timeout * 10):
            if received["ok"]:
                break
            time.sleep(0.1)

        client.loop_stop()
        if received["ok"]:
            print("✅ MQTT connection test succeeded.")
            return True
        else:
            print("❌ MQTT connection test failed (no message received).")
            return False

    except Exception as e:
        print(f"❌ MQTT connection failed: {e}")
        return False


if __name__ == "__main__":
    test_mqtt_connection()
