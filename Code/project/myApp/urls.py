from django.urls import path
from django.conf.urls import include
from django.contrib import admin
from . import views
from appforcelery import views as celery_views

urlpatterns = [    
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('register/', views.register, name='register'),
    path('postIncident/', views.PostIncident, name='PostIncident'),
    path('postProperty/', views.PostProperty, name='PostProperty'),
    path('profile/', views.profile, name='profile'),
    path('editprofile/', views.editprofile, name='editprofile'),
    path('seeprofile/<str:ProfileID>', views.SeeProfiles, name='SeeProfiles'),
    path('changePassword/', views.Changepassword, name='Changepassword'),
    path('upvote/<str:PostID>', views.Upvote, name='Upvote'),
    path('downvote/<str:PostID>', views.Downvote, name='Downvote'),
    path('IncidentFeed/', views.IncidentFeed, name='IncidentFeed'),
    path('PropertyFeed/', views.PropertyFeed, name='PropertyFeed'),
    path('searchIncident/', views.SearchIncident, name='SearchIncident'),
    path('searchProperty/', views.SearchProperty, name='SearchProperty'),
    path('myPosts/', views.myPost, name='myPost'),
    
    # path for celery
    path('appforcelery', include('appforcelery.urls')),
    path('', celery_views.testcelery, name='testcelery')

]