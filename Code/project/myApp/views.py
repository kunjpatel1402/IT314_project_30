from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from .forms import LoginForm, RegisterationForm, PostIncidentForm, PostPropertyForm, ChangePasswordForm
#from apscheduler.schedulers.background import BackgroundScheduler
import pymongo
import math
import sys, os


client = pymongo.MongoClient("mongodb+srv://superuser:superuser%40SWE30@swe-cluster.xxvswrz.mongodb.net/?retryWrites=true&w=majority")

# main database (switch to main database after testing only)
# db = client["swe_db"]

# test database
db = client["swe_test_db"]
user_collection = db["users"]
incident_collection = db["incident"]
property_collection = db["properties"]


def index(request):
    username = request.session.get('username')
    if username is not None:
        return render(request, 'myApp/reg_hmpg.html')
    else:
        return render(request, 'myApp/unreg_hmpg.html')


def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            query = {"username": form.UserName, "password": form.Password}
            projection = {"_id": 0, "username": 1}

            user = user_collection.find_one(query, projection)

            if user is not None:
                request.session['username'] = user['username']
                request.session.save()
                return redirect('/myApp')
            else:
                error_message = "Invalid username or password"
                return render(request, 'myApp/login.html', {'error_message': error_message})
        else:
            error_message = "Enter credentials"
            return render(request, 'myApp/login.html', {'error_message': error_message})
    else:
        return render(request, 'myApp/login.html')


def register(request):
    if request.method == 'POST':
        #print(request.POST)
        form = RegisterationForm(request.POST)
        if form.is_valid():
            query = {"username": form.UserName}
            projection = {"_id": 0, "username": 1}

            user = user_collection.find_one(query, projection)

            if user is None:
                new_user = {
                    "username": form.UserName,
                    "password": form.Password,
                    "first_name": form.FirstName,
                    "last_name": form.LastName,
                    "email": form.Email,
                    "dob": form.DOB
                }
                user_collection.insert_one(new_user)
                request.session['username'] = new_user['username']
                request.session.save()
                return redirect('/myApp')
            else:
                error_message = "Username already exists"
                return render(request, 'myApp/register.html', {'error_message': error_message})
    else:
        return render(request, 'myApp/register.html')


def logout(request):
    request.session.flush()
    return redirect('/myApp')


def calc_distance(lat1, long1, lat2, long2):
    R = 6371  # Earth's radius in kilometers
    lat1, long1, lat2, long2 = map(math.radians, [lat1, long1, lat2, long2])
    dlat = lat2 - lat1
    dlong = long2 - long1
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlong / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    d = R * c
    return d


def hourly_function():
    #This function will retrieve all the incidents present till current time
    #Also all properties present till the current time
    #It will create two dictionaries 'INC' and 'PROP', where all the respective data is stored
    #Next retrieve the needed data for incident = {longitude, latitude, time, coefficient}
    #Same goes for property = {longitude, latitude}
    # Call calculate_score

    db2 = client["swe_test_db"]
    INC = db2["incidents"]

    incident_list = []

    for post in INC.find():
        longitude1 = post['Longitude']
        latitude1 = post['Latitude']
        coeff = post['Incident_type']
        # retrieve incident time
        # retrieve post id

        incident_data = {'Longitude':longitude1, 'Latitude':latitude1, 'Incident_type':coeff}
        incident_list.append(incident_data)

    db3 = client["swe_test_db"]
    PROP = db3["properties"]


    property_list = []

    for post in PROP.find():
        longitude2 = post['Longitude']
        latitude2 = post['Latitude']
        # retrieve property id
        # retrieve score


        property_data = {'Longitude': longitude2, 'Latitude': latitude2, 'Score':prop_score}
        property_list.append(property_data)

    calculate_score(property_list, incident_list)


def calculate_score(property_list, incident_list):
    #The function is based on following formula:
    # (SIGMA(Ci * exp(-k1 * ti) * exp(-k2 * di))) / SIGMA(Ci * exp(-k1 * ti)) * 100
    # di = distance difference
    # ti = time difference

    k1 = 5
    k2 = 12

    for property_data in property_list:
        longitude1 = property_data['Longitude']
        latitude1 = property_data['Latitude']
        # get score variable

        numerator = 0
        denominator = 0

        for incident_data in incident_list:
            longitude2 = post['Longitude']
            latitude2 = post['Latitude']
            coeff = post['Incident_type']
            # retrieve incident time
            # retrieve post id

            di = calc_distance(latitude1, longitude1, latitude2, longitude2)
            # calculate time difference ti
            ti = 0

            numerator += coeff*exp(-k1*ti)*exp(-k2*di)
            denominator += coeff*exp(-k2*ti)

        score = (numerator/denominator)*100

        # store the score in the database for this property using property_id



# scheduler = BackgroundScheduler()
# scheduler.add_job(hourly_function(), 'interval', hours=1)
# scheduler.start()







def PostIncident(request):
    username = request.session.get('username')
    #print(username)
    if username is not None:
        if (request.method == 'POST'):
            #print(request.POST)
            form = PostIncidentForm(request.POST, username)
            if form.is_valid():
                # call the score function here
                #hourly_function()
                new_incident = {
                    "author": form.author,
                    "title": form.title,
                    "description": form.description,
                    "longitude": form.longitude,
                    "latitude": form.latitude,
                    "post_id": form.post_ID,
                    "incident_type": form.incident_type,
                    "time": form.time
                }
                incident_collection.insert_one(new_incident)
                return HttpResponse("Post Successful")
            else:
                #print("Here2")
                return HttpResponse("Post Failed")
        else:
            return render(request, 'myApp/postIncident.html')
    else:
        return redirect('/myApp/login/')

def PostProperty(request):
    username = request.session.get('username')
    #print(username)
    if username is not None:
        if (request.method == 'POST'):
            #print(request.POST)
            form = PostPropertyForm(request.POST, username)
            if form.is_valid():
                # call the score function here
                #hourly_function()
                new_property = {
                    "author": form.author,
                    "title": form.title,
                    "description": form.description,
                    "longitude": form.longitude,
                    "latitude": form.latitude,
                    "score": form.score,
                    "pincode": form.pincode,
                    "address_line1": form.address_line1,
                    "address_line2": form.address_line2,
                    "city": form.city,
                    "state": form.state,
                    "country": form.country,
                    "post_ID": form.post_ID,
                }
                property_collection.insert_one(new_property)
                return HttpResponse("Post Successful")
            else:
                #print("Here2")
                return HttpResponse("Post Failed")
        else:
            return render(request, 'myApp/PostProperty.html')
    else:
        return redirect('/myApp/login/')





def profile(request):
    if request.user.is_authenticated:
        return render(request, 'myApp/profile.html', {'username': request.user.username})
    else:
        return redirect('/myApp/login/')


def SeePosts(requests, PostID):
    if requests.user.is_authenticated:
        if requests.method == 'GET':
            return render(requests, 'myApp/SeePosts.html', {'PostID': PostID})
    else:
        return redirect('/myApp/login/')


def SeeProfiles(requests, ProfileID):
    if requests.user.is_authenticated:
        if (requests.method == 'GET'):
            if (User.objects.filter(username=ProfileID).exists()):
                return render(requests, 'myApp/SeeProfiles.html', {'username': ProfileID})
            else:
                return HttpResponse("User does not exist")
    else:
        return redirect('/myApp/login/')


def Changepassword(request):
    if (request.method == 'POST'):
        #print(request.POST)
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            query = {"username": form.UserName}
            projection = {"_id": 0, "username": 1}
            user_ = user_collection.find_one(query, projection)
            if user_ is None:
                return HttpResponse("User does not exist" + form.UserName)
            else:
                query = {"DOB": form.DOB}
                projection = {"_id": 0, "username": 1}
                user_ = user_collection.find_one(query, projection)
                if user_ is None:
                    return HttpResponse("Incorrect DOB")
                else:
                    #change password
                    return HttpResponse("Password Changed")
        else:
            #print("Here2")
            error_message = "Passwords in both fields do not match"
            return render(request, 'myApp/changePassword.html', {'error_message': error_message})
    else:
        return render(request, 'myApp/changePassword.html')