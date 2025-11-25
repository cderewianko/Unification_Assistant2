"""Create November 14, 2025"""


import os
import psycopg2
import paho.mqtt.client as mqtt
from datetime import datetime

# -------------------------
# Postgres connection pool
# -------------------------
def get_db_connection():
    return psycopg2.connect(
        host=os.getenv("POSTGRES_HOST", "localhost"),
        port=os.getenv("POSTGRES_PORT", "5432"),
        dbname=os.getenv("POSTGRES_DB", "casper_home"),
        user=os.getenv("POSTGRES_USER", "casper"),
        password=os.getenv("POSTGRES_PASSWORD", "password123")
    )

# ----------------------------------
# Callback when MQTT connects
# ----------------------------------
def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT with result:", rc)
    client.subscribe("#")  # subscribe to all topics


# ----------------------------------
# Callback when MQTT receives message
# ----------------------------------
def on_message(client, userdata, msg):
    print(f"MQTT: {msg.topic} → {msg.payload.decode()}")

    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            """
            INSERT INTO mqtt_messages (topic, payload, received_at)
            VALUES (%s, %s, %s)
            """,
            (msg.topic, msg.payload.decode(), datetime.utcnow())
        )
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        print("DB Insert Error:", e)


# ----------------------------------
# Main loop
# ----------------------------------
def start_mqtt_consumer():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    # Broker host & port
    broker = os.getenv("MQTT_HOST", "localhost")
    port = int(os.getenv("MQTT_PORT", "1883"))

    client.connect(broker, port, 60)
    client.loop_forever()

def create_temp_file():
    with open("D:/dev/Unification_Assistant/dump/temp_file.txt", "w") as file:
        file.write("This is a temporary file created by the rock-star python developer!")
    

if __name__ == "__main__":
    create_temp_file()
    #start_mqtt_consumer()
