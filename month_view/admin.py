from ast import Pass
from django.contrib import admin
from .models import Event

@admin.register(Event)
class ModelEvent(admin.ModelAdmin):
    pass
