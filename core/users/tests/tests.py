from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from core.posts.tests.factories import LikeFactory, CommentFactory
from core.users.tests.factories import UserFactory

User = get_user_model()