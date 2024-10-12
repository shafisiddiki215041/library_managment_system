from django.shortcuts import render
from django.views.generic import  FormView, View, TemplateView
from django.contrib.auth import login, logout
from django.urls import reverse_lazy
from django.contrib import messages
from books.models import Book, Category

def home(request, category_slug = None):
    data = Book.objects.all()
    if category_slug is not None:        
        category = Category.objects.get(slug = category_slug)
        data = Book.objects.filter(category = category)
    categories = Category.objects.all()
    return render(request,'user/homepage.html',{'post':data,'category':categories})
