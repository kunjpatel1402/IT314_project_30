import pymongo
import random
import string
from myApp.forms import PostIncidentForm, PostPropertyForm
from datetime import datetime

client = pymongo.MongoClient("mongodb+srv://superuser:superuser%40SWE30@swe-cluster.xxvswrz.mongodb.net/?retryWrites=true&w=majority")

# main database (switch to main database after testing only)
# db = client["swe_db"]

# test database
db = client["swe_test_db"]
user_collection = db["users"]
incident_collection = db["incident"]
property_collection = db["properties"]

incident_collection.delete_many({})
property_collection.delete_many({})

for i in range(100):
    print(i)
    incident = PostIncidentForm({
        'Title': ''.join(random.choice(string.ascii_uppercase + " ") for _ in range(10)),
        'Description': ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + " " + string.punctuation) for _ in range(100)),
        'Longitude': random.uniform(-180, 180),
        'Latitude': random.uniform(-90, 90),
        'Time': datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
    }, (''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(10)))) 
    incident_collection.insert_one(incident.to_dict())
    property = PostPropertyForm({
        "Title": ''.join(random.choices(string.ascii_lowercase + ' ', k=20)),
        "Description": ''.join(random.choices(string.ascii_lowercase + ' ', k=40)),
        "Longitude": random.uniform(-180, 180),
        "Latitude": random.uniform(-90, 90),
        "Pincode": random.uniform(0, 1000000),
        "AddressLine1": ''.join(random.choices(string.ascii_lowercase + ' ', k=40)),
        "AddressLine2": ''.join(random.choices(string.ascii_lowercase + ' ', k=40)),
        "City": ''.join(random.choices(string.ascii_lowercase, k=10)),
        "State": ''.join(random.choices(string.ascii_lowercase, k=10)),
        "Country": ''.join(random.choices(string.ascii_lowercase, k=10)),
    }, ''.join(random.choices(string.ascii_lowercase + string.ascii_uppercase + string.digits, k=10)))
    property_collection.insert_one(property.to_dict())