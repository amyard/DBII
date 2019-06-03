import factory
from factory import fuzzy
from faker import Faker

from core.common.factories import BaseModelFactory
from core.posts.models import Post, Like, Comment
from core.users.tests.factories import UserFactory


fake = Faker()


class PostFactory(BaseModelFactory):
    author = factory.SubFactory(UserFactory)
    title = factory.Sequence(lambda n: 'new title for post {}'.format(n))
    slug = factory.Sequence(lambda n: 'new-title-for-post-{}'.format(n))
    content = fake.text()

    class Meta:
        model = Post


class LikeFactory(BaseModelFactory):
    post = factory.SubFactory(PostFactory)
    user = factory.SubFactory(UserFactory)

    class Meta:
        model = Like


class CommentFactory(BaseModelFactory):
    post = factory.SubFactory(PostFactory)
    user = factory.SubFactory(UserFactory)
    text = fake.text()

    class Meta:
        model = Comment