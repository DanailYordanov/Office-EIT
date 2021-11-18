from django.contrib import admin
from main.models import Car, Reminder, ReminderType, Service

admin.site.register(Car)
admin.site.register(Service)
admin.site.register(Reminder)
admin.site.register(ReminderType)
