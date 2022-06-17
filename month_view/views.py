from datetime import datetime, date
import calendar

from django.urls import reverse
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.utils.decorators import method_decorator

from .forms import NewEventForm, EditEventForm
from .models import Event


'''@login_required(login_url='/')
def month_view_page(request, month, year):
    new_form = NewEventForm()
    edit_form = EditEventForm()
    if request.method == 'POST':
        if 'logout' in request.POST:
            logout(request)
            return redirect(reverse('login_page'))
        elif 'right_month' in request.POST:
            month = month + 1
            month, year = _validate_month_year(month, year)
            return redirect(reverse('month_page', kwargs={'month': month, 'year': year}))
        elif 'left_month' in request.POST:
            month = month - 1
            month, year = _validate_month_year(month, year)
            return redirect(reverse('month_page', kwargs={'month': month, 'year': year}))
        elif 'edit_event' in request.POST:
            event_to_edit = Event.objects.get(id=request.POST['event_id'])
            edit_form = EditEventForm(request.POST, instance=event_to_edit)
            if edit_form.is_valid():
                edit_form.save()
        elif 'delete_event' in request.POST:
            event_to_delete = Event.objects.get(id=request.POST['event_id'])
            event_to_delete.delete()
        else:
            new_form = NewEventForm(request.POST)
            if new_form.is_valid():
                new_form.save()
    month_day_info = []

    
    last_day_of_month = date(year, month, _get_days_in_month(month, year)).weekday()
    if last_day_of_month == 6:
        last_day_of_month = 0
    else:
        last_day_of_month += 1
        _get_before_filler_days(_get_day_of_week_month_starts_on(month, year), month, year) +  + _get_after_filler_days(last_day_of_month, month, year)
        
    dates = _get_dates_in_month(month, year)
    for i in range(1, _get_days_in_month(month, year) + 1):
        month_day_info.append((i, dates[i-1], _get_events_on_day(i, month, year)))

    context = {
        'new_form': new_form,
        'edit_form': edit_form,
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

def _validate_month_year(month, year):
    if month == 0:
        return 12, year - 1
    elif month == 13:
        return 1, year + 1
    return month, year

def _get_day_of_week_month_starts_on(month, year):
    day = calendar.monthrange(year, month)[0]
    if day == 6:
        return 0
    return day + 1

def _get_before_filler_days(day_of_week, month, year):
    month, year = _validate_month_year(month-1, year)
    past_month_len = _get_days_in_month(month, year) + 1
    return [i for i in range(past_month_len - day_of_week, past_month_len)]

def _get_after_filler_days(day_of_week, month, year):
    month, year = _validate_month_year(month+1, year)
    return [i + 1 for i in range(6 - day_of_week)]'''


class MonthViewPage(View):

    new_event_form = NewEventForm()
    edit_event_form = EditEventForm()
    user = None
    month = None
    year = None

    @method_decorator(login_required)
    def get(self, request, month, year):
        self.month, self.year = month, year
        month_days = self._get_days_in_month()
        context = {
            'new_form': self.new_event_form,
            'edit_form': self.edit_event_form,
            'month_number': month,
            'month_name': self._get_month_name(),
            'year_number': year,
            'month_events': [(day, list(self._get_events_on_day(day))) for day in month_days]
        }
        return render(request, 'month_view/month_view.html', context)

    @method_decorator(login_required)
    def post(self, request, month, year):
        self.month, self.year = month, year
        if 'logout' in request.POST:
            return self.logout_post(request)
        elif 'right_month' in request.POST:
            return self.right_month_post()
        elif 'left_month' in request.POST:
            return self.left_month_post()
        elif 'edit_event' in request.POST:
            self.edit_event_post(request)
        elif 'delete_event' in request.POST:
            self.delete_event_post(request)
        else:
            self.new_event_form = NewEventForm(request.POST)
            if self.new_event_form.is_valid():
                self.new_event_form.save()
        month_days = self._get_days_in_month()
        context = {
            'new_form': self.new_event_form,
            'edit_form': self.edit_event_form,
            'month_number': month,
            'month_name': self._get_month_name(),
            'year_number': year,
            'new_form': self.new_event_form,
            'month_events': [(day, list(self._get_events_on_day(day))) for day in month_days]
        }
        return render(request, 'month_view/month_view.html', context=context)

    def logout_post(self, request):
        logout(request)
        return redirect(reverse('login_page'))

    def right_month_post(self):
        self.month += 1
        month, year = self._validate_month_year()
        return redirect(reverse('month_page', kwargs={'month': month, 'year': year}))

    def left_month_post(self):
        self.month -= 1
        month, year = self._validate_month_year()
        return redirect(reverse('month_page', kwargs={'month': month, 'year': year}))

    def edit_event_post(self, request):
        event_to_edit = Event.objects.get(id=request.POST['event_id'])
        edit_form = EditEventForm(request.POST, instance=event_to_edit)
        if edit_form.is_valid():
            edit_form.save()

    def delete_event_post(self, request):
        event_to_delete = Event.objects.get(id=request.POST['event_id'])
        event_to_delete.delete()

    def _validate_month_year(self):
        if self.month == 0:
            return 12, self.year - 1
        elif self.month == 13:
            return 1, self.year + 1
        return self.month, self.year

    def _find_month_length(self):
        return calendar.monthrange(self.year, self.month)[1]
    
    def _get_days_in_month(self):
        length = calendar.monthrange(self.year, self.month)[1]
        return [i + 1 for i in range(length)]
    
    def _get_events_on_day(self, day, month=None, year=None):
        if month == None or year == None:
            month = self.month
            year = self.year
        return Event.objects.filter(date=f'{year}-{month}-{day}')

    def _get_month_name(self):
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
        return months[self.month]

    def _set_month_year(self, month, year):
        self.month = month
        self.year = year