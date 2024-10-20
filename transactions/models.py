from django.db import models
from .constants import TRANSACTION_TYPE
from user.models import Account
from books.models import Book , Borrow

# Create your models here.

class Transaction(models.Model):
    account = models.ForeignKey(Account, related_name='transactions',on_delete=models.CASCADE)
    amount = models.DecimalField(decimal_places=2,max_digits=12)
    balance_after_transaction = models.DecimalField(decimal_places=2, max_digits=12)
    transaction_type = models.IntegerField(choices=TRANSACTION_TYPE,null=True)
    timestamp =models.DateTimeField(auto_now_add=True)
    borrow_return = models.BooleanField(default=False)
    book = models.ForeignKey(Book, null=True, blank=True, on_delete=models.SET_NULL)
    borrow = models.ForeignKey(Borrow, on_delete=models.SET_NULL, null=True, blank=True)
    
    class Meta:
        ordering = ['timestamp']

