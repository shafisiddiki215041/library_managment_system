from django.db import models
from catagories.models import Category
from django.contrib.auth.models import User

# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    category = models.ManyToManyField(Category, related_name='books') 
    borrowing_price = models.DecimalField(max_digits=6, decimal_places=2)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='books/media/uploads/', blank =True, null = True)

    def __str__(self):
        return self.title
    
class Review(models.Model):
    book = models.ForeignKey(Book,related_name='reviews', on_delete=models.CASCADE)
    rating = models.IntegerField(null=False)
    name = models.CharField(max_length=30)
    email = models.EmailField()
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Commentes by {self.name}"


class Borrow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrrow_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.book.title