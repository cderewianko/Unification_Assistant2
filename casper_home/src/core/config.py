"""

# Example usage.
from src.core.config import Config

config = Config()
mqtt_host = config.get("mqtt_DEPRECATED.host")
log.info(f"MQTT host: {mqtt_host}")

"""
# TODO: Module needs to be deprecated
'''
from dotenv import load_dotenv

# Load the .env file located at the base of the project.
load_dotenv()

# Variable check tests.
#import os
#some_variable = os.getenv('POSTGRES_USER')
#print('some_variable: ', some_variable)

import os
import yaml
from dotenv import load_dotenv
from pathlib import Path

class Config:
    def __init__(self, config_file: str = "config.yaml"):
        load_dotenv()  # Load from .env if exists

        base_path = Path(__file__).resolve().parents[2]
        file_path = base_path / config_file

        # Default configuration values
        self.data = {
            "mqtt_DEPRECATED": {
                "host": os.getenv("MQTT_HOST", "localhost"),
                "port": int(os.getenv("MQTT_PORT", 1883)),
                "topic_prefix": os.getenv("MQTT_TOPIC_PREFIX", "home/")
            },
            "database": {
                "host": os.getenv("DB_HOST", "localhost"),
                "port": int(os.getenv("DB_PORT", 5432)),
                "name": os.getenv("DB_NAME", "casper_db"),
                "user": os.getenv("DB_USER", "postgres"),
                "password": os.getenv("DB_PASSWORD", "postgres")
            },
            "general": {
                "log_level": os.getenv("LOG_LEVEL", "INFO"),
                "debug_mode": os.getenv("DEBUG_MODE", "false").lower() == "true"
            }
        }

        # Merge config file if available
        if file_path.exists():
            with open(file_path, "r", encoding="utf-8") as f:
                file_data = yaml.safe_load(f)
                self._deep_update(self.data, file_data)

    def _deep_update(self, base: dict, updates: dict):
        """Recursively update dictionary"""
        for key, value in updates.items():
            if isinstance(value, dict) and key in base:
                self._deep_update(base[key], value)
            else:
                base[key] = value

    def get(self, key_path: str, default=None):
        keys = key_path.split(".")
        val = self.data
        for k in keys:
            val = val.get(k, {})
        return val or default
'''