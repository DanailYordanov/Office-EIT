from django.contrib import admin
from main import models


admin.site.register(models.Car)
admin.site.register(models.CarType)
admin.site.register(models.Bank)
admin.site.register(models.Service)
admin.site.register(models.ServiceType)
admin.site.register(models.Contractor)
admin.site.register(models.Reminder)
admin.site.register(models.ReminderType)
admin.site.register(models.Course)
admin.site.register(models.FromTo)
admin.site.register(models.Expense)
admin.site.register(models.ExpenseType)
admin.site.register(models.Address)
admin.site.register(models.CourseAddress)
admin.site.register(models.TripOrder)
admin.site.register(models.CourseInvoice)
admin.site.register(models.TaxTransactionBasis)
admin.site.register(models.CourseMedicalExamination)
admin.site.register(models.CourseTechnicalInspection)