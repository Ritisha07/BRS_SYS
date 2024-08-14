from django.conf.urls.static import static
from django.urls import path
from django.conf import settings
from . import views

urlpatterns = [
    # Home and About
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),

    # Search
    path('search/', views.search_books, name='search_books'),

    # Genre URLs
    # path('genre/fiction/', views.genre_fiction, name='genre_fiction'),
    # path('genre/nonfiction/', views.genre_nonfiction, name='genre_nonfiction'),
    # path('genre/sci-fi/', views.genre_sci_fi, name='genre_sci_fi'),

    # Authentication
    path('SignIn/register/', views.register, name='register'),
    path('SignIn/login/', views.user_login, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Book Details and Reviews
    path('book/<int:id>/book_detail', views.book_detail, name='book_details'),
    path('book/<int:id>/add_review/', views.add_review, name='add_review'),
    # path('review/<int:review_id>/edit_review/', views.edit_review, name='edit_review'),
    path('review/<int:review_id>/edit_review/', views.edit_review, name='edit_review'),

    # Genre Search
    path('genre/<str:genre>/', views.genre_search, name='genre_search'),
    
    
    
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)