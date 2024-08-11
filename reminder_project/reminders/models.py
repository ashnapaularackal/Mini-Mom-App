# reminders/models.py
from django.db import models

class Destination(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)  # Allow blank and null

    def __str__(self):
        return self.name

class Reminder(models.Model):
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE)
    item = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.item} for {self.destination.name}'
