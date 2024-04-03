import fastavro
import json

# Mock data to be stored as AVRO and JSON file
data = {
    "userid": 10001,
    "heart_rate": 128,
    "timestamp": 1711943972,
    "meta": {
        "activityid": 2345,
        "location": {"latitude": 37.416834, "longitude": -121.975002}
    }
}

avro_schema = {
    "type": "record",
    "name": "UserData",
    "fields": [
        {"name": "userid", "type": "int"},
        {"name": "heart_rate", "type": "int"},
        {"name": "timestamp", "type": "int"},
        {
            "name": "meta",
            "type": {
                "type": "record",
                "name": "MetaInfo",
                "fields": [
                    {"name": "activityid", "type": "int"},
                    {
                        "name": "location",
                        "type": {
                            "type": "record",
                            "name": "LocationInfo",
                            "fields": [
                                {"name": "latitude", "type": "float"},
                                {"name": "longitude", "type": "float"}
                            ]
                        }
                    }
                ]
            }
        }
    ]
}

# Write Avro data to a file
with open("data.avro", "wb") as avro_file:
    fastavro.writer(avro_file, avro_schema, [data])

# Serialize dictionary object to JSON format
json_string = json.dumps(data, indent=4)

# Write JSON data to a file
with open("data.json", "w") as json_file:
    json_file.write(json_string)
