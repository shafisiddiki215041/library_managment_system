from django.shortcuts import render
from django.views.generic import CreateView, ListView
from .models import Transaction
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import DepositForm
from .constants import DEPOSIT
from django.contrib import messages
from user.models import Account
from django.template.loader import render_to_string
from django.core.mail import EmailMessage, EmailMultiAlternatives

# Create your views here.
def send_transaction_email(user, amount, subject, template):
    
        message = render_to_string(template,{
            'user' : user,
            'amount': amount
        })
        send_email = EmailMultiAlternatives(subject,'',to=[user.email])
        send_email.attach_alternative(message,'text/html')
        send_email.send()

class TransactionCreateMaxin(LoginRequiredMixin, CreateView):
    template_name = 'transaction_form.html'
    model = Transaction
    title = ''
    success_url= reverse_lazy('transaction_form')
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        account = getattr(self.request.user, 'account', None)
        if not account:
           account, created = Account.objects.get_or_create(user=self.request.user)
        kwargs.update({
            'account': self.request.user.account,
        })
        return kwargs
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title' :self.title
        })
        return context
    
    
class DepositMoneyView(TransactionCreateMaxin):
    form_class = DepositForm
    title = 'Deposit'
    
    def get_initial(self):
        initial = {'transaction_type': DEPOSIT}
        return initial
    def form_valid(self, form):
        amount = form.cleaned_data.get('amount')
        account = self.request.user.account
        account.balance += amount
        account.save(
            update_fields =['balance'],
        )
        messages.success(self.request, f"{amount}$ was deposited to your account successfully")
        
        send_transaction_email(self.request.user, amount, "Deposite Message",'deposite_mail.html')
        return super().form_valid(form)