from sys import api_version
from kafka.admin import KafkaAdminClient, NewTopic

# Set up Kafka Admin Client
admin_client = KafkaAdminClient(
    bootstrap_servers="10.100.102.49:9092",  # Replace with your Docker container IP and port if necessary
    client_id="sensor_client",
    api_version=(7,7,1)
)

# Define new topic
topic_list = [NewTopic(name="sensors", num_partitions=1, replication_factor=1)]

# Create topic
admin_client.create_topics(new_topics=topic_list, validate_only=False)

print("Topic created successfully")
