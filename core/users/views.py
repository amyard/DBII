from django.shortcuts import render
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.views import LogoutView
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.urls import reverse_lazy
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from django.views.generic import CreateView, View, DetailView

from .forms import CustomAuthenticationForm, CustomUserCreationForm
from .tokens import account_activation_token

from bootstrap_modal_forms.generic import BSModalLoginView


User = get_user_model()


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


class SignUpView(View):
    template_name = 'users/signup.html'
    form = CustomUserCreationForm

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, context={'form':self.form})

    def post(self, request, *args, **kwargs):
        form = self.form(request.POST or None)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            password = form.cleaned_data['password1']
            user.set_password(password)
            password_check = form.cleaned_data['password2']
            user.save()
            current_site = get_current_site(request)
            message = render_to_string('users/confirm_email/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                'token': account_activation_token.make_token(user),
            })
            mail_subject = 'Activate your blog account.'
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()
            return render(self.request, 'users/confirm_email/confirm_email.html', {})

        form = self.form(request.POST or None)
        return render(self.request, self.template_name, context = {'form': form})




class ActivateView(View):
    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            return render(request, 'users/confirm_email/confirm_email_valid.html', {})
        else:
            return render(request, 'users/confirm_email/confirm_email_invalid.html', {})



class ProfileDetailView(DetailView):
    model = User
    context_object_name = 'profile'
    template_name = 'users/user-detail.html'