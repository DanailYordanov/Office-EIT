from datetime import timedelta
from django.utils import timezone
from main.models import Reminder

def notifications_processor(request):
    notifications = Reminder.objects.filter(expiration_date__lte=(timezone.now() + timedelta(days=5)))
    context = {
        'notifications': notifications
    }

    return context