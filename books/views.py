from django.shortcuts import render
from django.views.generic import DetailView
from . import models
from . import forms
from django.urls import reverse_lazy
from django.contrib import messages

# Create your views here.
class DetailPostView(DetailView):
    model = models.Book
    pk_url_kwarg = 'id'
    template_name = 'user/details.html'
    context_object_name ='post'
    
    def post(self, request, *args, **kwargs):
        comments_form = forms.ReviewForm(data=self.request.POST)
        post = self.get_object()
        if comments_form.is_valid():
            new_comment = comments_form.save(commit = False)
            new_comment.book = post
            new_comment.save()
        return self.get(request, *args, **kwargs) 
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.object # post model er object
        comments = post.reviews.all()
        comments_form = forms.ReviewForm()
        context['comments'] = comments
        context['comments_form'] = comments_form
        return context
        



class show_borrow_books(DetailView):
    model = models.Book
    template_name = 'user/profile.html'
    pk_url_kwarg ='id'
   
    def post(self, request, *args, **kwargs):
        print('enter')
        book = self.get_object()
        
        borrow_book = forms.Borrow_forms(data =request.POST)
       
        if borrow_book.is_valid():
            print('enter again')
            new_buy= borrow_book.save(commit =False)
            new_buy.user = request.user
            new_buy.book = book
            new_buy.save()

            messages.success(request,'Borrowed Successfully')
        print("Purchase successfully.")
        return self.get(request, *args, **kwargs) 
    
     
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # car = self.object
        context['purchases'] = models.Borrow.objects.filter(user=self.request.user)
        return context
