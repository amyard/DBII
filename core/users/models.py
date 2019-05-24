from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser


USERNAME_REGEX = '^[a-zA-Z0-9.+-]*$'

class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        if not email:
            raise ValueError('Пользователь должен указать адрес электронной почты')

        user = self.model(username = username, email = self.normalize_email(email))
        user.set_password(password)
        user.is_active = True
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None):
        user = self.create_user(username, email, password=password)
        user.is_admin = True
        user.is_staff = True
        user.save(using=self._db)
        return user



class User(AbstractBaseUser):
    username = models.CharField(max_length=75, unique=True,
                                validators=[RegexValidator(regex=USERNAME_REGEX,
                                                            message='Username must be alphanumeric or contain numbers',
                                                            code='invalid_username')]
                                )
    email = models.EmailField(max_length=255, unique=True)

    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.email

    def get_short_name(self):
        return self.email


    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True