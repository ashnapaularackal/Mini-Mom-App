from django.conf import settings
import google.generativeai as genai
import json  # Import the json module

genai.configure(api_key=settings.GEMINI_API_KEY)

def get_gemini_response(prompt):
    try:
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(prompt)
        print("Raw response:", response.text)  # Log the raw response
        return response.text
    except Exception as e:
        print(f"Error fetching Gemini API response: {e}")
        return "I'm sorry, I couldn't generate a response at the moment."

def get_personalized_reminders(destination, location=''):
    prompt = f"""
    Provide 5 personalized reminders for someone going to {destination} in {location if location else 'the area'}.
    Include essential items, clothing, documents, time management, and safety tips.
    Format the response as a JSON array of strings.
    """
    response = get_gemini_response(prompt)

    try:
        reminders = json.loads(response)
        if isinstance(reminders, list) and len(reminders) == 5:
            return reminders
    except json.JSONDecodeError:
        pass

    # Fallback reminders
    fallback_reminders = {
        "school": [
            "Pack your backpack with all necessary books and notebooks",
            "Don't forget your lunch or lunch money",
            "Bring any completed homework assignments",
            "Remember your PE kit if you have gym class today",
            "Double-check you have your school ID card"
        ],
        "party": [
            "Bring a gift if it's a birthday party",
            "Don't forget to style your hair and apply makeup if desired",
            "Charge your phone for pictures and emergencies",
            "Bring a jacket in case it gets cold later",
            "Remember to arrange a safe ride home"
        ],
        "gym": [
            "Pack your workout clothes and shoes",
            "Bring a water bottle to stay hydrated",
            "Don't forget your gym membership card",
            "Pack a small towel and toiletries for after your workout",
            "Bring a healthy snack for post-workout energy"
        ]
    }

    return fallback_reminders.get(destination.lower(), [
        f"Remember to bring essentials for {destination}",
        "Check if you need any specific items or documents",
        "Dress appropriately for the occasion",
        "Plan your schedule to arrive on time",
        "Stay safe and have a great time!"
    ])

def get_weather_info(location):
    prompt = f"""
    Provide a brief, friendly weather report for {location}, as if you're a parent telling their child. 
    Include whether they should bring an umbrella, wear a coat, or take any other weather-related precautions.
    Keep it concise and easy to understand.
    """
    return get_gemini_response(prompt)

def get_traffic_info(location):
    prompt = f"""
    Provide a brief, friendly traffic update for {location}, as if you're a parent advising their child. 
    Mention if they should leave earlier or if the usual route is clear.
    Keep it concise and easy to understand.
    """
    return get_gemini_response(prompt)
