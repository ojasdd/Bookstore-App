from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Book
from .forms import LoginForm

def login_view(request):
    form = LoginForm(data=request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.get_user()
        login(request, user)
        return redirect('book_list')
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def book_list(request):
    books = Book.objects.all()
    request.session['last_page'] = 'book_list'
    return render(request, 'book_list.html', {'books': books})

@login_required
def add_to_cart(request, book_id):
    cart = request.session.get('cart', [])
    if book_id not in cart:
        cart.append(book_id)
    request.session['cart'] = cart
    return redirect('book_list')

@login_required
def view_cart(request):
    cart = request.session.get('cart', [])
    books = Book.objects.filter(id__in=cart)
    return render(request, 'cart.html', {'books': books})

@login_required
def back_to_books(request):
    return redirect('book_list')
