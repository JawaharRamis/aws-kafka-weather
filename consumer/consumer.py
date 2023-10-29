import json
from confluent_kafka import Consumer, KafkaError
import boto3
from datetime import datetime
import os

def main():
    kafka_broker = os.environ.get("KAFKA_BROKER")
    aws_access_key = os.environ.get("AWS_ACCESS_KEY")
    aws_secret_key = os.environ.get("AWS_SECRET_KEY")
    kafka_topic = os.environ.get("TOPIC_NAME")
    bucket = os.environ.get("S3_BUCKET") 
    # Kafka consumer configuration
    consumer_config = {
        'bootstrap.servers': kafka_broker,
        'group.id': 'my-group',
        'auto.offset.reset': 'earliest'
    }

    # Create a Kafka consumer instance
    consumer = Consumer(consumer_config)

    # Subscribe to the Kafka topic
    consumer.subscribe([kafka_topic])
    print(aws_access_key, aws_secret_key)
    s3 = boto3.client('s3', 
            aws_access_key_id=aws_access_key,
            aws_secret_access_key=aws_secret_key
        )
    print("inside consumer")
    try:
        while True:
            msg = consumer.poll(3.0)  # Poll for messages with a 1-second timeout
            if msg is None:
                print("No message")
                continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    print('Reached end of partition')
                else:
                    print('Error while consuming message: {}'.format(msg.error()))
            else:
                print('Received message: {}'.format(msg.value().decode('utf-8')))
                msg= json.loads(msg.value().decode('utf-8'))
                today = datetime.now().strftime('%Y-%m-%d')
                current_time = datetime.now().strftime('%H-%M-%S')
                city_name = msg["City"]
                folder_key = f'{city_name}/{today}/{current_time}.json'
                s3.put_object(Bucket = bucket, Key = folder_key, Body = json.dumps(msg))

    finally:
        consumer.close()

if __name__ == "__main__":
    main()