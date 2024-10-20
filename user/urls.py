from django.contrib import admin
from django.urls import path,  include
from .views import UserRegistrationView, LOGINView, LOGOUTView, Profile
from transactions.views import DepositMoneyView
from books.views import return_book

urlpatterns = [
    path('register/',UserRegistrationView.as_view(),name='register'),
    path('login/',LOGINView.as_view(),name='login'),
    path('logout/',LOGOUTView.as_view(),name='logout'),
    path('profile/',Profile.as_view(),name='profile'),
    path('deposite_money/',DepositMoneyView.as_view(),name='deposite_money'),
    path('transaction_form/',DepositMoneyView.as_view(),name='transaction_form'),
     path('books/return/<int:borrow_id>/', return_book, name='return_books'),

]
