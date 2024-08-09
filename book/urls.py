from django.conf.urls.static import static

from django.urls import path

from brs import settings
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('search/', views.search_books, name='search_books'),
    path('books/<int:id>/', views.book_detail, name='book_detail'),
    path('genre/fiction/', views.genre_fiction, name='genre_fiction'),
    path('genre/nonfiction/', views.genre_nonfiction, name='genre_nonfiction'),
    path('genre/sci-fi/', views.genre_sci_fi, name='genre_sci_fi'),
    path('SignIn/register/', views.register, name='register'),
    path('SignTn/login/', views.user_login, name='login'),
<<<<<<< HEAD
    path('book/<int:id>/', views.book_detail, name='book_details'),
=======
>>>>>>> 82a77c52e0187b9e27a77a74c90d7a3553e04797
]
