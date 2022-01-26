from django.urls import path
from .views import month_view_page

url_patterns = [
    path('home/', month_view_page, name='month_page')
]