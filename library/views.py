from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate , login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.urls import reverse
from .models import Book,BorrowRequest
from .forms import BookForm,BorrowRequestForm

# Create your views here.
def register_view(request): #the user can register using this view.
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']  # receives data from the user

        user = User.objects.create_user(username=username, password=password)
        user.save()
        messages.success(request,'Registered Successfilly')
        return redirect('login')
    return render(request,'library/register.html')
def login_view(request):
    if request.method =='POST':
        username = request.POST['username']
        password = request.POST['password'] 

        user = authenticate(request,username=username, password=password)  #authenticates the user

        if user:
            login(request,user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid Credentials')
    return render(request, 'library/login.html')
def logout_view(request):
    logout(request)
    return redirect('login')
@login_required
def home_view(request):
    books = Book.objects.all()
    if request.user.is_superuser:
        requests = BorrowRequest.objects.filter(approved=False)
        return render(request, 'library/home_librarian.html', {'books': books, 'requests': requests})
    user_requests = BorrowRequest.objects.filter(user=request.user, approved=False).values_list('book_id', flat=True)
    return render(request, 'library/home_user.html', {
    'books': books,
    'pending_requests': user_requests
    })



@login_required
def my_books_view(request):
    books = Book.objects.filter(issued_to=request.user)
    return render(request, 'library/my_books.html', {'books': books})

@login_required
def borrow_request_view(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == 'POST':
        form = BorrowRequestForm(request.POST, request.FILES)
        if form.is_valid():
            borrow_request = form.save(commit=False)
            borrow_request.user = request.user
            borrow_request.book = book
            borrow_request.save()
            messages.success(request, 'Borrow request submitted.')
            return redirect('home')
    else:
        form = BorrowRequestForm()
    return render(request, 'library/borrow_request.html', {'form': form, 'book': book})

@login_required
def approve_request(request, request_id):
    if not request.user.is_superuser:
        return HttpResponseForbidden("Not authorized")
    borrow_request = get_object_or_404(BorrowRequest, id=request_id)
    book = borrow_request.book
    if not book.is_issued:
        book.is_issued = True
        book.issued_to = borrow_request.user
        book.save()
        borrow_request.approved = True
        borrow_request.save()
        messages.success(request, 'Book issued successfully.')
    else:
        messages.error(request, 'Book is already issued.')
    return redirect('home')




@login_required
def issue_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if not book.is_issued:
        book.is_issued = True
        book.issued_to = request.user
        book.save()
        messages.success(request, f'Book "{book.title}" issued successfully.')
    else:
        messages.error(request, 'Book is already issued.')
    return HttpResponseRedirect(reverse('home'))


@login_required
def return_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if book.is_issued and book.issued_to == request.user:
        book.is_issued = False
        book.issued_to = None
        book.save()
        messages.success(request, f'Book "{book.title}" returned successfully.')
    else:
        messages.error(request, 'You cannot return this book.')
    return HttpResponseRedirect(reverse('home'))


@login_required
def delete_book(request, book_id):
    if not request.user.is_superuser:
        return HttpResponseForbidden("Not authorized")
    book = get_object_or_404(Book, id=book_id)
    book.delete()
    messages.success(request, 'Book deleted successfully.')
    return redirect('home')


@login_required
def add_book(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden("Not authorized to add books.")

    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Book added successfully.")
            return redirect('home')
    else:
        form = BookForm()

    return render(request, 'library/add_book.html', {'form': form})


@login_required
def admin_dashboard(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden("You are not authorized to view this page.")

    total_books = Book.objects.count()
    issued_books = Book.objects.filter(is_issued=True).count()
    users = User.objects.count()

    context = {
        'total_books': total_books,
        'issued_books': issued_books,
        'users': users,
    }
    return render(request, 'library/dashboard.html', context)
