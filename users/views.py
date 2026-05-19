from django.shortcuts import render
from django.contrib.auth import authenticate,login, logout
from django.shortcuts import redirect,render
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