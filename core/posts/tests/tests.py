from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse, resolve
from django.core.paginator import Paginator
from django.utils.encoding import force_text


from core.posts.models import Post, Like, Comment
from core.posts.tests.factories import PostFactory, LikeFactory, CommentFactory
from core.users.tests.factories import UserFactory
from core.posts import views


User = get_user_model()



class PostListView(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.client = Client()
        cls.user = UserFactory(is_active=True)
        cls.url = reverse('posts:base_view')


    def test_login_user(self):
        self.client.force_login(self.user)
        response = self.client.get('/')
        curr_user = response.wsgi_request.user
        self.assertEqual(curr_user, self.user)

    def test_view_url_exists_at_desired_location(self):
        self.client.force_login(self.user)
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('posts:base_view'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 200)
        assert 'base.html' in [t.name for t in response.templates]
        assert 'posts/main.html' in [t.name for t in response.templates]

    def test_paggination_is_invalid_less_than_6_pots(self):
        self.client.force_login(self.user)
        PostFactory.create_batch(5)

        response = self.client.get(reverse('posts:base_view'))
        self.assertEqual(response.status_code, 200)
        self.assertFalse('has_other_pages' in response.context)
        self.assertTrue(len(response.context['posts']) == 5)

    def test_paggination_is_valid(self):
        PostFactory.create_batch(15)
        paginator = Paginator(Post.objects.all(), 6)
        self.assertEqual(15, paginator.count)
        self.assertEqual(3, paginator.num_pages)
        self.assertEqual([1, 2, 3], list(paginator.page_range))

    def test_pagination_first_page(self):
        self.client.force_login(self.user)
        PostFactory.create_batch(15)

        response = self.client.get(reverse('posts:base_view')+'/?page=1')
        self.assertEqual(response.status_code, 200)
        paginator = response.context['paginator']
        p = paginator.page(1)
        self.assertEqual("<Page 1 of 3>", force_text(p))
        self.assertTrue(p.has_next())
        self.assertFalse(p.has_previous())
        self.assertTrue(p.has_other_pages())
        self.assertEqual(2, p.next_page_number())
        self.assertEqual(1, p.start_index())
        self.assertEqual(6, p.end_index())
        self.assertTrue(len(response.context['posts']) == 6)

    def test_pagination_last_page(self):
        self.client.force_login(self.user)
        PostFactory.create_batch(15)

        response = self.client.get(reverse('posts:base_view') + '/?page=3')
        self.assertEqual(response.status_code, 200)
        paginator = response.context['paginator']
        p = paginator.page(3)
        self.assertEqual("<Page 3 of 3>", force_text(p))
        self.assertFalse(p.has_next())
        self.assertTrue(p.has_previous())
        self.assertTrue(p.has_other_pages())
        self.assertEqual(2, p.previous_page_number())
        self.assertEqual(13, p.start_index())
        self.assertEqual(15, p.end_index())



class TestListViewFilterByLikeAndComments(TestCase):

    @classmethod
    def setUp(cls):
        cls.client = Client()
        cls.user = UserFactory(is_active=True)
        cls.url = reverse('posts:base_view')

        cls.pr1 = PostFactory()
        LikeFactory.create_batch(2, post = cls.pr1)
        CommentFactory.create_batch(2, post=cls.pr1)

        cls.pr2 = PostFactory()
        LikeFactory.create_batch(2, post=cls.pr2)
        CommentFactory.create_batch(2, post=cls.pr2)

        cls.pr3 = PostFactory()
        LikeFactory.create_batch(2, post=cls.pr3)

        cls.pr4 = PostFactory()
        CommentFactory.create_batch(2, post=cls.pr4)

        cls.pr5 = PostFactory()

    def test_filter_posts_by_existed_likes(self):
        response = self.client.get(self.url)
        likes = Like.objects.values_list('post__title', flat=True).distinct().count()
        self.assertEqual(likes, 3)

    def test_filter_post_without_likes(self):
        response = self.client.get(self.url)
        likes = Like.objects.values_list('post', flat=True).distinct()
        res = Post.objects.exclude(pk__in=likes).count()
        self.assertEqual(res, 2)

    def test_filter_post_by_existed_comment(self):
        response = self.client.get(self.url)
        res = Comment.objects.values_list('post__title', flat=True).distinct().count()
        self.assertEqual(res, 3)

    def test_filter_post_without_comment(self):
        response = self.client.get(self.url)
        comment = Comment.objects.values_list('post', flat=True).distinct()
        res = Post.objects.exclude(pk__in=comment).count()
        self.assertEqual(res, 2)