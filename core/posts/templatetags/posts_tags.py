from django import template
from django.db.models import Count, Case, When
from ..models import Post, Like, Comment


register = template.Library()


@register.simple_tag
def most_liked_posts(count=5):
    uniq_ids = Like.objects.values('post').annotate(count=Count('post')).order_by('-count')[:count].values_list('post', flat=True)
    preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(uniq_ids)])
    res = Post.objects.filter(id__in=uniq_ids).order_by(preserved)
    return res

@register.simple_tag
def most_commented_posts(count=5):
    uniq_ids = Comment.objects.values('post').annotate(count=Count('post')).order_by('-count')[:count].values_list('post', flat=True)
    preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(uniq_ids)])
    res = Post.objects.filter(id__in=uniq_ids).order_by(preserved)
    return res


@register.simple_tag
def newest_posts(count=12):
    res = Post.objects.all()[:count]
    return res