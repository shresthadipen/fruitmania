from django.contrib.auth.decorators import login_required
from .models import Fruits, Cart, CartItem
from django.http import JsonResponse
from django.shortcuts import render, redirect, HttpResponseRedirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login , logout as auth_logout, update_session_auth_hash
from .models import *


def signup(request):
    if request.method == 'POST':
        username = request.POST.get('signup_username')
        email = request.POST.get('signup_email')
        password = request.POST.get('signup_password')

        myuser = User.objects.create_user(username, email, password)
        myuser.save()

        return render(request, "auth.html")

    return render(request, 'auth.html')



def login_view(request):
    if request.method == "POST":
        username = request.POST.get('login_username')
        password = request.POST.get('login_password')
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)

            next_url = request.GET.get('next', '/')
            return redirect(next_url)
        else:
            return render(request, 'auth.html', {'error': 'Invalid Username or Password'})
    return render(request, 'auth.html')

def home(request):
    fruits = Fruits.objects.all().order_by("-id")
    return render(request, 'index.html', {"fruits": fruits})


def logout(request):
    auth_logout(request)
    return redirect("home")


def add_to_cart(request, fruit_id):
    fruit = Fruits.objects.get(id=fruit_id)
    user = request.user

    cart, _ = Cart.objects.get_or_create(user=user, is_paid=False)
    
    cart_item = CartItem.objects.filter(cart=cart, product=fruit).first()

    if cart_item:
        cart_item.quantity += 1
        cart_item.save()
    else:
        cart_item = CartItem.objects.create(cart=cart, product=fruit, quantity=1)
    
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def cart(request):
    cart = Cart.objects.filter(is_paid=False, user=request.user).first()

    if cart:
        cart_items = CartItem.objects.filter(cart=cart)
    else:
        cart_items = []

    total_amount = sum(item.total_price for item in cart_items)
    shipping = 50 
    amount = total_amount + shipping

    context = {
        'cart_items': cart_items,
        'amount': total_amount,
        'shipping': shipping,
        'total_amount': amount,
    }

    return render(request, 'cart.html', context)

def add_quantity(request, fruit_id):
    # Get the cart and product
    fruit = get_object_or_404(Fruits, id=fruit_id)
    user = request.user
    cart = get_object_or_404(Cart, user=user, is_paid=False)
    
    # Get the cart item
    cart_item = CartItem.objects.filter(cart=cart, product=fruit).first()

    if cart_item:
        # Increase quantity by 1
        cart_item.quantity += 1
        cart_item.save()
    
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def minus_quantity(request, fruit_id):
    fruit = get_object_or_404(Fruits, id=fruit_id)
    user = request.user
    cart = get_object_or_404(Cart, user=user, is_paid=False)
    
    # Get the cart item
    cart_item = CartItem.objects.filter(cart=cart, product=fruit).first()

    if cart_item:
        # Decrease quantity by 1 if greater than 1
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            # If quantity is 1, you can remove the cart item (optional)
            cart_item.delete()
    
    return HttpResponseRedirect(request.META.get('HTTP_REFERER')) 


def remove_from_cart(request, fruit_id):
    # Get the product and user
    fruit = get_object_or_404(Fruits, id=fruit_id)
    user = request.user
    cart = get_object_or_404(Cart, user=user, is_paid=False)
    
    # Get the cart item and delete it
    cart_item = CartItem.objects.filter(cart=cart, product=fruit).first()
    
    if cart_item:
        cart_item.delete()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def profile(request):
    return render(request, 'profile.html')

def order(request):
    return render(request, 'order.html')

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

def available(request):
    fruits = Fruits.objects.all()
    return render(request, 'available.html',{"fruits" : fruits})