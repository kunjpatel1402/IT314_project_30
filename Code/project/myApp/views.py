from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from .forms import LoginForm, RegisterationForm
import pymongo
# Create your views here.


client = pymongo.MongoClient("mongodb+srv://superuser:superuser%40SWE30@swe-cluster.xxvswrz.mongodb.net/?retryWrites=true&w=majority")

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
        form  = LoginForm(request.POST)
        if form.is_valid():
            Username = form.UserName
            Password = form.Password
            if User.objects.filter(username=Username).exists():
                user = authenticate(request, username = Username, password=Password)
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
        form  = RegisterationForm(request.POST)
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