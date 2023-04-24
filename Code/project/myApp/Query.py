import json
import pymongo
import datetime
import random
from bson.json_util import dumps

client = pymongo.MongoClient('mongodb+srv://Kris:1DwQsf8Olmj1eOhW@cluster0.hvo47if.mongodb.net/test')

'''                                      CRIME                                            '''

def insert_crime(json_data):
    db = client['project']
    collection = db['crimeData']
    crime = {
        'type': json_data['type'],
        'location': {
            'type': 'Point',
            'coordinates': [
                json_data['longitude'],
                json_data['latitude']
            ]
        },
        'pincode':json_data['pincode'],
        'city':json_data['city'],
        'locality':json_data['locality'],
        'description': json_data['description'],
        'upvotes': 0,
        'downvotes': 0,
        'date': json_data['date'],
        'is-verified': False,
        'post-by-admin': False
    }
    result = collection.insert_one(crime)
    return result.inserted_id

def search_crime_by_locality(json_data):
    db = client['project']
    collection = db['crimeData']
    loc = json_data['locality']
    crimes = collection.find({'locality':loc})
    json_d = dumps(list(crimes))
    return json_d

def search_crime_by_city(json_data):
    db = client['project']
    collection = db['crimeData']
    city = json_data['city']
    crimes = collection.find({'city':city})
    json_d = dumps(list(crimes))
    return json_d

def get_crime_within_range(json_data):
    db = client['project']
    collection = db['crimeData']
    longitude = json_data['longitude']
    latitude = json_data['latitude']

    min_longitude = longitude - 0.15
    max_longitude = longitude + 0.15
    min_latitude = latitude - 0.15
    max_latitude = latitude + 0.15
    
    query = {
        'location.coordinates.0': {
            '$gt': min_longitude,
            '$lt': max_longitude
        },
        'location.coordinates.1': {
            '$gt': min_latitude,
            '$lt': max_latitude
        }
    }
    incidents = collection.find(query)
    json_d = dumps(list(incidents))
    return json_d

# this is left
def verify_crime_incidents():
    db = client['project']
    collection = db['crimeData']
    query = {
        {
            'user-role':'normal',
            'upvotes': {
                '$gt': 100,
            }
        }
    }
    verified_crimes = collection.find(query)
    json_d = dumps(list(verified_crimes))
    return json_d

def feed_crime_posts():
    db = client['project']
    collection = db['crimeData']
    latest_entries = collection.find().sort('_id', -1).limit(20)
    json_d = dumps(list(latest_entries))
    print(json_d)
    return json_d

'''                                      PROPERTY                                            '''

def insert_property(json_data):
    db = client['project']
    collection = db['propertyData']
    property = {
        'address': {
            'address_line_1': json_data['address_line_1'],
            'address_line_2': json_data['address_line_2'],
            'city' : json_data['city'],
            'pincode': json_data['pincode'],
            'location': {
                'type': 'Point',
                'coordinates': [
                    json_data['longitude'],
                    json_data['latitude']
                ]
            },
            'state' : json_data['state'],
            'country': json_data['country'],
        },
        'crime-score':json_data['crime-score'],
        'author': json_data['author'],
        'user-role': json_data['user-role']
    }
    result = collection.insert_one(property)
    return result.inserted_id

def get_property_within_range(json_data):
    db = client['project']
    collection = db['propertyData']
    longitude = json_data['longitude']
    latitude = json_data['latitude']

    min_longitude = longitude - 0.15
    max_longitude = longitude + 0.15
    min_latitude = latitude - 0.15
    max_latitude = latitude + 0.15

    query = {
        'location.coordinates.0': {
            '$gt': min_longitude,
            '$lt': max_longitude
        },
        'location.coordinates.1': {
            '$gt': min_latitude,
            '$lt': max_latitude
        }
    }
    property = collection.find(query)
    json_d = dumps(list(property))
    return json_d


# Query all properties in a specific city
def get_properties_by_city(json_data):
    db = client['project']
    collection = db['PropertyData']
    city = json_data['city']
    properties = collection.find({'city': city})
    json_d = dumps(list(properties))
    return json_d

# Query all properties in a locality
def get_properties_by_locality(json_data):
    db = client['project']
    collection = db['PropertyData']
    loc = json_data['locality']
    properties = collection.find({'locality': loc})
    json_d = dumps(list(properties))
    return json_d

# Query properties with a crime safety percentile score greater than a specified value
def get_properties_by_crime_percentile(json_data):
    db = client['project']
    collection = db['PropertyData']
    value = json_data['value']
    properties = collection.find({'crime_safety_percentile': {'$lt': value}})
    json_d = dumps(list(properties))
    return json_d

# Query properties with a hazard safety percentile score greater than a specified value
def get_properties_by_hazard_safety_percentile(json_data):
    db = client['project']
    collection = db['PropertyData']
    value = json_data['value']
    properties = collection.find({'hazard_safety_percentile': {'$lt': value}})
    json_d = dumps(list(properties))
    return json_d

# Query properties with both crime and hazard safety percentile scores greater than specified values
def get_properties_by_crime_and_hazard_safety_percentiles(json_data):
    db = client['project']
    collection = db['PropertyData']
    crime_value = json_data['crime_value']
    hazard_value = json_data['hazard_value']
    properties = collection.find({'$and': [{'crime_safety_percentile': {'$gt': crime_value}}, {'hazard_safety_percentile': {'$gt': hazard_value}}]})
    json_d = dumps(list(properties))
    return json_d

'''                                      USER                                            '''

def insert_user(json_data):
    db = client['project']
    collection = db['userData']
    user = {
        'username': json_data['username'],
        'firstname': json_data['firstname'],
        'lastname' : json_data['lastname'],
        'email': json_data['email'],
        'password': json_data['password'],
        'DOB': json_data['DOB'],
        'address': {
            'address_line_1': '',
            'address_line_2': '',
            'city' : '',
            'pincode': '',
            'location': {
                'type': 'Point',
                'coordinates': [
                    json_data['longitude'],
                    json_data['latitude']
                ]
            },
            'state' : '',
            'country': '',
        },
        'contact': {
            'mobile_number': '',
            'instagram_handle': '',
            'twitter_handle': '',
        },
        'profile_picture': '',
        'user-role': 'normal',
    }
    result = collection.insert_one(user)
    return result.inserted_id
    
'''                                      HAZARD                                            '''

def insert_hazard(json_data):
    db = client['project']
    collection = db['hazardData']
    hazard = {
        'type': json_data['type'],
        'location': {
            'type': 'Point',
            'coordinates': [
                json_data['longitude'],
                json_data['latitude']
            ]
        },
        'pincode':json_data['pincode'],
        'city':json_data['city'],
        'locality':json_data['locality'],
        'description': json_data['description'],
        'upvotes':json_data['upvotes'],
        'downvotes':json_data['downvotes'],
        'date': json_data['date'],
        'is-verified': json_data['is-verified'],
        'author': json_data['author'],
        'user-role': json_data['user-role']
    }
    result = collection.insert_one(hazard)
    return result.inserted_id

def search_hazard_by_locality(json_data):
    db = client['project']
    collection = db['hazardData']
    loc = json_data['locality']
    hazards = collection.find({'locality':loc})
    json_d = dumps(list(hazards))
    return json_d

def search_hazard_by_city(json_data):
    db = client['project']
    collection = db['hazardData']
    city = json_data['city']
    hazards = collection.find({'city':city})
    json_d = dumps(list(hazards))
    return json_d

def get_hazard_within_range(json_data):
    db = client['project']
    collection = db['hazardData']
    longitude = json_data['longitude']
    latitude = json_data['latitude']

    min_longitude = longitude - 0.15
    max_longitude = longitude + 0.15
    min_latitude = latitude - 0.15
    max_latitude = latitude + 0.15
    # print(min_longitude,max_longitude,min_latitude,max_latitude)
    query = {
        'location.coordinates.0': {
            '$gt': min_longitude,
            '$lt': max_longitude
        },
        'location.coordinates.1': {
            '$gt': min_latitude,
            '$lt': max_latitude
        }
    }
    incidents = collection.find(query)
    json_d = dumps(list(incidents))
    return json_d

def verify_hazard_incidents():
    db = client['project']
    collection = db['hazardData']
    query = {
        {
            'user-role':'normal',
            'upvotes': {
                '$gt': 100,
            }
        }
    }
    verified_hazard = collection.find(query)
    json_d = dumps(list(verified_hazard))
    return json_d

def feed_hazard_posts():
    db = client['project']
    collection = db['hazardData']
    latest_entries = collection.find().sort('_id', -1).limit(20)
    json_d = dumps(list(latest_entries))
    return json_d
