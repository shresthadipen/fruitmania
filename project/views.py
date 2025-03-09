from django.contrib.auth.decorators import login_required
from .models import Fruits, Cart, CartItem
from django.http import JsonResponse
from django.shortcuts import render, redirect, HttpResponseRedirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login , logout as auth_logout, update_session_auth_hash
from .models import *
from django.db.models import Sum

def get_total_cart_items(user):
    user_cart = Cart.objects.filter(user=user).first()
    total_cart_items = 0
    if user_cart:
        total_cart_items = CartItem.objects.filter(cart=user_cart).aggregate(total_items=Sum('quantity'))['total_items'] or 0
    return total_cart_items

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

            if user.is_superuser:
                return redirect('dashboard')
            else:
                return redirect('home')

        else:
            return render(request, 'auth.html', {'error': 'Invalid Username or Password'})

    return render(request, 'auth.html')

def home(request):
    fruits = Fruits.objects.all().order_by("-id")
    return render(request, 'index.html', {"fruits": fruits})

def logout(request):
    auth_logout(request)
    return redirect("home")

@login_required
def add_to_cart(request, fruit_id):
    try:
        fruit = Fruits.objects.get(id=fruit_id)
    except Fruits.DoesNotExist:
        return redirect('login')

    if fruit.stock is None or fruit.stock == 0:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    user = request.user
    cart, _ = Cart.objects.get_or_create(user=user, is_paid=False)
    cart_item = CartItem.objects.filter(cart=cart, product=fruit).first()

    if cart_item:
        if cart_item.quantity < fruit.stock:
            cart_item.quantity += 1
            cart_item.save()
    else:
        cart_item = CartItem.objects.create(cart=cart, product=fruit, quantity=1)

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def cart(request):
    if request.user.is_authenticated:
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

    else:
        return render(request, 'cart.html')

def add_quantity(request, fruit_id):
    fruit = get_object_or_404(Fruits, id=fruit_id)

    if fruit.stock is None or fruit.stock == 0:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    user = request.user
    cart = get_object_or_404(Cart, user=user, is_paid=False)

    cart_item = CartItem.objects.filter(cart=cart, product=fruit).first()

    if cart_item:
        if cart_item.quantity < fruit.stock:
            cart_item.quantity += 1
            cart_item.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def minus_quantity(request, fruit_id):
    fruit = get_object_or_404(Fruits, id=fruit_id)

    if fruit.stock is None or fruit.stock == 0:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    user = request.user
    cart = get_object_or_404(Cart, user=user, is_paid=False)

    cart_item = CartItem.objects.filter(cart=cart, product=fruit).first()

    if cart_item:
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def remove_from_cart(request, fruit_id):
    fruit = get_object_or_404(Fruits, id=fruit_id)
    user = request.user
    cart = get_object_or_404(Cart, user=user, is_paid=False)

    cart_item = CartItem.objects.filter(cart=cart, product=fruit).first()

    if cart_item:
        cart_item.delete()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required
def order_history(request):
    # Fetch all orders for the logged-in user
    orders = Order.objects.filter(user=request.user).order_by('-created_at')  # Order by most recent
    return render(request, 'order.html', {'orders': orders})

def about(request):
    return render(request, 'about.html')



def available(request):
    fruits = Fruits.objects.all()
    return render(request, 'available.html',{"fruits" : fruits})


@login_required
def dashboard(request):
    product = Fruits.objects.all()[:5]
    order = Order.objects.all()[:7]
    totaluser = User.objects.count()
    total_sales = Order.objects.aggregate(total_sales=Sum('total_price'))['total_sales'] or 0
    totalProducts = Fruits.objects.count()
    return render(request, "dash_home.html", {"products":product,  "orders":order, "totalUsers":totaluser, 'totalSales': total_sales, "totalProduct":totalProducts})

def order_dash(request):
    order = Order.objects.all()
    return render(request, "order_dash.html", {"orders":order})

def product(request):
    product = Fruits.objects.all()
    return render(request, "product.html", {"products":product})

def user(request):
    user = User.objects.all()
    return render(request, "user.html", {"users" : user})


def edit_product(request, product_id):
    product = get_object_or_404(Fruits, id=product_id)

    if request.method == 'POST':
        product.name = request.POST.get('name')
        product.price = request.POST.get('price')
        product.stock = request.POST.get('stock')
        product.description = request.POST.get('description')

        if 'image' in request.FILES:
            product.image = request.FILES['image']

        product.save()

        return redirect('product')

    return render(request, 'edit_product.html', {'product': product})

def edit_user(request, user_id):
    user = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        user.username = request.POST.get('username')
        user.email = request.POST.get('email')
        user.save()
        return redirect('user')

    return render(request, 'edit_user.html', {'user': user})

def profile(request, user_id):
    user = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        user.username = request.POST.get('username')
        user.email = request.POST.get('email')
        user.save()
        return redirect('user')

    return render(request, 'profile.html', {'user': user})

def add_product(request):
    if request.method == 'POST':
        # Get data from the form
        name = request.POST.get('name')
        price = request.POST.get('price')
        stock = request.POST.get('stock')
        description = request.POST.get('description')
        image = request.FILES.get('image')

        # Save the new product
        product = Fruits(
            name=name,
            price=price,
            stock=stock,
            description=description,
            image=image
        )
        product.save()

        # Redirect to the product list page
        return redirect('product_list')

    # Render the add product form
    return render(request, 'add_product.html')

@login_required
def place_order(request):
    if request.method == 'POST':
        cart = get_object_or_404(Cart, user=request.user, is_paid=False)

        shipping_address = request.POST.get('shipping_address')
        if not shipping_address:
            return render(request, 'cart.html', {'error': 'Please provide a shipping address.'})

        payment_method = 'Cash on Delivery'

        total_price = sum(item.total_price for item in cart.items.all())

        order = Order.objects.create(
            user=request.user,
            cart=cart,
            shipping_address=shipping_address,  
            payment_method=payment_method,
            total_price=total_price
        )

        cart.is_paid = True
        cart.save()

        return redirect('order_confirmation', order_id=order.id)

    return redirect('cart')

@login_required
def order_confirmation(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'order_confirmation.html', {'order': order})