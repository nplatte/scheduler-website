from datetime import datetime
import calendar
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
    context = {'month_length': _get_days_in_month()}
    return render(request, 'month_view/month_view.html', context)

def _get_days_in_month(month=datetime.now().month, year=datetime.now().year):
    days = [i + 1 for i in range(calendar.monthrange(year, month)[1])]
    return days
