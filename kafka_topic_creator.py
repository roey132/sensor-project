from kafka.admin import KafkaAdminClient, NewTopic

# Set up Kafka Admin Client
admin_client = KafkaAdminClient(
    bootstrap_servers="10.0.0.13:29092",  # Replace with correct IP and port if necessary
    client_id="sensors"
)

# Define new topic
topic_list = [NewTopic(name="sensorstest", num_partitions=1, replication_factor=1)]

# Create topic
admin_client.create_topics(new_topics=topic_list, validate_only=False)

print("Topic created successfully")