from django.urls import path, include
from . import views


urlpatterns = [
    path('', include('allauth.urls')),
    path('profile/details/',
         views.ProfileDetailsView.as_view(), name='profile-details')
]
