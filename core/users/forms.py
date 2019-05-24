from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.validators import validate_email

from bootstrap_modal_forms.mixins import PopRequestMixin, CreateUpdateAjaxMixin


User = get_user_model()


class CustomAuthenticationForm(AuthenticationForm):
    # email = forms.CharField(label='Email', widget=forms.EmailInput())
    password = forms.CharField(label='Password', widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ['password']

    def clean_username(self):
        email = self.cleaned_data['username']
        if '@' not in email:
            raise forms.ValidationError('Missed the @ symbol in the email address.')
        if '.' not in email:
            raise forms.ValidationError('Missed the . symbol in the email address.')
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError('User with such email doesn\'t exists.')
        try:
            mt = validate_email(email)
        except:
            raise forms.ValidationError('Incorrect email.')
        return email


    def clean_password(self):
        email = self.cleaned_data.get('username')
        password = self.cleaned_data['password']
        user = User.objects.filter(email=email)
        if not user:
            raise forms.ValidationError('Invalid password for this user.')
        elif not User.objects.get(email=email).check_password(password):
            raise forms.ValidationError('Invalid password.')
        return password



class CustomUserCreationForm(PopRequestMixin, CreateUpdateAjaxMixin, UserCreationForm):
    username = forms.CharField(label='Username', widget=forms.TextInput())
    email = forms.CharField(label='Email', widget=forms.EmailInput())
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput())
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('User with this name already exist.')
        return username


    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 != password2:
            raise forms.ValidationError('Your passwords don\'t match.')
        return password2


    def clean_email(self):
        email = self.cleaned_data['email']
        if '@' not in email:
            raise forms.ValidationError('Missed the @ symbol in the email address.')
        if '.' not in email:
            raise forms.ValidationError('Missed the . symbol in the email address.')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(f'User with email {email} already exists.')
        try:
            mt = validate_email(email)
        except:
            raise forms.ValidationError('Incorrect email.')
        return email