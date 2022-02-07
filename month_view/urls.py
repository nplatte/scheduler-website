from django.urls import path
from .views import month_view_page

urlpatterns = [
    path('<int:month>-<int:year>/', month_view_page, name='month_page'),
]