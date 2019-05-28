from django import forms
from .models import Post, Comment
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
        self.post_slug = kwargs.pop('post_slug', '')
        super(PostUpdateForm, self).__init__(*args, **kwargs)

    def clean_title(self):
        title = self.cleaned_data['title']
        if Post.objects.exclude(slug=self.post_slug).filter(title=title).exists():
            raise forms.ValidationError('You cann\'t use this title again.')
        return title


class CommentForm(forms.Form):
    text = forms.CharField(label='', widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'cols': 100, 'placeholder': 'Enter your comment'}))

    class Meta:
        model = Comment
        fields = ['text']


class CommentUpdateForm(BSModalForm):
    text = forms.CharField(label='', widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'cols': 100, 'placeholder': 'Enter your comment'}))
    class Meta:
        model = Comment
        fields = ['text']



class FilterForm(forms.Form):
    choices = (
        (1, 'All posts'),
        (2, 'Most commented posts'),
        (3, "Post without comments"),
        (4, "Most popular posts"),
        (5, "Posts without comments"),
    )
    position = forms.ChoiceField(label='', choices=choices, required=False, widget=forms.Select())