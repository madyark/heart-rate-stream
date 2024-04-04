from confluent_kafka import Producer
import random
import pandas as pd
import time
from faker import Faker
import os
import json
import sys
from dotenv import load_dotenv

def read_config():
    """Reads the client configuration from client.properties and returns it as a key-value map"""
    config = {}
    with open("client.properties") as fh:
        for line in fh:
            line = line.strip()
            if len(line) != 0 and line[0] != "#":
                parameter, value = line.strip().split('=', 1)
                config[parameter] = value.strip()
    return config

def delivery_callback(err, msg):
    """Callback function to handle message delivery status of the stream"""
    if err:
        sys.stderr.write('%% Message failed delivery: %s\n' % err)
    else:
        sys.stderr.write('%% Message delivered to %s [%d] @ %d\n' % 
                         (msg.topic(), msg.partition(), msg.offset()))

def read_csv_file(file_path: str) -> pd.DataFrame:
    """Load CSV file into a pandas DataFrame"""
    return pd.read_csv(file_path)

def main():
    load_dotenv()
    config = read_config()
    topic = os.environ.get('CONFLUENT_TOPIC')

    # Create a new producer instance
    producer = Producer(config)

    # Navigate to the mock-data parent directory to load CSV files
    mock_data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

    activities_csv_path = os.path.join(mock_data_dir, 'static', 'data', 'activities.csv')
    users_csv_path = os.path.join(mock_data_dir, 'static', 'data', 'users.csv')

    activities_df = read_csv_file(activities_csv_path)
    users_df = read_csv_file(users_csv_path)

    # Create a Faker instance
    fake = Faker()

    try:
        while True:
            # Select a user based on the previously-generated mock data
            user_id = random.choice(users_df['userid'])
            user_country = users_df.loc[users_df['userid'] == user_id, 'address_country_code'].iloc[0]

            # Select an activity based on the previously-generated mock data
            activity_id = random.choice(activities_df['activity_id'])
            activity_name = activities_df.loc[activities_df['activity_id'] == activity_id, 'activity_name'].iloc[0]
            
            # Select latitude and longitude coordinates based on user's address country
            latlng = fake.local_latlng(country_code=user_country)

            # Generate heart rate based on activity type
            if activity_name in ["Stand", "Sit", "Sleep"]:
                heart_rate = random.randint(40, 80)
            elif activity_name in ["Run", "HIIT", "Swimming", "Kickboxing", "Multisport"]:
                heart_rate = random.randint(130, 205)
            else:
                heart_rate = random.randint(70, 150)

            # Have the sensor emit a random amount of heart rate readings for the user within a small time period
            sensor_readings = random.randint(1, 4)

            for i in range(sensor_readings):
                heart_rate = random.randint(round(heart_rate * 0.95), round(heart_rate * 1.1)) # Heart rate will change slightly each time

                current_epoch_time = int(time.time())

                hr_data = {
                    "user_id": str(user_id),
                    "heart_rate": str(heart_rate),
                    "timestamp": str(current_epoch_time),
                    "meta": {
                        "activity_id": str(activity_id),
                        "location": {
                            "latitude": str(latlng[0]),
                            "longitude": str(latlng[1])
                        }
                    }
                }
                
                producer.produce(
                    topic, 
                    key=json.dumps(hr_data['user_id']).encode('utf-8'), 
                    value=json.dumps(hr_data).encode('utf-8')
                )

                print(f"Produced message to topic {topic}")
                print(f"User ID: {hr_data['user_id']}")
                print(f"Heart Rate: {hr_data['heart_rate']}")
                print(f"Timestamp: {hr_data['timestamp']}\n")
                
                # Send any outstanding or buffered messages to the Kafka broker
                producer.flush()

                time.sleep(3) # Have a small gap between each sensor reading for the user

    except KeyboardInterrupt:
        # Do not print any error messages for keyboard interrupt of infinite while loop
        pass

main()