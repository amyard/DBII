from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import PermissionsMixin

import datetime



USERNAME_REGEX = '^[a-zA-Z0-9.+-]*$'

class UserManager(BaseUserManager):

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The Email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(email, password, **extra_fields)



def save_image_path(instance, filename):
    filename = instance.image
    return 'profile_pics/{}/{}'.format(instance.username, filename)



class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=75, unique=True,
                            validators=[RegexValidator(regex=USERNAME_REGEX,
                                                        message='Username must be alphanumeric or contain numbers',
                                                        code='invalid_username')]
                            )
    email = models.EmailField(max_length=255, unique=True)

    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    city = models.CharField(max_length=25, blank=True)
    country = models.CharField(max_length=25, blank=True)
    birthday = models.DateField(default = datetime.date(1970, 1,1), blank=True, null=True)
    image = models.ImageField(default='default-profile.jpg', upload_to=save_image_path, blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')

    def __str__(self):
        return self.email

    def get_short_name(self):
        return self.email


    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True