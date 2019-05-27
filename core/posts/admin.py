from django.contrib import admin
from django.db import models
from .models import Post, Comment
from tinymce.widgets import TinyMCE


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author',)
    list_display_links = ('title', )
    search_fields = ['author', 'title']
    list_filter = ['created']
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('created','modified')

    fieldsets = (
        ('Title', {'fields':('title', 'slug',)}),
        ('General info', {'fields':('author', 'content', 'image',)}),
        ('Create/Update', {'fields':('created','modified',)})
    )

    formfield_overrides = {
        models.TextField: {'widget':TinyMCE()}
    }



@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'user',)
    search_fields = ['post']

    fieldsets = [
        ('Post name', {'fields': ['post']}),
        ('User Info', {'fields': ['user']}),
        ('Content', {'fields': ['text']})
    ]