Casper Home Assistant

Casper is a modular, locally hosted home assistant designed to control smart devices through natural language voice commands.
The system emphasizes privacy, local inference, and modular architecture, with each room acting as an intelligent node connected to a central “brain”.

Overview

Casper operates on a room-based agent system. Each room node detects the wake word (“Casper”), records a short voice command, and transmits it to a central hub.
The central hub:

Transcribes speech (STT)

Interprets intent via deterministic parsing and local LLM (Ollama)

Executes actions through unified smart device APIs

Logs all activity to PostgreSQL

Current Milestone: Foundations
✅ Goals

Create a unified repository structure

Stand up Docker containers for PostgreSQL + MQTT

Establish environment configuration, linting, and development tools

Implement a minimal “hello world” MQTT message

🧠 Tech Stack

Python 3.10+

PostgreSQL 16 (logging, fuzzy matching)

Eclipse Mosquitto (MQTT) (pub/sub communication)

Ollama + Llama3 (local LLM personality)

Whisper / VOSK (STT pipeline, later milestones)

🗂 Structure
src/
  core/            # Core system functions
  devices/         # Device API adapters
  services/        # Voice + intent logic

🐳 Running the environment
docker-compose up -d

🧪 Test the MQTT connection
python src/core/mqtt_client.py


Extra Tidbits:
[Vendor Adapter] → [Device Registry] → [BaseDevice Abstraction] → [System Logic]
