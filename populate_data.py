import os, django, random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()


from core.posts.models import Post, Comment, Like
from django.utils.text import slugify
from transliterate import translit
from django.core.files.images import ImageFile
from django.contrib.auth import get_user_model
from faker import Faker
import lorem


User = get_user_model()


def gen_slug(s):
    try:
        new_slug = slugify(translit(s, reversed=True, allow_unicode = True))
    except:
        new_slug = slugify(s, allow_unicode = True)
    return new_slug



def create_users(data):
    for i in data:
        User.objects.create(
            username = i,
            email = f'{i.lower()}@gmail.com',
            password = f'{i.lower()}',
            is_active=True
        )


def create_post(N):
    fake = Faker()
    for i in range(N):
        numb_text = random.randint(1, 4)
        pic = random.randint(1, 10)
        post = Post.objects.create(
            title=f'This is new title for Post № {i}',
            slug=gen_slug(f'Slug field for Post № {i}'),
            content = lorem.text()*numb_text,
            author = User.objects.order_by("?").first()
        )
        post.image = ImageFile(open(f'{os.getcwd()}/populate_data/{pic}.jpg', 'rb'))
        post.save()


def create_comments(N):
    fake = Faker()
    for _ in range(N):
        Comment.objects.create(
            post = Post.objects.order_by("?").first(),
            user = User.objects.order_by("?").first(),
            text = fake.text()
        )


def create_likes(N):
    for _ in range(N):
        post = Post.objects.order_by("?").first()
        user = User.objects.order_by("?").first()
        likes = Like.objects.filter(post=post).values_list('user__id', flat=True)

        like_obj = Like.objects.create(post = post)

        if user.id not in likes:
            like_obj.user = user
            like_obj.save()
        else:
            pass


def main():
    users = ['TestUser', 'NewUser', 'delme', 'ItsMe', 'Awesome']

    # create_users(users)
    create_post(50)
    create_comments(150)
    create_likes(75)


if __name__ == '__main__':
    main()
    print('Finish All.')