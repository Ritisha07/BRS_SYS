from django.shortcuts import render,redirect
<<<<<<< HEAD
from django.shortcuts import render, get_object_or_404
=======
>>>>>>> 82a77c52e0187b9e27a77a74c90d7a3553e04797
from .models import Book
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponse
# Create your views here.
def home(request):
    popular_books = Book.objects.all()  # or apply some filter to get popular books
    return render(request, 'book/home.html', {'popular_books': popular_books})

def about(request):
    return render(request,"book/about.html",{})

<<<<<<< HEAD
=======

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        
        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists')
            elif User.objects.filter(email=email).exists():
                messages.error(request, 'Email already exists')
            else:
                user = User.objects.create_user(username=username, email=email, password=password1)
                user.save()
                login(request, user)
                return redirect('home')
        else:
            messages.error(request, 'Passwords do not match')
    return render(request, 'book/register.html')

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password')
            return redirect('login')
    return render(request, 'book/login.html')
# def login(request):
#     return render(request, "book/login.html",{})
>>>>>>> 82a77c52e0187b9e27a77a74c90d7a3553e04797

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        
        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists')
            elif User.objects.filter(email=email).exists():
                messages.error(request, 'Email already exists')
            else:
                user = User.objects.create_user(username=username, email=email, password=password1)
                user.save()
                messages.success(request, 'Registration successful! Please log in.')
                return redirect('login')  # Redirect to the login page after registration
        else:
            messages.error(request, 'Passwords do not match')
    return render(request, 'book/register.html')

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password')
            return redirect('login')
    return render(request, 'book/login.html')
# def login(request):
#     return render(request, "book/login.html",{})

# views.py
from django.shortcuts import render
from .models import Book

def search_books(request):
    # Retrieve search parameters from request GET data
    title = request.GET.get('title', '')
    author = request.GET.get('author', '')
    genre = request.GET.get('genre', '')

    # Filter books based on search parameters
    books = Book.objects.all()
    if title:
        books = books.filter(title__icontains=title)
    if author:
        books = books.filter(author__icontains=author)
    if genre:
        books = books.filter(genre__icontains=genre)

    # Render the template with search results
    return render(request, 'book/search_results.html', {'books': books, 'search_params': request.GET})


def book_detail(request, id):
    book = get_object_or_404(Book, id=id)
    return render(request, 'book/book_detail.html', {'book': book})

def genre_fiction(request):
    # Logic for fiction genre
    return render(request, 'book/genre_fiction.html')

def genre_nonfiction(request):
    # Logic for non-fiction genre
    return render(request, 'book/genre_nonfiction.html')

def genre_sci_fi(request):
    return render(request, 'book/genre_sci_fi.html')