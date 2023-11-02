from confluent_kafka import Producer
import requests
import json
from prettytable import PrettyTable

topic = "user_profiles"
kafka_config = {
    "bootstrap.servers": "localhost:9092",  # Change this to your Kafka server address
}

producer = Producer(kafka_config)

# Create a table for displaying the data
table = PrettyTable()
table.field_names = ["Gender", "Name", "Location", "Email", "Username", "Date of Birth", "Phone", "Cell", "Nationality", "UUID", "Postcode"]

while True:
    try:
        response = requests.get("https://randomuser.me/api/", timeout=10)  # Adjust the timeout value as needed
        if response.status_code == 200:
            data = json.loads(response.text)
            user_data = data["results"][0]  # Assuming there is only one user in the results
            gender = user_data["gender"]
            name = f"{user_data['name']['title']} {user_data['name']['first']} {user_data['name']['last']}"
            location = f"{user_data['location']['city']}, {user_data['location']['country']}"
            email = user_data["email"]
            username = user_data["login"]["username"]
            dob = user_data["dob"]["date"]
            phone = user_data.get("phone", "")
            cell = user_data.get("cell", "")
            nationality = user_data.get("nat", "")
            uuid = user_data["login"]["uuid"]
            postcode = user_data["location"]["postcode"]

            # Add the data to the table
            table.add_row([gender, name, location, email, username, dob, phone, cell, nationality, uuid, postcode])

            # Print the table
            print(table)

            # Produce the data to Kafka
            producer.produce(topic, key="randomuser", value=json.dumps(user_data))
            producer.flush()
        else:
            print(f"Request failed with status code {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")