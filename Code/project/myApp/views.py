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
        print(request.POST)
        print("here")
        form = LoginForm(request.POST)
        if form.is_valid():
            query = {"UserName": form.UserName, "Password": form.Password}
            projection = {"_id": 0, "UserName": 1}

            user = user_collection.find_one(query, projection)

            if user is not None:
                request.session['username'] = user['UserName']
                request.session.save()
                return redirect('/myApp')
            else:
                error_message = "Invalid username or password"
                print("error")
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
            if form.Password != form.ConfirmPassword:
                error_message = "Passwords do not match"
                return render(request, 'myApp/register.html', {'error_message': error_message})

            query = {"UserName": form.UserName}
            projection = {"_id": 0, "UserName": 1}

            user = user_collection.find_one(query, projection)

            if user is None:
                user_collection.insert_one(form.to_dict())
                request.session['username'] = form.UserName
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
                incident_collection.insert_one(form.to_dict())
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
                property_collection.insert_one(form.to_dict())
                return HttpResponse("Post Successful")
            else:
                #print("Here2")
                return HttpResponse("Post Failed")
        else:
            return render(request, 'myApp/PostProperty.html')
    else:
        return redirect('/myApp/login/')





def profile(request):
    username = request.session.get('username')
    if username is not None:
        user = user_collection.find_one({"UserName": username})
        #print(user)
        return render(request, 'myApp/profile.html', {'user': user})
    else:
        return redirect('/myApp/login/')


def SeePosts(request, PostID):
    username = request.session.get('username')
    if username is not None:
        if request.method == 'GET':
            post = incident_collection.find_one({"post_ID": PostID})
            author = user_collection.find_one({"UserName": post['author']})
            return render(request, 'myApp/SeePosts.html', {'post': post, 'author': author})
    else:
        return redirect('/myApp/login/')


def SeeProfiles(request, ProfileID):
    username = request.session.get('username')
    if username is not None:
        if (request.method == 'GET'):
            if user_collection.find_one({"username": ProfileID}) is not None:
                return render(request, 'myApp/SeeProfiles.html', {'username': ProfileID})
            else:
                return HttpResponse("User does not exist")
    else:
        return redirect('/myApp/login/')


def Upvote(request, PostID):
    username = request.session.get('username')
    if username is not None:
        if (request.method == 'GET'):
            query = {"post_ID": PostID}
            post = incident_collection.find_one(query)
            myuser = user_collection.find_one({"UserName": username})
            #print("here\n\n\n")
            #print(myuser)
            downvoted = myuser['downvoted']
            upvoted = myuser['upvoted']
            #print(downvoted)
            #print(upvoted)
            if (post is None) or (downvoted.get(PostID) != None):
                return HttpResponse(status = 500)
            elif upvoted.get(PostID) != None:
                new_values = {"$set": {"upvotes": post['upvotes'] - 1}}
                incident_collection.update_one(query, new_values)
                upvoted.pop(PostID)
                new_values = {"$set": {"upvoted": upvoted}}
                user_collection.update_one({"UserName": username}, new_values)
                return HttpResponse(status = 201)
            else:
                #print("upvoting")
                new_values = {"$set": {"upvotes": post['upvotes'] + 1}}
                incident_collection.update_one(query, new_values)
                upvoted[PostID] = True
                new_values = {"$set": {"upvoted": upvoted}}
                user_collection.update_one({"UserName": username}, new_values)
                return HttpResponse(status = 200)
    else:
        return redirect('/myApp/login/')
    
def Downvote(requests, PostID):
    username = requests.session.get('username')
    if username is not None:
        if (requests.method == 'GET'):
            query = {"post_ID": PostID}
            post = incident_collection.find_one(query)
            myuser = user_collection.find_one({"UserName": username})
            downvoted = myuser['downvoted']
            upvoted = myuser['upvoted']
            if (post is None) or (upvoted.get(PostID) != None):
                return HttpResponse(status = 500)
            elif downvoted.get(PostID) != None:
                new_values = {"$set": {"downvotes": post['downvotes'] - 1}}
                incident_collection.update_one(query, new_values)
                downvoted = downvoted.pop(PostID)
                new_values = {"$set": {"downvoted": downvoted}}
                user_collection.update_one({"UserName": username}, new_values)
                return HttpResponse(status = 201)
            else:
                new_values = {"$set": {"downvotes": post['downvotes'] + 1}}
                incident_collection.update_one(query, new_values)
                downvoted[PostID] = True
                new_values = {"$set": {"downvoted": downvoted}}
                user_collection.update_one({"UserName": username}, new_values)
                return HttpResponse(status = 200)
    else:
        return redirect('/myApp/login/')

def Changepassword(request):
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            query = {"UserName": form.UserName}
            user = user_collection.find_one(query)
            if user is None:
                error_message = "User does not exist"
                return render(request, 'myApp/changePassword.html', {'error_message': error_message})
            else:
                if user['DOB'] != form.DOB:
                    error_message = "Incorrect Date of Birth"
                    return render(request, 'myApp/changePassword.html', {'error_message': error_message})
                else:
                    query = {"UserName": form.UserName}
                    new_values = {"$set": {"Password": form.new_password}}
                    user_collection.update_one(query, new_values)
                    return redirect('/myApp/login/')
        else:
            error_message = "Passwords do not match"
            return render(request, 'myApp/changePassword.html', {'error_message': error_message})
    else:
        return render(request, 'myApp/changePassword.html')
    
def IncidentFeed(request):
    if (request.method == 'GET'):
        posts = list(incident_collection.find())
        username = request.session.get('username')
        user = user_collection.find_one({"UserName": username})
        #print(posts)
        return render(request, 'myApp/IncidentFeed.html', {'posts': posts, 'user': user})
    else:
        return HttpResponse("Error")
    
def PropertyFeed(request):
    if (request.method == 'GET'):
        posts = property_collection.find()
        #print(posts)
        username = request.session.get('username')
        user = user_collection.find_one({"UserName": username})
        return render(request, 'myApp/PropertyFeed.html', {'posts': posts, 'user': user})
    else:
        return HttpResponse("Error")
    