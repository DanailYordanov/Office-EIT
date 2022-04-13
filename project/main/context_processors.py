from django.utils import timezone
from django.core.cache import cache
from django.contrib.auth import get_user_model
from main.models import Reminder


def notifications_processor(request):
    drivers_notifications = cache.get('drivers_notifications')
    reminders_notifications = cache.get('reminders_notifications')

    if not drivers_notifications:
        drivers_notifications = list()
        drivers = get_user_model().objects.filter(is_active=True, is_staff=False)

        expiration_fields = {
            'Лична карта': 'id_card_expiration',
            'Шофьорска книжка': 'drivers_license_expiration',
            'Професионална компетентност': 'professional_competence',
            'ADR': 'adr_expiration',
            'Дигитална карта': 'digital_card_expiration',
            'Психотест': 'psychological_test_expiration',
            'Паспорт': 'pasport_expiration'
        }

        for driver in drivers:
            for key, value in expiration_fields.items():
                if getattr(driver, value):
                    if getattr(driver, value) <= (timezone.now().date() + timezone.timedelta(days=10)):
                        drivers_notifications.append({
                            'driver': driver,
                            'expiration_field': key,
                            'expiration_date': getattr(driver, value)
                        })

        cache.set('drivers_notifications', drivers_notifications)

    if not reminders_notifications:
        reminders_notifications = Reminder.objects.filter(
            expiration_date__lte=(timezone.now().date() + timezone.timedelta(days=5)))
        cache.set('reminders_notifications', reminders_notifications)

    context = {
        'drivers_notifications': drivers_notifications,
        'reminders_notifications': reminders_notifications,
        'notifications_count': len(drivers_notifications) + len(reminders_notifications)
    }

    return context
