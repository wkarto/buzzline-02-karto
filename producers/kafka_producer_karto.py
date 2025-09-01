"""
kafka_producer_karto.py

Send JSON messages to a Kafka topic.
"""

#####################################
# Import Modules
#####################################

import os
import json
import time
from dotenv import load_dotenv
from kafka import KafkaProducer
from utils.utils_logger import logger
from utils.utils_producer import get_kafka_broker_address

#####################################
# Load Environment Variables
#####################################

load_dotenv()

#####################################
# Getter Functions for .env Variables
#####################################

def get_kafka_topic() -> str:
    topic = os.getenv("KAFKA_TOPIC", "buzzline")
    logger.info(f"Kafka topic: {topic}")
    return topic

#####################################
# Send messages function
#####################################

def send_message(producer: KafkaProducer, topic: str, message: dict) -> None:
    try:
        # Convert dict to JSON bytes
        msg_bytes = json.dumps(message).encode("utf-8")
        producer.send(topic, msg_bytes)
        producer.flush()
        logger.info(f"Sent message: {message}")
    except Exception as e:
        logger.error(f"Failed to send message: {e}")

#####################################
# Main function
#####################################

def main() -> None:
    logger.info("START climate producer.")

    topic = get_kafka_topic()
    broker = get_kafka_broker_address()

    logger.info(f"Connecting to Kafka broker at {broker}...")
    producer = KafkaProducer(bootstrap_servers=[broker])
    logger.info("Kafka producer successfully created.")

    # Example climate data messages
    messages = [
        {"city": "Mumbai", "temp": 32, "condition": "Sunny"},
        {"city": "Delhi", "temp": 28, "condition": "Cloudy"},
        {"city": "Bangalore", "temp": 24, "condition": "Rainy"},
        {"city": "Kolkata", "temp": 30, "condition": "Hot"},
    ]

    try:
        while True:
            for msg in messages:
                send_message(producer, topic, msg)
                time.sleep(2)  # simulate streaming
    except KeyboardInterrupt:
        logger.warning("Producer interrupted by user.")
    finally:
        producer.close()
        logger.info(f"Kafka producer for topic '{topic}' closed.")
        logger.info("END climate producer.")

#####################################
# Conditional execution
#####################################

if __name__ == "__main__":
    main()
