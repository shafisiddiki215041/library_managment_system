from django.shortcuts import render
from django.views.generic import  FormView, View, TemplateView
from django.contrib.auth import login, logout
from .forms import RegistrationForm
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from books.models import Borrow
from transactions.models import Transaction
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
class UserRegistrationView(FormView):
    template_name='user/register.html'
    form_class= RegistrationForm
    success_url = reverse_lazy('profile')

    def form_valid(self, form):
        user = form.save()
        messages.success(self.request, 'Account Create Successfully')
        login(self.request, user)
        return super().form_valid(form)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["type"] = 'Register'
        return context
    

class LOGINView(LoginView):
    template_name = 'user/register.html'
    # success_url = reverse_lazy('profile')
    def get_success_url(self):
        return reverse_lazy('profile')
    def form_valid(self, form):
        messages.success(self.request, 'Logged in successfully')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.success(self.request, 'Logged in information incorrect')
        return super().form_invalid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["type"] = 'Login'
        return context   

class LOGOUTView(LogoutView):
    def get_success_url(self):
        return reverse_lazy('homepage')  
      
    
class Profile(LoginRequiredMixin, TemplateView):
    template_name = 'user/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_balance'] = self.request.user.account.balance
        context['transactions'] = Transaction.objects.filter(account=self.request.user.account) 
        context['purchases'] = Borrow.objects.filter(user=self.request.user)
        return context  

