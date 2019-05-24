from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.validators import validate_email
from django.urls import reverse

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Button


User = get_user_model()


class CustomAuthenticationForm(AuthenticationForm):
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





class CustomUserCreationForm(forms.ModelForm):
    username = forms.CharField(label='Username', widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter your username'}))
    email = forms.CharField(label='Email', widget=forms.EmailInput(attrs={'class':'form-control', 'placeholder':'Enter an email'}))
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Enter password'}))
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Repeat your password again'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('username', css_class='form-group col-md-6 mb-0'),
                Column('email', css_class='form-group col-md-6 mb-0'),
            ),
            Row(
                Column('password1', css_class='form-group col-md-6 mb-0 mt-4'),
                Column('password2', css_class='form-group col-md-6 mb-0 mt-4'),
            ),
            Row(
                Column(Submit('submit', 'Sign UP', css_class='btn btn-primary px-4'), css_class='form-group col-md-1 mb-0 mt-3'),
                Column(Button('cancel', 'Cancel', css_class='btn btn-danger px-4',
                              onclick="window.location.href = '{}';".format(reverse('core:base_view'))
                              ), css_class='form-group col-md-1 mb-0 mt-3 ml-5'),

            ),
        )


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

