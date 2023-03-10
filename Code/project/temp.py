import pymongo
import datetime
import pprint

conn_str = ""

client = pymongo.MongoClient(conn_str, serverSelectionTimeoutMS=5000)

client.server_info()
print("Connection Successful")

for db in client.list_databases():
    print(db)