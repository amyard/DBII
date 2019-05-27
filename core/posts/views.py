from django.shortcuts import render, reverse
from django.views.generic import ListView, DetailView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from .models import Post
from .forms import PostForm, PostUpdateForm

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




class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, BSModalUpdateView):
    model = Post
    template_name = 'posts/post_update.html'
    form_class = PostUpdateForm
    slug_url_kwarg = 'post_slug'
    success_message = 'Success: Post was updated.'

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(PostUpdateView, self).get_form_kwargs(*args, **kwargs)
        kwargs['pk'] = self.kwargs['pk']
        return kwargs

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        obj = self.kwargs['post_slug']
        return reverse('posts:detail-post', kwargs={'post_slug': obj})

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author or self.request.user == self.request.user.is_superuser:
            return True
        return False


class BookDeleteView(BSModalDeleteView):
    model = Post
    template_name = 'posts/post_delete.html'
    success_message = 'Success: Post was deleted.'
    success_url = reverse_lazy('posts:base_view')