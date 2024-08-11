# reminders/admin.py
from django.contrib import admin
from .models import Destination, Reminder

admin.site.register(Destination)
admin.site.register(Reminder)
