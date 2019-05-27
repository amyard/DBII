from django import forms
from .models import Post
from bootstrap_modal_forms.forms import BSModalForm


class PostForm(BSModalForm):

    class Meta:
        model = Post
        fields = ['title', 'slug', 'content', 'image']

    def clean_title(self):
        title = self.cleaned_data['title']
        if Post.objects.filter(title=title).exists():
            raise forms.ValidationError('You cann\'t use this title again.')
        return title




class PostUpdateForm(BSModalForm):

    class Meta:
        model = Post
        fields = ['title', 'slug', 'content', 'image']

    def __init__(self, *args, **kwargs):
        self.pk = kwargs.pop('pk', '')
        super(PostUpdateForm, self).__init__(*args, **kwargs)

    def clean_title(self):
        title = self.cleaned_data['title']
        if Post.objects.exclude(pk=self.pk).filter(title=title).exists():
            raise forms.ValidationError('You cann\'t use this title again.')
        return title