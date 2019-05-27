from django import forms
from .models import Post
from bootstrap_modal_forms.forms import BSModalForm


class PostForm(BSModalForm):

    # slug = forms.TextInput(required=False)

    class Meta:
        model = Post
        fields = ['title', 'slug', 'content', 'image']

    def clean_title(self):
        title = self.cleaned_data['title']
        if Post.objects.filter(title=title).exists():
            raise forms.ValidationError('You cann\'t use this title again.')
        return title


