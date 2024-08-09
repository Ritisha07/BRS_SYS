from django.shortcuts import render,redirect
from django.shortcuts import render, get_object_or_404
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

from django.db.models import Q
from django.shortcuts import render
from .models import Book

def search_books(request):
    query = request.GET.get('query', '')
    print(f"Search query: {query}")  # Debug line
    if query:
        books = Book.objects.filter(
            Q(title__icontains=query) |
            Q(author__icontains=query) |
            Q(genre__icontains=query)
        )
    else:
        books = Book.objects.all()
    
    print(f"Number of books found: {books.count()}")  # Debug line

    context = {
        'books': books,
        'search_query': query,
    }
    return render(request, 'book/search_results.html', context)



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