from django.shortcuts import render
from django.contrib.auth import authenticate,login, logout
from django.contrib.auth.hashers import make_password
from django.shortcuts import redirect,render
from django.contrib.auth.models import User
from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.forms import UserCreationForm

# Create your views here.
def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
    return render(request, 'users/login.html')

def logout_user(request):
    logout(request)
    return redirect("home")

def CreateUserView(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = UserCreationForm()
    return render(
        request,
        "users/register.html",
        {"form": form}
    )

