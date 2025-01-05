from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate

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

        user = authenticate(username = username, password = password )

        if user is not None:
            login(request, user)
            return render (request, 'index.html')

        else:
            return HttpResponse("Invalid Username or Password")
        
    return render(request, 'auth.html')

def home(request):
    return render(request, 'index.html')
