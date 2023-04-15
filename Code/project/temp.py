import pymongo
import random
import string
client = pymongo.MongoClient("mongodb+srv://superuser:superuser%40SWE30@swe-cluster.xxvswrz.mongodb.net/?retryWrites=true&w=majority")

# main database (switch to main database after testing only)
# db = client["swe_db"]

# test database
db = client["swe_test_db"]
user_collection = db["users"]
incident_collection = db["incident"]
property_collection = db["properties"]


for i in range(100):
    print(i)
    new_property = {
        "author": ''.join(random.choices(string.ascii_lowercase, k=10)),
        "title": ''.join(random.choices(string.ascii_lowercase + ' ', k=20)),
        "description": ''.join(random.choices(string.ascii_lowercase + ' ', k=40)),
        "longitude": random.uniform(-90, 90),
        "latitude": random.uniform(-90, 90),
        "score": random.uniform(0, 100),
        "pincode": random.uniform(0, 1000000),
        "address_line1": ''.join(random.choices(string.ascii_lowercase + ' ', k=40)),
        "address_line2": ''.join(random.choices(string.ascii_lowercase + ' ', k=40)),
        "city": ''.join(random.choices(string.ascii_lowercase, k=10)),
        "state": ''.join(random.choices(string.ascii_lowercase, k=10)),
        "country": ''.join(random.choices(string.ascii_lowercase, k=10)),
        "post_ID": ''.join(random.choices(string.ascii_lowercase + string.ascii_uppercase + string.digits, k=10)),
    }
    print(new_property)
    property_collection.insert_one(new_property)