from django.views.generic import UpdateView
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import ProfileDetailsForm


class ProfileDetailsView(LoginRequiredMixin, UpdateView):
    model = get_user_model()
    form_class = ProfileDetailsForm
    template_name = 'account/profile_details.html'

    def get_object(self):
        return self.request.user
