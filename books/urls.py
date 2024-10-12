from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('post/<int:id>/', views.DetailPostView.as_view(),name='details'),
    path('show_borrow_books/<int:id>/', views.show_borrow_books.as_view(),name='show_borrow_books'),
]