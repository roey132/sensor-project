from kafka import KafkaConsumer
import json

# Initialize the Kafka consumer
consumer = KafkaConsumer(
    'sensor-input',                 # Replace with your topic name
    bootstrap_servers='10.100.102.54:9092',
    auto_offset_reset='earliest',       # Start from the earliest message
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))  # Deserializes JSON messages
)

print("Reading messages from topic...")

# Consume messages
for message in consumer:
    print("Received message:", message.value)