from datetime import datetime
import calendar

from django.urls import reverse
from django.shortcuts import render, redirect

from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

from .forms import NewEventForm
from.models import Event


@login_required(login_url='/')
def month_view_page(request, month, year):
    form = NewEventForm()
    if request.method == 'POST':
        if 'logout' in request.POST:
            logout(request)
            return redirect(reverse('login_page'))
        elif 'right_month' in request.POST:
            if month == 12:
                month = 1
                year = year + 1
            else:
                month = month + 1
            return redirect(reverse('month_page', kwargs={'month': month, 'year': year}))
        elif 'left_month' in request.POST:
            if month == 1:
                month = 12
                year = year - 1
            else:
                month = month - 1
            return redirect(reverse('month_page', kwargs={'month': month, 'year': year}))
        else:
            form = NewEventForm(request.POST)
            if form.is_valid():
                form.save()
    month_day_info = []
    dates = _get_dates_in_month(month, year)
    for i in range(1, _get_days_in_month(month, year) + 1):
        month_day_info.append((i, dates[i-1], _get_events_on_day(i, month, year)))
    context = {
        'form': form,
        'month_number': month,
        'year_number': year,
        'month_day_tuples': month_day_info,
        'month_name': _get_month_name(month)
        }
    return render(request, 'month_view/month_view.html', context)

def _get_days_in_month(month=datetime.now().month, year=datetime.now().year):
    days = calendar.monthrange(year, month)[1]
    return days

def _get_events_on_day(day, month, year):
    return Event.objects.filter(date=f'{year}-{month}-{day}')

def _get_dates_in_month(month, year):
    return [f'{year}-{month}-{i}' for i in range(1, _get_days_in_month(month, year) + 1)]

def _get_month_name(month=datetime.now().month):
    months = {
        1: 'January',
        2: 'February',
        3: 'March',
        4: 'April',
        5: 'May',
        6: 'June',
        7: 'July',
        8: 'August',
        9: 'September',
        10: 'October',
        11: 'November',
        12: 'December'
    }
    return months[month]
