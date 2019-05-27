from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.utils.text import slugify
from django.urls import reverse

from model_utils.models import TimeStampedModel
import datetime


def gen_slug(s):
    new_slug = slugify(s, allow_unicode = True)
    return new_slug


def save_image_path(instance, filename):
    filename = instance.slug + '.jpg'
    date = instance.created.strftime("%Y-%m-%d %H:%M:%S").split(' ')[0]
    return f'posts_pics/{date}/{instance.slug}/{filename}'



class Post(TimeStampedModel):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(_('Name'), max_length=255, unique=True)
    slug = models.SlugField(_('Slug'), max_length=150, unique=True, blank=True)
    content = models.TextField(_('Content'))
    image = models.ImageField(default='default-post.png', upload_to=save_image_path, blank=True)

    class Meta:
        ordering = ['-created']

    def get_absolute_url(self):
        return reverse('posts:post_detail', kwargs={'post_slug':self.slug})

    def save(self, *args, **kwargs):
        self.slug = gen_slug(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title



class Comment(TimeStampedModel):
    post = models.ForeignKey(Post, related_name='comments', on_delete = models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, related_name='comments', on_delete = models.CASCADE)
    text = models.TextField(_('Comment'), max_length = 500)

    def __str__(self):
        return f'Comment from {self.user}'

    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'
        ordering = ['-id']


class Like(TimeStampedModel):
    post = models.ForeignKey(Post, related_name='likes', on_delete = models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, related_name='likes', on_delete = models.CASCADE)

    class Meta:
        unique_together = ['post', 'user']
        ordering = ['-id']

    def __str__(self):
        return f'{self.post} from {self.user.username}'