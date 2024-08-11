# reminders/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('reminders/', views.get_reminders_view, name='get_reminders'),
    path('ask_location/<str:destination>/', views.ask_location, name='ask_location'),
    path('audio/<str:filename>', views.serve_audio, name='serve_audio'),
]
