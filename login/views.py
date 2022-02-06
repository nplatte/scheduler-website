from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login

from datetime import datetime

def login_page(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(f'month_view/{datetime.now().month}/')
        else:
            return redirect('/')
    return render(request, 'login/login.html')
