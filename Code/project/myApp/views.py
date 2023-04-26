from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from .forms import LoginForm, RegisterationForm, PostIncidentForm, PostPropertyForm, ChangePasswordForm
from django.http import JsonResponse
from .forms import LoginForm, RegisterationForm, PostIncidentForm, PostPropertyForm, ChangePasswordForm , EditDetailsForm
#from apscheduler.schedulers.background import BackgroundScheduler
import pymongo
from django.test import Client
import math
import sys, os
# import datetime
from datetime import datetime
from subprocess import Popen, PIPE
from threading import Thread

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
    Thread(target=hourly_function).start()
    # response = Client().post('/appforcelery/')   
    # print(response)
    if username is not None:
        return render(request, 'myApp/reg_hmpg.html', {'user': username})
    else:
        return render(request, 'myApp/unreg_hmpg.html', {'user': None})

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

    # db2 = client["swe_test_db"]
    # INC = db2["incident"]

    incident_list = list(incident_collection.find())

    # for post in incident_collection.find():
    #     longitude1 = post['longitude']
    #     latitude1 = post['latitude']
    #     coeff = post['incident_type']
    #     thattime = post['time']# retrieve incident time
    #     postid = post['post_ID']# retrieve post id

    #     incident_data = {'longitude':longitude1, 'latitude':latitude1, 'incident_type':coeff, 'time':thattime, 'post_ID':postid}
    #     incident_list.append(incident_data)
    #print(incident_list, file=open('incident_list.txt', 'w'))
    # db3 = client["swe_test_db"]
    # PROP = db3["properties"]


    property_list = list(property_collection.find())

    # for post in property_collection.find():
    #     longitude2 = post['longitude']
    #     latitude2 = post['latitude']
    #     prop_score = post['score']# retrieve score
    #     prop_id = post['post_ID']# retrieve property id
        


    #     property_data = {'longitude': longitude2, 'latitude': latitude2, 'score':prop_score, 'post_ID':prop_id}
    #     property_list.append(property_data)
    #print(property_list, file=open('property_list.txt', 'w'))
    calculate_score(property_list, incident_list)


def calculate_score(property_list, incident_list):
    #The function is based on following formula:
    # (SIGMA(Ci * exp(-k1 * ti) * exp(-k2 * di))) / SIGMA(Ci * exp(-k1 * ti)) * 100
    # di = distance difference
    # ti = time difference

    k1 = 1
    k2 = 1

    for property_data in property_list:
        longitude1 = property_data['longitude']
        latitude1 = property_data['latitude']
        prop_score = property_data['score']# get score variable

        numerator = 0
        denominator = 0

        for incident_data in incident_list:
            longitude2 = incident_data['longitude']
            latitude2 = incident_data['latitude']
            coeff = incident_data['incident_type']
            thattime = incident_data['time']# retrieve incident time
            postid = incident_data['post_ID']# retrieve post id

            di = calc_distance(latitude1, longitude1, latitude2, longitude2)
            # calculate time difference ti
            current_time = datetime.utcnow().isoformat()
            curdt = datetime.fromisoformat(current_time)
            thatdt = datetime.fromisoformat(thattime)
            
            monthdiff = curdt.month - thatdt.month
            daydiff = curdt.day - thatdt.day
            hourdiff = curdt.hour - thatdt.hour

            ti = monthdiff*30*24 + daydiff*24 + hourdiff    # May need to modify

            numerator += math.exp(-k1*ti)*math.exp(-k2*di)    #removed coeff
            denominator += math.exp(-k2*ti)               #removed coeff

        prop_score = (numerator/denominator)*100
        # prop_score = 1234
        # property_data['score'] = 1234
        property_data['score'] = prop_score
        # store the score in the database for this property using property_id
        
        # for prop_id, prop_score in property_list:
        #property_collection.update_one({'post_ID': property_data['post_ID']}, {'$set': {'score': prop_score}})
    property_list = sorted(property_list, key=lambda d: d['score'])
    length = len(property_list)
    for i in range(len(property_list)):
        property_list[i]['score'] = ((i+1.0)/length)*100
    for property_data in property_list:
        property_collection.update_one({'post_ID': property_data['post_ID']}, {'$set': {'score': property_data['score']}})



# scheduler = BackgroundScheduler()
# scheduler.add_job(hourly_function(), 'interval', hours=1)
# scheduler.start()




def PostIncident(request):
    username = request.session.get('username')
    #print(username)
    if username is not None:
        if (request.method == 'POST'):  
            print(request.POST)
            form = PostIncidentForm(request.POST, username)
            if form.is_valid():
                incident_collection.insert_one(form.to_dict())
                return redirect('/myApp')
            else:
                #print("Here2")
                return HttpResponse("Post Failed")
        else:
            return render(request, 'myApp/postIncident.html', {'user': username})
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
                return redirect('/myApp')
            else:
                #print("Here2")
                return HttpResponse("Post Failed")
        else:
            return render(request, 'myApp/PostProperty.html', {'user': username})
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
    
def editprofile(request):
    username = request.session.get('username')
    print("here-----------------")
    if username is not None:
        if (request.method == 'POST'):
            print(request.POST)
            form = EditDetailsForm(request.POST)
            if form.is_valid():
                user_collection.update_one({"UserName": username}, {"$set": form.to_dict()})
                return redirect('/myApp/profile/')
            else:
                return HttpResponse("Profile Update Failed")
        else:
            user = user_collection.find_one({"UserName": username})
            return render(request, 'myApp/EditDetails.html', {'user': user})
    else:
        return redirect('/myApp/login/')




def SeeProfiles(request, ProfileID):
    username = request.session.get('username')
    if username is not None:
        if (request.method == 'GET'):
            user = user_collection.find_one({"UserName": ProfileID})
            if user is not None:
                return render(request, 'myApp/SeeProfile.html', {'user': user})
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
            curr = post['upvotes'] - post['downvotes']
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
                return JsonResponse({"status": "neutral", "votes": curr-1})
            else:
                #print("upvoting")
                new_values = {"$set": {"upvotes": post['upvotes'] + 1}}
                incident_collection.update_one(query, new_values)
                upvoted[PostID] = True
                new_values = {"$set": {"upvoted": upvoted}}
                user_collection.update_one({"UserName": username}, new_values)
                return JsonResponse({"status": "upvoted", "votes": curr+1})
    else:
        return redirect('/myApp/login/')

def find_post(PostID):
    query = {"post_ID": PostID}
    post = incident_collection.find_one(query)
    return post

def find_user(username):
    myuser = user_collection.find_one({"UserName": username})
    return myuser

def Downvote(requests, PostID):
    username = requests.session.get('username')
    if username is not None:
        if (requests.method == 'GET'):
            query = {"post_ID": PostID}
            post = find_post(PostID)
            curr = post['upvotes'] - post['downvotes']
            myuser = find_user(username)
            downvoted = myuser['downvoted']
            upvoted = myuser['upvoted']
            if (post is None) or (upvoted.get(PostID) != None):
                return HttpResponse(status = 500)
            elif downvoted.get(PostID) != None:
                new_values = {"$set": {"downvotes": post['downvotes'] - 1}}
                incident_collection.update_one(query, new_values)
                downvoted.pop(PostID)
                new_values = {"$set": {"downvoted": downvoted}}
                user_collection.update_one({"UserName": username}, new_values)
                return JsonResponse({"status": "neutral", "votes": curr+1})
            else:
                new_values = {"$set": {"downvotes": post['downvotes'] + 1}}
                incident_collection.update_one(query, new_values)
                downvoted[PostID] = True
                new_values = {"$set": {"downvoted": downvoted}}
                user_collection.update_one({"UserName": username}, new_values)
                return JsonResponse({"status": "downvoted", "votes": curr-1})
    else:
        return redirect('/myApp/login/')

def Changepassword(request):
    username = request.session.get('username')
    if username is not None:
        if request.method == 'POST':
            form = ChangePasswordForm(request.POST)
            if form.is_valid():
                query = {"UserName": form.UserName}
                user = user_collection.find_one(query)
                if user is None:
                    error_message = "User does not exist"
                    return render(request, 'myApp/changePassword.html', {'error_message': error_message},{'user':username})
                else:
                    if user['DOB'] != form.DOB:
                        error_message = "Incorrect Date of Birth"
                        return render(request, 'myApp/changePassword.html', {'error_message': error_message},{'user':username})
                    else:
                        query = {"UserName": form.UserName}
                        new_values = {"$set": {"Password": form.new_password}}
                        user_collection.update_one(query, new_values)
                        return redirect('/myApp/login/')
            else:
                error_message = "Passwords do not match"
                return render(request, 'myApp/changePassword.html', {'error_message': error_message},{'user':username})
        else:
            return render(request, 'myApp/changePassword.html',{'user':username})
    else:
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
        print(user)
        return render(request, 'myApp/IncidentFeed.html', {'posts': posts, 'user': user})
    else:
        return HttpResponse("Error")
    
def PropertyFeed(request):
    if (request.method == 'GET'):
        posts = property_collection.find().sort("score", 1)
        #print(posts)
        username = request.session.get('username')
        user = user_collection.find_one({"UserName": username})
        return render(request, 'myApp/PropertyFeed.html', {'posts': posts, 'user': user})
    else:
        return HttpResponse("Error")
    
def SearchIncident(request):
    username = request.session.get('username')
    if username is not None:
        if (request.method == 'POST'):
            prompt = request.POST['prompt']
            print("prompt: " + prompt)
            posts = incident_collection.find({'$text': {'$search':prompt}},{ 'score': { '$meta': "textScore" } })
            posts.sort([('score', {'$meta': 'textScore'})])
            posts = list(posts)
            #print(posts)
            return render(request, 'myApp/IncidentFeed.html', {'posts': posts})
        else:
            return HttpResponse("Error")
    else:
        return redirect('/myApp/login/')
    
    
def SearchProperty(request):
    username = request.session.get('username')
    if username is not None:
        if (request.method == 'POST'):
            prompt = request.POST['prompt']
            print("prompt: " + prompt)
            posts = property_collection.find({'$text': {'$search':prompt}},{ 'score': { '$meta': "textScore" } })
            posts.sort([('score', {'$meta': 'textScore'})])
            posts = list(posts)
            #print(posts)
            return render(request, 'myApp/PropertyFeed.html', {'posts': posts})
        else:
            return HttpResponse("Error")
    else:
        return redirect('/myApp/login/')
    
def myPost(request):
    username = request.session.get('username')
    if username is not None:
        if (request.method == 'GET'):
            posts = incident_collection.find({'author': username})
            posts = list(posts)
            #print(posts)
            return render(request, 'myApp/IncidentFeed.html', {'posts': posts})
        else:
            return HttpResponse("Error")
    else:
        return redirect('/myApp/login/')