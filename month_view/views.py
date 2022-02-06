from datetime import datetime
import calendar

from django.urls import reverse
from django.shortcuts import render, redirect

from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

from .forms import NewEventForm
from.models import Event


@login_required(login_url='/')
def month_view_page(request):
    month = datetime.now().month
    year = datetime.now().year
    form = NewEventForm()
    if request.method == 'POST':
        if 'logout' in request.POST:
            logout(request)
            return redirect(reverse('login_page'))
        elif 'right_month' in request.POST:
            month = int(request.POST['month']) + 1
        else:
            form = NewEventForm(request.POST)
            if form.is_valid():
                form.save()
    month_events = {i: _get_events_on_day(i, month, year) for i in range(1, _get_days_in_month(month, year) + 1)}
    #month_day_info = [(i, date, _get_events_on_day(i, month, year)) for i in range(1, _get_days_in_month(month, year) + 1)]
    context = {
        'form': form,
        'month_number': month,
        'month_events': month_events,
        'month_name': _get_month_name(month)
        }
    return render(request, 'month_view/month_view.html', context)

def _get_days_in_month(month=datetime.now().month, year=datetime.now().year):
    days = calendar.monthrange(year, month)[1]
    return days

def _get_events_on_day(day, month, year):
    return Event.objects.filter(date=f'{year}-{month}-{day}')

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
