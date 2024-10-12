from django.contrib import admin
from django.urls import path,  include
from .views import UserRegistrationView, LOGINView, LOGOUTView, Profile
urlpatterns = [
    path('register/',UserRegistrationView.as_view(),name='register'),
    path('login/',LOGINView.as_view(),name='login'),
    path('logout/',LOGOUTView.as_view(),name='logout'),
    path('profile/',Profile.as_view(),name='profile'),
]
