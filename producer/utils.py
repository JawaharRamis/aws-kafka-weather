# import os
# from dotenv import load_dotenv
import csv
import json


# def get_env_variable(variable_name, default=None):
#     # Get the directory of the currently executing script
#     current_directory = os.path.dirname(os.path.abspath(__file__))

#     # Construct the path to the .env file in the root directory
#     env_path = os.path.join(current_directory, '..', '.env')

#     # Load the .env file
#     load_dotenv(dotenv_path=env_path)

#     # Read the environment variable
#     value = os.getenv(variable_name, default=default)
    
#     if value is None:
#         raise ValueError(f"{variable_name} is not defined in the .env file.")
#     return value


def read_csv(csv_file='city-list.csv'):
    city_list = []

    try:
        # Open the CSV file for reading
        with open(csv_file, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                city_list.append(row)
    except FileNotFoundError:
        print(f"Error: The CSV file '{csv_file}' was not found.")
    except Exception as e:
        print(f"An error occurred while reading the CSV file: {e}")

    return city_list

# Define a delivery callback function to handle delivery reports
def delivery_report(err, msg):
    if err is not None:
        print(f'Message delivery failed: {err}')
    else:
        print(f'Message delivered to {msg.topic()} [{msg.partition()}] at offset {msg.offset()}')

def send_to_kafka(producer, topic, message, key):
    message = json.dumps(message)
    producer.produce(topic, key=None, value=message, callback=delivery_report)
    producer.flush()