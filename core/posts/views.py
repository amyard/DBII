from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.shortcuts import render, reverse
from django.views.generic import ListView, DetailView, View
from django.core.paginator import Paginator

from .models import Post, Comment
from .forms import PostForm, PostUpdateForm, CommentForm, CommentUpdateForm

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
    form = CommentForm
    paginate_by = 3

    def get_context_data(self, *args, **kwargs):
        context = super(PostDetailView, self).get_context_data(*args, **kwargs)
        context['profile'] = self.request.user
        context['form'] = self.form

        # Pagination for comments
        p = Paginator(Comment.objects.filter(post=self.get_object()), self.paginate_by)
        page_number = self.request.GET.get('page', 1)
        page = p.get_page(page_number)
        context['comments'] = page
        return context


class PostCreateView(BSModalCreateView):
    template_name='posts/post_create.html'
    form_class=PostForm
    success_message = 'Success: Post was created.'
    success_url = reverse_lazy('posts:base_view')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


# class PostUpdateView(BSModalUpdateView):
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, BSModalUpdateView):
    model = Post
    template_name = 'posts/post_update.html'
    form_class = PostUpdateForm
    slug_url_kwarg = 'post_slug'
    success_message = 'Success: Post was updated.'

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(PostUpdateView, self).get_form_kwargs(*args, **kwargs)
        kwargs['post_slug'] = self.kwargs['post_slug']
        return kwargs

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self, **kwargs):
        return self.request.META.get('HTTP_REFERER')

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author or self.request.user.is_admin:
            return True
        return False


class BookDeleteView(BSModalDeleteView):
    model = Post
    template_name = 'posts/post_delete.html'
    success_message = 'Success: Post was deleted.'
    success_url = reverse_lazy('posts:base_view')


class CommentCreateView(View):
    def post(self, request, *args, **kwargs):
        post_id = self.request.POST.get('post_id')
        comment = self.request.POST.get('comment')

        if comment == '':
            return JsonResponse({}, safe=False)
        else:
            new_comment = Comment.objects.create(post=Post.objects.get(id=post_id), user=request.user, text=comment)
        count = Comment.objects.filter(post=Post.objects.get(id=post_id)).count()
        created = new_comment.created.strftime('%b %d, %Y, %I:%M %p').replace('PM', 'p.m.').replace('AM', 'a.m.')
        comment = [{'text': new_comment.text,
                    'created': created,
                    'count': count,
                    'ids': new_comment.id,
                    'user': self.request.user.username}]
        return JsonResponse(comment, safe=False)


class CommentDeleteView(BSModalDeleteView):
    model = Comment
    template_name = 'posts/comment_delete.html'
    success_message = 'Success: Comment was deleted.'

    def get_success_url(self, **kwargs):
        return self.request.META.get('HTTP_REFERER')


class CommentUpdateView(BSModalUpdateView):
    model = Comment
    form_class = CommentUpdateForm
    template_name = 'posts/comment_update.html'
    success_message = 'Success: Comment was updated.'

    def get_success_url(self, **kwargs):
        return self.request.META.get('HTTP_REFERER')