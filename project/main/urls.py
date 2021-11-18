from django.urls import path
from . import views

app_name = 'main'
urlpatterns = [
    path('', views.cars_list, name='cars-list'),
    path('add-car/', views.add_car, name='add-car'),
    path('update-car/<int:pk>/', views.update_car, name='update-car'),
    path('delete-car/<int:pk>/', views.CarDeleteView.as_view(), name='delete-car'),
    path('reminders/', views.reminders_list, name='reminders-list'),
    path('add-reminder/', views.add_reminder, name='add-reminder'),
    path('update-reminder/<int:pk>/',
         views.update_reminder, name='update-reminder'),
    path('delete-reminder/<int:pk>/',
         views.ReminderDeleteView.as_view(), name='delete-reminder'),
    path('services/', views.services_list, name='services-list'),
    path('add-service/', views.add_service, name='add-service'),
    path('update-service/<int:pk>/', views.update_service, name='update-service'),
    path('delete-service/<int:pk>/',
         views.ServiceDeleteView.as_view(), name='delete-service')
]
