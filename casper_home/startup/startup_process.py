

import os
import subprocess
import time

import check_docker_engine as cde

# TODO: This is a starting point. Later, you can expand to check PostgreSQL, any other services, and even run migrations or device discovery.
from casper_home.src.core.logger import Logger
logger = Logger().setup_logger("INFO")


def is_container_running(name):
    logger.info(f"\t- Check Running Docker Container : {name}")
    # docker compose -f D:\dev\Unification_Assistant\docker-raspberry-pi\docker-compose.yml up -d
    result = subprocess.run(
        #["docker-raspberry-pi", "ps", "--filter", f"name={name}", "--format", "{{.Names}}"],
        #["docker", "compose", "-f", "D:/dev/Unification_Assistant/docker-raspberry-pi/docker-compose.yml", "up", "-d"],
        ["docker", "compose", "-f", "D:/dev/Unification_Assistant/docker-raspberry-pi/docker-compose.yml", "ps"],
        capture_output=True, text=True
    )
    
    return name in result.stdout




def start_container(name, compose_file="D:/dev/Unification_Assistant/docker-raspberry-pi/docker-compose.yml"):
    logger.info(f"\t- Starting Docker Container: {name} Using: {compose_file}")
    subprocess.run(
        #["docker-raspberry-pi", "compose", "-f", compose_file, "up", "-d", name]
        ["docker", "compose", "-f", "D:/dev/Unification_Assistant/docker-raspberry-pi/docker-compose.yml", "up", "-d", name],
    
    )
    # Wait a few seconds for startup
    time.sleep(5)


def check_mqtt(host="localhost", port=1883):
    logger.info(f"\t- Check Running MQTT Host: {host} Port: {port}")
    try:
        
        print(".... inside")
        import paho.mqtt.client as mqtt
        client = mqtt.Client()
        print('client: ', client)
        connected_client = client.connect(host, port, 5)
        print('connected_client: ', connected_client)
        disconnect_client = client.disconnect()
        print('disconnect_client: ', disconnect_client)
        return True
    
    except:
        return False


def check_postgres(host="localhost", port=5432):
    logger.info(f"\t- Check Running PostgreSQL Host: {host} Port: {port}")
    try:
        import psycopg2
        conn = psycopg2.connect(
            host=os.getenv("POSTGRES_HOST", "localhost"),
            port=os.getenv("POSTGRES_PORT", "5432"),
            dbname=os.getenv("POSTGRES_DB", "casper_home"),
            user=os.getenv("POSTGRES_USER", "casper"),
            password=os.getenv("POSTGRES_PASSWORD", "password123")
        )
        conn.close()
        return True
    
    except:
        return False


def compose_containers(name="docker-raspberry-pi/docker-compose.yml", compose_file="D:/dev/Unification_Assistant/docker-raspberry-pi/docker-compose.yml"):
    logger.info(f"\t- Starting Docker Container: {name} Using: {compose_file}")
    
    subprocess.run(
        # ["docker-raspberry-pi", "compose", "-f", compose_file, "up", "-d", name]
        ["docker", "compose", "-f", compose_file, "up", "-d",
         #name
         ],
    
    )
    # Wait a few seconds for startup
    time.sleep(3)


def initialize_sequence(logger=logger):
    
    # Original information in config .env file.
    container_name = os.getenv("DOCKER_CONTAINER_NAME")
    compose_file = os.getenv("DOCKER_COMPOSE_FILE_PATH")
    
    # Check if the Docker Engine is running.
    if not cde.check_docker_uptime():
        logger.error("Docker Engine is not running.")
    else:
        logger.info("Docker Engine running.")
    
    #return
    
    compose_containers()
    
    return
    
    if not is_container_running(container_name):
        start_container(container_name, compose_file=compose_file)
    
    #else:
    
    
    logger.info("\t- Check - MQTT Broker")
    while not check_mqtt():
        logger.warning("\tWaiting for MQTT...")
        time.sleep(2)
    
    logger.info("\t- Ready MQTT broker ready.")


if __name__ == "__main__":
    initialize_sequence()

