"""
kafka_consumer_karto.py

Consume JSON messages from Kafka topic and process them.
"""

#####################################
# Import Modules
#####################################

import os
import json
from dotenv import load_dotenv
from kafka import KafkaConsumer
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

def get_kafka_consumer_group_id() -> str:
    group_id = os.getenv("KAFKA_CONSUMER_GROUP_ID_JSON", "climate_group")
    logger.info(f"Kafka consumer group id: {group_id}")
    return group_id

#####################################
# Process message
#####################################

def process_message(message: str) -> None:
    try:
        data = json.loads(message)
    except json.JSONDecodeError:
        logger.error(f"Invalid JSON: {message}")
        return

    city = data.get("city")
    temp = data.get("temp")
    condition = data.get("condition")

    logger.info(f"Processing city={city}, temp={temp}, condition={condition}")

    if temp and temp > 30:
        logger.warning(f"High temperature alert! {city}: {temp}°C")

#####################################
# Main function
#####################################

def main() -> None:
    logger.info("START climate consumer.")

    topic = get_kafka_topic()
    group_id = get_kafka_consumer_group_id()
    broker = get_kafka_broker_address()

    logger.info(f"Consumer: Topic '{topic}' and group '{group_id}'...")

    consumer = KafkaConsumer(
        topic,
        bootstrap_servers=[broker],
        group_id=group_id,
        auto_offset_reset="earliest",
        enable_auto_commit=True,
        value_deserializer=lambda m: m.decode("utf-8")
    )

    try:
        for message in consumer:
            logger.debug(f"Received message at offset {message.offset}: {message.value}")
            process_message(message.value)
    except KeyboardInterrupt:
        logger.warning("Consumer interrupted by user.")
    finally:
        consumer.close()
        logger.info(f"Kafka consumer for topic '{topic}' closed.")
        logger.info(f"END climate consumer for topic '{topic}' and group '{group_id}'.")

#####################################
# Conditional execution
#####################################

if __name__ == "__main__":
    main()

