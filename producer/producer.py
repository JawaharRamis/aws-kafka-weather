import requests
from utils import read_csv, send_to_kafka
from confluent_kafka import Producer
import time
import os



def main():
    kafka_broker = os.environ.get("KAFKA_BROKER")
    producer_config = {
        # 'bootstrap.servers': "52.32.233.173:9092",
        'bootstrap.servers': kafka_broker,
        'client.id': 'python-producer'
    }
    producer = Producer(producer_config)
    kafka_topic = os.environ.get("TOPIC_NAME")
    api_key = os.environ.get("OPENWEATHER_API")

    city_list = read_csv()
    # Iterate over each city in the dictionary
    for city_item in city_list:
        city_code= city_item['city_id']
        city_name= city_item['city_name']
        # URL for the OpenWeatherMap API
        url = f'http://api.openweathermap.org/data/2.5/weather?id={city_code}&appid={api_key}'
        try:
            # Send an HTTP GET request to the API
            response = requests.get(url)
        
            # Check if the request was successful (status code 200)
            if response.status_code == 200:
                data = response.json()
                # Extract relevant weather information
                main_weather = data['weather'][0]['main']
                description = data['weather'][0]['description']
                temperature = data['main']['temp']
                humidity = data['main']['humidity']
                message = {
                    "City": city_name,
                    "Weather": f'{main_weather} - {description}',
                    "Temperature": f'{temperature}°C',
                    "Humidity": f'{humidity}%'
                }
                send_to_kafka(producer, kafka_topic, message, message["City"])

                # Display the weather information for the current city
                print(f'City: {city_name}')
                print(f'Weather: {main} - {description}')
                print(f'Temperature: {temperature}°C')
                print(f'Humidity: {humidity}%')
                print('-' * 30)  # Separate city data with a line
            else:
                print(f'Error: Unable to retrieve weather data for {city_name}. Status code {response.status_code}')
        except requests.exceptions.RequestException as e:
            print(f'Error: An HTTP request error occurred for {city_name}. {e}')

if __name__ == "__main__":
    while True:
        main()
        time.sleep(60)
