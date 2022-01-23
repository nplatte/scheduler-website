from django.shortcuts import render, redirect


from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

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
    return render(request, 'month_view/login.html')

@login_required(login_url='/')
def month_view_page(request):
    return render(request, 'month_view/month_view.html')

