import paho.mqtt.client as mqtt
import json
import os

# Define the MQTT server host and topic
MQTT_HOST = "localhost"
MQTT_TOPIC = "miscale/Nils/weight"
FILE_PATH = "./input_data/weight.json"  # Change this to the path of your JSON file

# This function is called when the client successfully connects to the broker
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe(MQTT_TOPIC)

# Function to load existing data from the file
def load_data(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            return json.load(file)
    else:
        print("Failed loading file")
    return []

# Function to write data to the file
def write_data(file_path, data):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)
        
# This function is called when a message is received from the broker
def on_message(client, userdata, msg):
    print(f"Message received on topic {msg.topic}: {msg.payload.decode()}")
    # Load existing data
    data = load_data(FILE_PATH)
    print(data)
    # Append new data
    data.append(json.loads(msg.payload.decode()))
    # Write back to file
    write_data(FILE_PATH, data)
    formats_str = os.getenv('FORMATS', 'pdf')  # Default formats
    formats = [fmt.strip().lower() for fmt in formats_str.split(',')]

    # Convert the Jupyter notebook to markdown (unchanged)
    for fmt in formats:
        os.system(f"jupyter nbconvert --to {fmt} --no-prompt --TemplateExporter.exclude_input=True --output-dir='./output/{fmt}' './notebook/notebook.ipynb'")
        os.system(f"jupyter nbconvert --to {fmt} --execute --no-prompt --TemplateExporter.exclude_input=True --output-dir='./output/{fmt}' './notebook/notebook.ipynb'")

# Create an MQTT client instance
client = mqtt.Client()

# Assign the on_connect and on_message functions
client.on_connect = on_connect
client.on_message = on_message

# Connect to the MQTT broker
client.connect(MQTT_HOST, 1883, 60)

# Start the loop
client.loop_forever()
