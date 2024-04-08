from datetime import datetime, timezone
import random
import pandas as pd
import os
import logging

def main():
    logging.basicConfig(level=logging.INFO, format='%(message)s')

    # List of activities borrowed from Apple Fitness
    activity_list = [
        "Stand", "Sit", "Sleep", "Walk", "Run", 
        "Cycling", "Elliptical", "Rower", "Stair Stepper", 
        "HIIT", "Hiking", "Yoga", "Functional Strength Training", 
        "Dance", "Cooldown", "Core Training", "Pilates", "Tai Chi", 
        "Swimming", "Wheelchair", "Multisport", "Kickboxing", "Other"
    ]

    selected_ids = [1]

    activity_data = []
    for activity in activity_list:

        # Randomly generate a unique ID number
        random_id = 1
        while random_id in selected_ids: 
            random_id = random.randint(20001, 20999)

        selected_ids.append(random_id)
        
        # Generate current timestamp with timezone as last update
        last_update = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')

        activity_record = {
            "activity_id": random_id,
            "activity_name": activity,
            "last_update": last_update
        }
        activity_data.append(activity_record)

    df = pd.DataFrame(activity_data)
    csv_file_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'activities.csv')
    df.to_csv(csv_file_path, index=False)
    logging.info(f"Activities data successfully created")

main()