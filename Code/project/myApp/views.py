from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from .forms import LoginForm
# Create your views here.


def index(request):
    if request.user.is_authenticated:
        return HttpResponse("Hello, world. You're at the myApp index. You are logged in as " + request.user.username)
    else:
        return HttpResponse("Hello, world. You're at the myApp index.")

def login(request):
    if (request.method == 'POST'):
        print(request.POST)
        form  = LoginForm(request.POST)
        if form.is_valid():
            Username = form.UserName
            Password = form.Password
            user = authenticate(request, username = Username, password=Password)
            if user is not None:
                auth_login(request, user)
                return redirect('/myApp')
            else:
                return HttpResponse("Login Failed!!")
        else:
            return HttpResponse("Login Failed")
    else:
        return render(request, 'myApp/login.html')
    
def logout(request):
    auth_logout(request)
    return redirect('/myApp')