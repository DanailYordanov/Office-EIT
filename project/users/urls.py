from django.urls import path, include
from . import views


urlpatterns = [
    path('', include('allauth.urls')),
    path('profile/details/<int:pk>/',
         views.profile_details, name='profile-details'),
    path('profile/details/',
         views.profile_details, name='profile-details')
]
