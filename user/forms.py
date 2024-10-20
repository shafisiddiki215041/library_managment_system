from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from .models import Account

class RegistrationForm(UserCreationForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'id':'required'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'id':'required'}))

    class Meta:
        model = User
        fields =['username','first_name','last_name','email']

    def save(self, commit=True):
        our_user = super().save(commit=False)

        if commit:
            our_user.save()

            Account.objects.create(
                user = our_user,
                balance =0
            )
        return our_user

