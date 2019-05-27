from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.urls import reverse_lazy

from .models import Post
from .forms import PostForm

from bootstrap_modal_forms.generic import BSModalCreateView, BSModalUpdateView, BSModalDeleteView




class PostListView(ListView):
    template_name='posts/main.html'
    model = Post
    context_object_name='posts'
    paginate_by=2

    def get_context_data(self, *args, **kwargs):
        context = super(PostListView, self).get_context_data(*args, **kwargs)
        context['profile'] = self.request.user
        return context



class PostDetailView(DetailView):
    model = Post
    context_object_name = 'post'
    slug_url_kwarg = 'post_slug'


    def get_context_data(self, *args, **kwargs):
        context = super(PostDetailView, self).get_context_data(*args, **kwargs)
        context['profile'] = self.request.user
        return context


class PostCreateView(BSModalCreateView):
    template_name='posts/post_create.html'
    form_class=PostForm
    success_message = 'Success: Post was created.'
    success_url = reverse_lazy('posts:base_view')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)