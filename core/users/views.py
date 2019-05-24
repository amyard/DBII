from django.contrib.auth.views import LogoutView
from django.contrib import messages
from django.urls import reverse_lazy

from .forms import CustomAuthenticationForm

from bootstrap_modal_forms.generic import BSModalLoginView

class CustomLogoutView(LogoutView):
    def get_next_page(self):
        next_page = super(CustomLogoutView, self).get_next_page()
        messages.add_message(self.request, messages.SUCCESS, 'Success: You successfully log out!')
        return next_page


class CustomLoginView(BSModalLoginView):
    authentication_form = CustomAuthenticationForm
    template_name = 'users/signin.html'
    success_message = 'Success: You were successfully logged in.'
    success_url = reverse_lazy('core:base_view')