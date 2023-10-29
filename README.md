# Kafka Producer and Consumer with AWS S3 and Athena Integration

This project demonstrates a setup for a Kafka producer and consumer, designed to fetch data from an external API and store it in AWS S3 and queried with AWS Athena.

## Prerequisites

Before you start, make sure you have the following dependencies and access credentials:

- [Docker](https://www.docker.com/get-started)
- A running Kafka broker accessible over the network on an AWS EC2 instance.
- AWS S3 credentials with access to an S3 bucket.

## Getting Started

1. Clone this repository:

   ```bash
   git clone https://github.com/JawaharRamis/aws-kafka-weather.git
   ```

2. Navigate to the project directory:

3. Update the Docker Compose file (`docker-compose.yml`) with your specific configuration:

   - Set the `KAFKA_BROKER` environment variable to the address of your Kafka broker.
   - Specify your Kafka topic name with the `TOPIC_NAME` variable.
   - Provide your OpenWeather API key as the `OPENWEATHER_API` variable for the producer.
   - For the consumer, set AWS S3 access credentials with `AWS_ACCESS_KEY` and `AWS_SECRET_KEY`, and specify the target S3 bucket with `S3_BUCKET`.

4. Build and start the services:

   ```bash
   docker-compose up -d
   ```

5. The Kafka producer will fetch data from the OpenWeather API and push it to the specified Kafka topic.

6. The Kafka consumer will read data from the Kafka topic and write it to the AWS S3 bucket.

## Monitoring and Logging

The producer and consumer services output logs to the console. You can view the logs by running:

```bash
docker-compose logs -f
```
