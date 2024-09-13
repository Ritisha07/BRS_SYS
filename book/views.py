from django.shortcuts import render,redirect, get_object_or_404
from .models import Book, Review, Purchase
from django.contrib.auth import login, authenticate,logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponse,JsonResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Count

def home(request):
    # Get all popular books
    popular_books = Book.objects.all()
    
    # Get recommendations if the user is authenticated
    recommendations = get_recommendations(request.user) if request.user.is_authenticated else Book.objects.none()
    
    # Prepare context
    context = {
        'popular_books': popular_books,
        'recommendations': recommendations,
        # other context variables can be added here
    }
    
    # Render the home template with the context
    return render(request, 'book/home.html', context)

# def get_recommendations(user):
#     # Get books reviewed by the user
#     user_reviews = Review.objects.filter(user=user)
#     reviewed_books_ids = set(user_reviews.values_list('book_id', flat=True))
    
#     # If the user has not reviewed any books, return no recommendations
#     if not reviewed_books_ids:
#         return Book.objects.none()

#     # Find other users who have reviewed the same books
#     similar_user_reviews = Review.objects.filter(
#         book_id__in=reviewed_books_ids
#     ).exclude(user=user)

#     # Collect book recommendations
#     recommended_books_ids = set()
#     for review in similar_user_reviews:
#         # Find books reviewed by this user that the user has not reviewed
#         other_user_reviews = Review.objects.filter(
#             user=review.user
#         ).exclude(book_id__in=reviewed_books_ids)
        
#         for other_review in other_user_reviews:
#             recommended_books_ids.add(other_review.book_id)

#     # Filter out books already reviewed by the user
#     # recommended_books_ids.difference_update(reviewed_books_ids)
    
#     # Retrieve books
#     recommended_books = Book.objects.filter(id__in=recommended_books_ids)

#     return recommended_books




# def about(request):
#     return render(request,"book/about.html",{})

def get_recommendations(user):
    # Get the user's reviews and the books they've reviewed
    user_reviews = Review.objects.filter(user=user)
    reviewed_books_ids = set(user_reviews.values_list('book_id', flat=True))

    # If the user has not reviewed any books, return no recommendations
    if not reviewed_books_ids:
        return Book.objects.none()

    # Find other users who have reviewed the same books as the current user
    similar_user_reviews = Review.objects.filter(
        book_id__in=reviewed_books_ids
    ).exclude(user=user)

    # Collect book recommendations based on reviews by similar users
    recommended_books_ids = set()
    for review in similar_user_reviews:
        # Find books reviewed by similar users that the current user has not reviewed
        other_user_reviews = Review.objects.filter(
            user=review.user
        ).exclude(book_id__in=reviewed_books_ids)

        # Add these books to the recommended list
        recommended_books_ids.update(other_user_reviews.values_list('book_id', flat=True))

    # Get the recommended books, excluding those the user already reviewed
    recommended_books = Book.objects.filter(id__in=recommended_books_ids)

    return recommended_books
def about(request):
    return render(request, "book/about.html", {})


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

def logout_view(request):
    logout(request)
    messages.success(request, 'Log Out successful! .')
    return redirect('home')

def add_review(request, id):
    book = get_object_or_404(Book, id=id)
    reviews = Review.objects.filter(book=book)
    has_reviewed = reviews.filter(user=request.user).exists() if request.user.is_authenticated else False

    if request.method == 'POST':
        if request.user.is_authenticated:
            rating = request.POST.get('rating')
            comment = request.POST.get('comment')
            if not has_reviewed:
                review = Review(book=book, user=request.user, rating=rating, comment=comment)
                review.save()
                return redirect('book_details', id=book.id)
            else:
                # Handle the case where user has already reviewed the book
                return redirect('book_details', id=book.id)
        else:
            return redirect('login')

    return render(request, 'book/add_review.html', {'book': book, 'has_reviewed': has_reviewed})

@login_required
def edit_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    
    # Check if the current user is the owner of the review
    if review.user != request.user:
        return redirect('some_error_page')  # Redirect or show an error if necessary
    
    if request.method == 'POST':
        # Update review fields directly from POST data
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')

        if rating and comment:
            review.rating = rating
            review.comment = comment
            review.save()
            return redirect('book_details', id=review.book.id)
    else:
        # For GET requests, pass the review data to the template
        context = {
            'review': review,
        }
        return render(request, 'book/edit_review.html', context)

@login_required
def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    
    # Check if the current user is the owner of the review
    if review.user != request.user:
        return redirect('some_error_page')  # Redirect or show an error if necessary
    
    if request.method == 'POST':
        review.delete()
        return redirect('book_details', id=review.book.id)
    
    # Optionally render a confirmation page for GET requests
    return render(request, 'book/delete_review.html', {'review': review})

# views.py
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
    reviews = Review.objects.filter(book=book)
    has_reviewed = reviews.filter(user=request.user).exists() if request.user.is_authenticated else False
    if request.user.is_authenticated:
        recommendations = get_recommendations(request.user)
    else:
        recommendations = None
    return render(request, 'book/book_detail.html', {'book': book, 'reviews': reviews, 'has_reviewed': has_reviewed, 'recommendations': recommendations})

def genre_search(request, genre):
    # Query books based on the genre
    books = Book.objects.filter(genre__icontains=genre)
    
    # Pass the books and search query to the template
    context = {
        'search_query': genre,
        'books': books
    }
    
    return render(request, 'book/genreSearch.html', context)

def buy_book(request, id):
    book = get_object_or_404(Book, id=id)
    
    if request.method == 'POST':
        # Example purchase logic: Create a Purchase record
        purchase = Purchase(user=request.user, book=book)
        purchase.save()
        
        # Redirect to a success page or the book details page
        # return redirect('purchase_success', id=book.id)
        messages.success(request, 'Purchase sucessfull! .')
        return redirect('home')
    elif request.method == 'GET':
        return render(request, 'book/buy.html', {'book': book})


@login_required
def favorite_books(request):
    # Get the books that the user has added to their favorites
    favorite_books = Book.objects.filter(favorites=request.user)
    
    context = {
        'favorite_books': favorite_books,
    }
    
    return render(request, 'book/favorite_books.html', context)

def add_favorite(request, id):
    book = get_object_or_404(Book, id=id)
    book.favorites.add(request.user)
    messages.success(request, 'Book added to favorites!')
    return redirect('home')  # Redirect to the book detail page

def remove_favorite(request, id):
    book = get_object_or_404(Book, id=id)
    book.favorites.remove(request.user)
    messages.success(request, 'Book removed from favorites!')
    return redirect('home' )
    
# @login_required
# def favorite_books(request):
#     # Get the books that the user has added to their favorites
#     favorite_books = Book.objects.filter(favorites=request.user)
    
#     context = {
#         'favorite_books': favorite_books,
#     }
    
#     return render(request, 'book/favorite_books.html', context)


    
    

    
    

