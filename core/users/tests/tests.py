from django.contrib import auth
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.test import TestCase, Client
from django.urls import reverse
import datetime

from core.users.tests.factories import UserFactory


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