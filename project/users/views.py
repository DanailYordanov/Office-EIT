from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect, get_object_or_404
from .forms import ProfileDetailsForm, UserDocumentFormset


def profile_details(request, pk=None):
    if pk:
        if request.user.is_staff:
            user = get_object_or_404(get_user_model(), pk=pk)
            redirect_url = reverse('main:users-details-list')
            message = f'Редактиране на информацията на {user}'
        else:
            raise PermissionDenied
    else:
        user = request.user
        redirect_url = reverse('profile-details')
        message = f'Редактиране на вашата информация'

    if request.method == 'POST':
        form = ProfileDetailsForm(request.user, request.POST, instance=user)
        formset = UserDocumentFormset(
            request.POST, request.FILES, instance=user)

        if form.is_valid() and formset.is_valid():
            form.save()

            for f in formset:
                if f.is_valid():
                    f.instance.user = user
                    f.save()

            formset.save()
            return redirect(redirect_url)
    else:
        form = ProfileDetailsForm(user=request.user, instance=user)
        formset = UserDocumentFormset(instance=user)

    context = {
        'form': form,
        'formset': formset,
        'message': message,
        'redirect_url': redirect_url,
        'page_heading': 'Информация за шофьор'
    }

    return render(request, 'account/profile_details.html', context)
