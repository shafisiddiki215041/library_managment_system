from django.shortcuts import render, redirect
from django.views.generic import DetailView
from . import models
from . import forms
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.utils import timezone
from transactions.models import Transaction

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
        

from transactions.views import send_transaction_email

class show_borrow_books(DetailView):
    model = models.Book
    template_name = 'user/profile.html'
    pk_url_kwarg ='id'
   
    def post(self, request, *args, **kwargs):
        print('enter')
        book = self.get_object()
        
        borrow_book = forms.Borrow_forms(data =request.POST)
        account = self.request.user.account

        if borrow_book.is_valid():
            print('enter again')
            if account.balance >= book.borrowing_price:
                new_borrow= borrow_book.save(commit =False)
                new_borrow.user = request.user
                new_borrow.book = book
                new_borrow.save()

                account.balance -= book.borrowing_price
                account.save(
                    update_fields =['balance'],
                    )
                Transaction.objects.create(
                    account=account,
                    book=book,
                    borrow=new_borrow, 
                    amount=book.borrowing_price,
                    balance_after_transaction=account.balance,
                    borrow_return=False 
                    )
                send_transaction_email(self.request.user, book.borrowing_price, "Borrow Message",'borrow_mail.html')
                messages.success(request,'Borrowed Successfully')
            else:
                messages.error(request,'There has no balance')

        return self.get(request, *args, **kwargs) 
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        purchases = models.Borrow.objects.filter(user=self.request.user)
        transactions = Transaction.objects.filter(account=self.request.user.account)
        transaction_dict = {transaction.borrow.id: transaction.balance_after_transaction for transaction in transactions if transaction.borrow}
        
        for purchase in purchases:
           purchase.balance_after_transaction = transaction_dict.get(purchase.id, 'N/A')

        context['purchases'] = purchases
        return context



def return_book(request, borrow_id):
    borrow = get_object_or_404(models.Borrow, id=borrow_id)
    user = request.user.account
    if borrow.return_date is not None:
        messages.error(request, "This book has already been returned.")
        return redirect('profile')    
    user.balance += borrow.book.borrowing_price
    user.save()
    print("Returning book:", borrow)
    print("Setting return date:", timezone.now())
    borrow.return_date = timezone.now()
    borrow.save()


    messages.success(request, 'Book returned successfully and amount refunded.')
    return redirect('profile')
