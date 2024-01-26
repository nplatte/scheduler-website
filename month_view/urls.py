from django.urls import path
from .views import MonthViewPage, month_view_api_page

urlpatterns = [
    path('<int:month>-<int:year>/', MonthViewPage.as_view(), name='month_page'),
    path('<int:month>-<int:year>/api', month_view_api_page, name='api_month_page')
]