# reminders/suggestions.py
def get_suggestions(destination):
    suggestions = {
        'Exam': ['Calculator', 'Admit Card'],
        'Shopping': ['Coupons', 'Membership Card']
    }
    return suggestions.get(destination.name, [])
