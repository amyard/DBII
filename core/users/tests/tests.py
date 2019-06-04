from django.contrib import auth
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.test import TestCase, Client
from django.urls import reverse
import datetime

from core.users.tests.factories import UserFactory
from core.users.forms import CustomAuthenticationForm, CustomUserCreationForm


User = get_user_model()


class CreateUpdateDeleteUserTestCase(TestCase):

    def setUp(self):
        self.user = User.objects._create_user(email='test@test.com', password='12121212')
        self.user.set_password('12121212')
        self.user.save()

    def test_create_user_invalid_active(self):
        self.assertFalse(self.user.is_active)

    def test_create_user_valid_active(self):
        self.user.is_active = True
        self.user.save()
        self.assertTrue(self.user.is_active)


    def test_update_user_valid(self):
        self.assertEqual(self.user.city, '')
        self.assertEqual(self.user.country, '')
        self.assertEqual(self.user.birthday, None)
        response = self.client.post(reverse('users:user_update', kwargs={'pk':self.user.id}),
                                    data={'city':'Valencia', 'country':'Spain', 'birthday':'12/12/1987', 'username':'bla'})
        self.assertEqual(response.status_code, 302)
        self.user.refresh_from_db()
        self.assertEqual(self.user.city, 'Valencia')
        self.assertEqual(self.user.country, 'Spain')
        self.assertEqual(self.user.birthday, datetime.date(1987, 12, 12))

    def test_delete_user(self):
        response=self.client.post(reverse('users:user_delete', kwargs={'pk':self.user.id}))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(User.objects.all())


class UsersTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.client = Client()
        cls.user = UserFactory()
        cls.url = reverse('users:signin')
        cls.logout = reverse('users:logout')

    def test_current_user_is_anonymous(self):
        response = self.client.get(self.url)
        curr_user = response.context["user"]
        self.assertEqual(curr_user, AnonymousUser())

    def test_login_url_accessible_by_name(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_redirect_if_not_logged_in(self):
        resp = self.client.get(reverse('posts:base_view'))
        self.assertRedirects(resp, '/users/signin/?next=/')

    def test_logout_user(self):
        self.client.force_login(self.user)
        response = self.client.get(self.logout)
        self.assertEqual(response.status_code, 302)

    def test_login_user(self):
        self.client.force_login(self.user)
        response = self.client.get('/')
        curr_user = response.wsgi_request.user
        self.assertEqual(curr_user, self.user)




class UserCreationFormTestCase(TestCase):

    def setUp(self):
        self.user = UserFactory(username='testing', email='testing@gmail.com')
        self.form = CustomUserCreationForm

    def test_form_is_valid_full_info(self):
        form = self.form(data = {'username':'test', 'email':'test@test.com', 'password1':'123123123', 'password2':'123123123'})
        self.assertTrue(form.is_valid())

    def test_form_is_invalid_no_username(self):
        form = self.form(data = {'email':'test@test.com', 'password1':'123123123', 'password2':'123123123'})
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 1)
        self.assertEquals(form.errors['username'][0], 'This field is required.')

    def test_form_invalid_username(self):
        form = self.form(data = {'email':'test@test.com', 'password1':'123123123', 'password2':'123123123', 'username':'testing'})
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 1)
        self.assertEquals(form.errors['username'][0], 'User with this name already exist.')

    def test_form_differend_passwords(self):
        form = self.form(data={'email': 'test@test.com', 'password1': '123123123', 'password2': '12121212', 'username': 'test'})
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 1)
        self.assertEquals(form.errors['password2'][0], 'Your passwords don\'t match.')

    def test_form_invalid_email(self):
        form = self.form(data = {'email':'testing@gmail.com', 'password1':'123123123', 'password2':'123123123', 'username':'test'})
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 1)
        self.assertEquals(form.errors['email'][0], 'User with email testing@gmail.com already exists.')

    def test_form_invalid_email_forget_sign(self):
        form = self.form(data = {'email':'testing#test.com', 'password1':'123123123', 'password2':'123123123', 'username':'test'})
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 1)
        self.assertEquals(form.errors['email'][0], 'Missed the @ symbol in the email address.')

    def test_form_invalid_email_forget_dot(self):
        form = self.form(data = {'email':'testing@test,com', 'password1':'123123123', 'password2':'123123123', 'username':'test'})
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 1)
        self.assertEquals(form.errors['email'][0], 'Missed the . symbol in the email address.')




class UserAuthenticationFormTestCase(TestCase):

    def setUp(self):
        self.user = UserFactory(username='testing', email='testing@gmail.com', password=12121212)
        self.form = CustomAuthenticationForm

    def test_form_invalid_password(self):
        form = self.form(data={'username': 'testing@gmail.com', 'password':112223344})
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 1)
        self.assertEquals(form.errors['password'][0], 'Invalid password.')

    def test_form_invalid_password_both_fields(self):
        form = self.form(data={'username': 'testing@testing.com', 'password':112223344})
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 2)
        self.assertEquals(form.errors['username'][0], 'User with such email doesn\'t exists.')
        self.assertEquals(form.errors['password'][0], 'Invalid password for this user.')