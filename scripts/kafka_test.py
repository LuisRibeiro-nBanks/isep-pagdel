from kafka import KafkaConsumer
from kafka.admin import KafkaAdminClient, NewTopic
from dotenv import load_dotenv
import os

# To ensure our .env variables are loaded..
load_dotenv()

def get_broker ():
    is_dev_environment = os.getenv("ENVIRONMENT") == "DEVELOPMENT"
    dev_broker = os.getenv("KAFKA_DEVELOPMENT_BROKER")
    docker_brocker = os.getenv("KAFKA_DOCKER_BROKER")
    return dev_broker if is_dev_environment else docker_brocker


def topic_exists(broker, new_topic_name):
    consumer = KafkaConsumer(bootstrap_servers=[broker])
    for topic in consumer.topics():
        if new_topic_name and new_topic_name == topic:
            print(f"Topic {topic} exists!")
            return True
    return False


broker = get_broker()
admin_client = KafkaAdminClient(bootstrap_servers=[broker])

topic = "my-topic"
new_topics_list = [NewTopic(name=topic, num_partitions=1, replication_factor=1)]

if not topic_exists(broker, topic):
    print(f"Creating {topic}")
    admin_client.create_topics(new_topics=new_topics_list, validate_only=False)