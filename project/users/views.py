from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect, get_object_or_404
from .forms import ProfileDetailsForm


def profile_details(request, pk=None):
    if pk:
        if request.user.is_staff:
            user = get_object_or_404(get_user_model(), pk=pk)
            redirect_url = reverse('profile-details', kwargs={'pk': pk})
            message = f'Редактиране на информацията на {user}'
        else:
            raise PermissionDenied
    else:
        user = request.user
        redirect_url = reverse('profile-details')
        message = f'Редактиране на вашата информация'

    if request.method == 'POST':
        form = ProfileDetailsForm(request.user, request.POST, instance=user)

        if form.is_valid():
            form.save()
            return redirect(redirect_url)
    else:
        form = ProfileDetailsForm(user=request.user, instance=user)

    context = {
        'form': form,
        'message': message,
        'redirect_url': redirect_url
    }

    return render(request, 'account/profile_details.html', context)
