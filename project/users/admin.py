from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from .forms import CustomUserCreationForm, CustomUserChangeForm


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm
    list_display = ('username', 'first_name',
                    'middle_name', 'last_name', 'is_staff')
    search_fields = ('username', 'first_name', 'middle_name', 'last_name')
    ordering = ('first_name',)

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Лична информация', {
         'fields': (
             'first_name',
             'middle_name',
             'last_name',
             'email',
             'personal_id',
             'phone_number',
             'bank',
             'debit_card_number'
         )}),
        (
            'Права',
            {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser',
                    'groups',
                    'user_permissions',
                ),
            },
        ),
        ('Дати', {'fields': (
            'last_login',
            'date_joined',
            'id_card_expiration',
            'drivers_license_expiration',
            'professional_competence',
            'adr_expiration',
            'digital_card_expiration',
            'psychological_test_expiration',
            'pasport_expiration'
        )}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'middle_name', 'last_name', 'password1', 'password2'),
        }),
    )


admin.site.register(CustomUser, CustomUserAdmin)
