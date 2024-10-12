from django import forms
from .models import Review, Borrow


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['name','email','body','rating']

class Borrow_forms(forms.ModelForm):
    class Meta:
        model = Borrow
        fields = []

