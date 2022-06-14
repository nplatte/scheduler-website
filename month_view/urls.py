from django.urls import path
from .views import MonthViewPage

urlpatterns = [
    path('<int:month>-<int:year>/', MonthViewPage.as_view(), name='month_page'),
]