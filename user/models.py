from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Account(models.Model):
    user = models.OneToOneField(User,related_name='account', on_delete=models.CASCADE)
    balance = models.DecimalField(decimal_places=2, max_digits=12, default=0)
