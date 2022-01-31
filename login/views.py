from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login

def login_page(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('month_view/')
        else:
            return redirect('/')
    return render(request, 'login/login.html')
