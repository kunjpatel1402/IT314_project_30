import pymongo
from flask import Flask  
from flask_pymongo import PyMongo

 
app = Flask(__name__)  
app.config
 
if __name__ == '__main__':  
        app.run() 


client = pymongo.MongoClient("mongodb+srv://superuser:superuser%40SWE30@swe-cluster.xxvswrz.mongodb.net/?retryWrites=true&w=majority")

mydb = client["swe_test_db"]
mycol = mydb["properties"]

prop = []

tbl="<tr><td>Title</td><td>Description</td><td>Longitude</td><td>Latitude</td><td>Score</td><td>Pincode</td><td>City</td><td>State</td><td>Country</td><td>Addressline1</td><td>Addressline2</td></tr>"
prop.append(tbl)

for y in mycol.find():
    a = "<tr><td>%s</td>"%y['title']
    prop.append(a)
    b = "<td>%s</td>"%y['description']
    prop.append(b)
    c = "<td>%s</td></tr>"%y['longitude']
    prop.append(c)
    d = "<tr><td>%s</td>"%y['latitude']
    prop.append(d)
    e = "<td>%s</td>"%y['score']
    prop.append(e)
    f = "<td>%s</td></tr>"%y['pincode']
    prop.append(f)
    g = "<tr><td>%s</td>"%y['city']
    prop.append(g)
    h = "<td>%s</td>"%y['state']
    prop.append(h)
    i = "<td>%s</td></tr>"%y['country']
    prop.append(i)
    j = "<td>%s</td>"%y['address_line1']
    prop.append(j)
    k = "<td>%s</td></tr>"%y['address_line2']
    prop.append(k)'



