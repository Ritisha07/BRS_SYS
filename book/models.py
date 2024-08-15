# models.py
from django.db import models
from django.contrib.auth.models import User

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    genre= models.CharField(max_length=200)
    description = models.TextField()
    published_date = models.DateField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    cover_image = models.ImageField(upload_to='cover_image/')
    
    def __str__(self):
        return self.title
    
class Review(models.Model):
    book = models.ForeignKey('Book', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)  # 1-5 stars
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"Review by {self.user.username}"

    
