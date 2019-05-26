from django.contrib import admin
from .models import Post


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