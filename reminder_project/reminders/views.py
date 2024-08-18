from django.shortcuts import render, redirect
from .gemini_api import get_personalized_reminders, get_weather_info, get_traffic_info
from django.http import HttpResponse, Http404
from gtts import gTTS
import os
from django.conf import settings
from .models import Destination
from .utils import get_encoded_ai_mom_image

def home(request):
    prompt_file = generate_voice_prompt("Where are you going today?", "home_prompt.mp3")
    context = {
        'prompt_file': prompt_file,
        'ai_mom_image': get_encoded_ai_mom_image()
    }
    return render(request, 'home.html', context)

def get_reminders_view(request):
    if request.method == 'POST':
        destination = request.POST.get('destination', '').lower()
        location = request.POST.get('location', '')
        current_location = request.POST.get('current_location', '')

        # Use current location for common destinations
        if destination in ['school', 'office', 'gym', 'college'] and current_location:
            reminders = get_personalized_reminders(destination, current_location)
            weather_info = get_weather_info(current_location)
            traffic_info = get_traffic_info(current_location)
        else:
            if not location:
                return ask_location(request, destination)
            reminders = get_personalized_reminders(destination, location)
            weather_info = get_weather_info(location)
            traffic_info = get_traffic_info(location)

        destination_obj, created = Destination.objects.get_or_create(
            name=destination,
            defaults={'description': ''}
        )

        # Generate voice response
        voice_text = f"Reminders for {destination}: {', '.join(reminders)}. Weather: {weather_info}. Traffic: {traffic_info}."
        voice_file = generate_voice_response(voice_text)

        context = {
            'destination': destination,
            'location': location or 'Current Location',
            'reminders': reminders,
            'weather_info': weather_info,
            'traffic_info': traffic_info,
            'voice_file': os.path.basename(voice_file),
            'ai_mom_image': get_encoded_ai_mom_image()
        }
        return render(request, 'reminders.html', context)

    return redirect('home')

def serve_audio(request, filename):
    file_path = os.path.join(settings.MEDIA_ROOT, filename)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="audio/mpeg")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
    raise Http404

def generate_voice_response(text):
    tts = gTTS(text=text, lang='en')
    filename = os.path.join(settings.MEDIA_ROOT, 'voice_response.mp3')
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    tts.save(filename)
    return filename

def generate_voice_prompt(text, filename):
    tts = gTTS(text=text, lang='en')
    filepath = os.path.join(settings.MEDIA_ROOT, filename)
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    tts.save(filepath)
    return filename

def ask_location(request, destination):
    prompt_file = generate_voice_prompt(f"Where is your {destination}?", f"location_prompt_{destination}.mp3")
    context = {
        'destination': destination,
        'prompt_file': prompt_file,
        'ai_mom_image': get_encoded_ai_mom_image()
    }
    return render(request, 'ask_location.html', context)