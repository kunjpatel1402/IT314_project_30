from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('register/', views.register, name='register'),
    path('post/', views.post, name='post'),
    path('profile/', views.profile, name='profile'),
    path('seepost/<str:PostID>', views.SeePosts, name='SeePosts'),
    path('seeprofile/<str:ProfileID>', views.SeeProfiles, name='SeeProfiles')
]