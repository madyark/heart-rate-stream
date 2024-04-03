from confluent_kafka import Producer
import random
import pandas as pd
import time
from faker import Faker
import os
import json
import sys

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
    if err:
        sys.stderr.write('%% Message failed delivery: %s\n' % err)
    else:
        sys.stderr.write('%% Message delivered to %s [%d] @ %d\n' %
                            (msg.topic(), msg.partition(), msg.offset()))

def read_csv_file(file_path: str) -> pd.DataFrame:
    """Load CSV file into a pandas DataFrame"""
    return pd.read_csv(file_path)

def main():
    
    config = read_config()
    topic = "hr-data-topic"

    # Create a new producer instance
    producer = Producer(config)

    activities_csv_path = 'mock-data/static/data/activities.csv'
    users_csv_path = 'mock-data/static/data/users.csv'

    activities_df = read_csv_file(activities_csv_path)
    users_df = read_csv_file(users_csv_path)

    # Create Faker instance
    fake = Faker()

    try:
        while True:

            user_id = random.choice(users_df['userid'])
            user_country = users_df.loc[users_df['userid'] == user_id, 'address_country_code'].iloc[0]

            activity_id = random.choice(activities_df['activity_id'])
            activity_name = activities_df.loc[activities_df['activity_id'] == activity_id, 'activity_name'].iloc[0]
            
            latlng = fake.local_latlng(country_code=user_country)

            if activity_name in ["Stand", "Sit", "Sleep"]:
                heart_rate = random.randint(40, 80)
            elif activity_name in ["Run", "HIIT", "Swimming", "Kickboxing", "Multisport"]:
                heart_rate = random.randint(130, 205)
            else:
                heart_rate = random.randint(70, 150)

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
            
            time.sleep(10) 
    
    except KeyboardInterrupt:
        pass

main()