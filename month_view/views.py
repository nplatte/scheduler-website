from datetime import datetime
import calendar
from django.shortcuts import render

from django.contrib.auth.decorators import login_required

from .forms import EventForm
from.models import Event


@login_required(login_url='/')
def month_view_page(request):
    month = datetime.now().month
    year = datetime.now().year
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form=EventForm()
    month_events = {i: _get_events_on_day(i, month, year) for i in range(1, _get_days_in_month(month, year) + 1)}
    context = {
        'form': form,
        'month_events': month_events
        }
    return render(request, 'month_view/month_view.html', context)

def _get_days_in_month(month=datetime.now().month, year=datetime.now().year):
    days = calendar.monthrange(year, month)[1]
    return days

def _get_events_on_day(day, month, year):
    return Event.objects.filter(date=f'{year}-{month}-{day}')
