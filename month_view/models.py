from django.db import models
from datetime import date

class Event(models.Model):

    title = models.CharField(max_length=20, default='')
    description = models.CharField(max_length=100, blank=True, null=True)
    time = models.TimeField(blank=True, null=True)
    date = models.DateField(default=date.today())
