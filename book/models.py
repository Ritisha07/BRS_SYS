# models.py
from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    genre= models.CharField(max_length=200)
    description = models.TextField()
    published_date = models.DateField(blank=True, null=True)
    cover_image = models.ImageField(upload_to='cover_image/')
    
    
    def __str__(self):
        return self.title
