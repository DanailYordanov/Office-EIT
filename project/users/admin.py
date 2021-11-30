from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from .forms import CustomUserCreationForm, CustomUserChangeForm


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ( 'email', 'first_name', 'last_name', 'password1', 'password2'),
        }),
    )


admin.site.register(CustomUser, CustomUserAdmin)