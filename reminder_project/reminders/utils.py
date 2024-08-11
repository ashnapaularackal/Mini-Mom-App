import base64
import os
from django.conf import settings

def get_encoded_ai_mom_image():
    image_path = os.path.join(settings.BASE_DIR, 'reminders', 'images', 'ai_mom.webp')
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')
