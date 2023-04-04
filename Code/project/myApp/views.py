from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from .forms import LoginForm, RegisterationForm, PostIncidentForm, PostPropertyForm
from apscheduler.schedulers.background import BackgroundScheduler
import pymongo
import math
# Create your views here.


client = pymongo.MongoClient(
    "mongodb+srv://superuser:superuser%40SWE30@swe-cluster.xxvswrz.mongodb.net/?retryWrites=true&w=majority")

# main database (switch to main database after testing only)
# db = client["swe_db"]

# test database
db = client["swe_test_db"]
user_collection = db["users"]


def index(request):
    if request.user.is_authenticated:
        return HttpResponse("Hello, world. You're at the myApp index. You are logged in as " + request.user.username)
    else:
        return redirect('/myApp/login/')


def login(request):
    if (request.method == 'POST'):
        print(request.POST)
        form = LoginForm(request.POST)
        if form.is_valid():
            Username = form.UserName
            Password = form.Password
            if User.objects.filter(username=Username).exists():
                user = authenticate(request, username=Username, password=Password)
                if user is not None:
                    auth_login(request, user)
                    return redirect('/myApp')
                else:
                    return HttpResponse("Login Failed!!")
            else:
                return HttpResponse("User does not exist")
        else:
            return HttpResponse("Login Failed enter valid credentials")
    else:
        return render(request, 'myApp/login.html')


def register(request):
    if (request.method == 'POST'):
        print(request.POST)
        form = RegisterationForm(request.POST)
        if form.is_valid():
            print("Here")
            Username = form.UserName
            Password = form.Password
            LastName = form.LastName
            FirstName = form.FirstName
            Email = form.Email
            if User.objects.filter(username=Username).exists():
                return HttpResponse("User already exists")
            else:
                user = User.objects.create_user(username=Username, password=Password)
                user.last_name = LastName
                user.first_name = FirstName
                user.email = Email
                user.save()
                print("User created")
                return redirect('/myApp')
        else:
            print("Here2")
            return HttpResponse("Registration Failed")
    else:
        return render(request, 'myApp/register.html')


def logout(request):
    auth_logout(request)
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



scheduler = BackgroundScheduler()
scheduler.add_job(hourly_function(), 'interval', hours=1)
scheduler.start()







def PostIncident(request):
    if request.user.is_authenticated:
        if (request.method == 'POST'):
            print(request.POST)
            form = PostIncidentForm(request.POST, request.user.username)
            if form.is_valid():
                # call the score function here
                hourly_function()
                return HttpResponse("Post Successful")
            else:
                print("Here2")
                return HttpResponse("Post Failed")
        else:
            return render(request, 'myApp/postIncident.html')
    else:
        return redirect('/myApp/login/')


def PostProperty(request):
    if request.user.is_authenticated:
        if (request.method == 'POST'):
            print(request.POST)
            form = PostPropertyForm(request.POST, request.user.username)
            if form.is_valid():
                #call the score function here
                calculate_score()
                return HttpResponse("Post Successful")
            else:
                print("Here2")
                return HttpResponse("Post Failed")
        else:
            return render(request, 'myApp/postProperty.html')
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
