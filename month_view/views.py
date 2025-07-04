from datetime import datetime, date
import calendar
from django.http import JsonResponse

from django.urls import reverse
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.utils.decorators import method_decorator

from .forms import NewEventForm, EditEventForm
from .models import Event
from month_view.serializers import EventSerializer


class MonthViewPage(View):

    new_event_form = NewEventForm()
    edit_event_form = EditEventForm()
    user = None
    month = None
    year = None

    @method_decorator(login_required)
    def get(self, request, month, year):
        self.month, self.year = month, year
        before_days = self._get_before_filler_days(self._get_day_of_week_month_starts_on())
        month_days = self._get_days_in_month()
        after_days = self._get_after_filler_days()
        context = {
            'new_form': self.new_event_form,
            'edit_form': self.edit_event_form,
            'month_number': month,
            'month_name': self._get_month_name(),
            'year_number': year,
            'last_month_events': [(day, list(self._get_events_on_day(day, self.last_month, self.last_year))) for day in before_days],
            'month_events': [(day, list(self._get_events_on_day(day))) for day in month_days],
            'next_month_events': [(day, list(self._get_events_on_day(day, self.next_month, self.next_year))) for day in after_days]
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
        before_days = self._get_before_filler_days(self._get_day_of_week_month_starts_on())
        month_days = self._get_days_in_month()
        after_days = self._get_after_filler_days()
        context = {
            'new_form': self.new_event_form,
            'edit_form': self.edit_event_form,
            'month_number': month,
            'month_name': self._get_month_name(),
            'year_number': year,
            'last_month_events': [(day, list(self._get_events_on_day(day, self.last_month, self.last_year))) for day in before_days],
            'month_events': [(day, list(self._get_events_on_day(day))) for day in month_days],
            'next_month_events': [(day, list(self._get_events_on_day(day, self.next_month, self.next_year))) for day in after_days]
        }
        return render(request, 'month_view/month_view.html', context=context)

    def logout_post(self, request):
        logout(request)
        return redirect(reverse('login_page'))

    def right_month_post(self):
        self.month += 1
        self._validate_month_year()
        return redirect(reverse('month_page', kwargs={'month': self.month, 'year': self.year}))

    def left_month_post(self):
        self.month -= 1
        self._validate_month_year()
        return redirect(reverse('month_page', kwargs={'month': self.month, 'year': self.year}))

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
            self.month, self.year = 12, self.year - 1
        elif self.month == 13:
            self.month, self.year = 1, self.year + 1

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

    def _get_day_of_week_month_starts_on(self):
        day = calendar.monthrange(self.year, self.month)[0]
        if day == 6:
            return 0
        return day + 1

    def _get_before_filler_days(self, day_of_week):
        self.month -= 1
        self._validate_month_year()
        self.last_month, self.last_year = self.month, self.year
        past_month_len = self._find_month_length() + 1
        self.month += 1
        self._validate_month_year()
        return [i for i in range(past_month_len - day_of_week, past_month_len)]

    def _get_after_filler_days(self):
        self.month += 1
        self._validate_month_year()
        self.next_month, self.next_year = self.month, self.year
        next_month_start = self._get_day_of_week_month_starts_on()
        self.month -= 1
        self._validate_month_year()
        days = [i for i in range(1, 8 - next_month_start)]
        if len(days) == 7:
            return []
        return days

    def _set_month_year(self, month, year):
        self.month = month
        self.year = year


def month_view_api_page(request, month, year):
    month_event_data = {}
    month_event_data['month_info'] = {
        'name' : _get_month_name(month),
        'month_num' : month,
        'year' : year,
    }
    month_event_data['events'] = _get_month_events(month, year)
    return JsonResponse(month_event_data)

def _get_month_events(month, year):
    events = {}
    month_events = Event.objects.filter(date__month=month, date__year=year)
    length = _find_month_length(month, year) + 1
    for day in range(1, length):
        day_events = month_events.filter(date__day=day)
        s = EventSerializer(day_events, many=True)
        events[day] = s.data
    return events

def _get_month_name(month):
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

def _find_month_length(month, year):
        return calendar.monthrange(year, month)[1]