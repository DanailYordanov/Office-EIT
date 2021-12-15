from django.contrib import admin
from main.models import Car, CarType, Reminder, ReminderType, Service, ServiceType, Contractor, Bank, Address, Course, CourseAddress


admin.site.register(Car)
admin.site.register(CarType)
admin.site.register(Bank)
admin.site.register(Service)
admin.site.register(ServiceType)
admin.site.register(Reminder)
admin.site.register(Contractor)
admin.site.register(ReminderType)
admin.site.register(Course)
admin.site.register(Address)
admin.site.register(CourseAddress)
