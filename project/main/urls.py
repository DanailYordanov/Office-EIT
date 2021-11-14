from django.urls import path
from . import views

app_name = 'main'
urlpatterns = [
    path('', views.cars_list, name='cars-list'),
    path('add-car/', views.add_car, name='add-car'),
    path('update-car/<int:pk>/', views.update_car, name='update-car'),
    path('delete-car/<int:pk>/', views.CarDeleteView.as_view(), name='delete-car')
]
