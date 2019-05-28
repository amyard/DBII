from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.shortcuts import render, reverse
from django.views.generic import ListView, DetailView, View
from django.core.paginator import Paginator
from django.db.models import Count, Q, Case, When

from .models import Post, Comment, Like
from .forms import PostForm, PostUpdateForm, CommentForm, CommentUpdateForm, FilterForm

from bootstrap_modal_forms.generic import BSModalCreateView, BSModalUpdateView, BSModalDeleteView




class PostListView(ListView):
    template_name='posts/main.html'
    model = Post
    context_object_name='posts'
    paginate_by=2
    form = FilterForm

    def get_queryset(self, *args, **kwargs):
        qs = Post.objects.all()

        # Filter posts system
        filter_value = self.request.GET.get('position')
        if filter_value in ['2', '3', '4', '5']:
            if filter_value == '2':
                uniq_ids = Post.objects.values('id').annotate(count=Count('comments')).order_by('-count').values_list('id', flat=True)
            elif filter_value == '3':
                uniq_ids = Post.objects.values('id').annotate(count=Count('comments')).order_by('count').values_list('id', flat=True)
            elif filter_value == '4':
                uniq_ids = Post.objects.values('id').annotate(count=Count('likes')).order_by('-count').values_list('id',flat=True)
            elif filter_value == '5':
                uniq_ids = Post.objects.values('id').annotate(count=Count('comments')).order_by('count').values_list('id', flat=True)
            preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(uniq_ids)])
            qs = Post.objects.filter(id__in=uniq_ids).order_by(preserved)
        return qs


    def get_context_data(self, *args, **kwargs):
        context = super(PostListView, self).get_context_data(*args, **kwargs)
        context['profile'] = self.request.user
        context['form'] = self.form

        # for paggination if filter
        if self.request.GET.get('position'):
            context['filter_cond'] = f"?position={self.request.GET.get('position')}"
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

        # change color of Like/Dislike button
        context['buttons'] = Like.objects.filter(post=self.get_object(), user=self.request.user)
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
        kwargs['post_slug'] = self.kwargs['post_slug']
        return kwargs

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self, **kwargs):
        return reverse('posts:post_detail', kwargs={'post_slug': self.object.slug})

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


class LikeToggleView(View):
    def get(self, request, *args, **kwargs):
        post_id = self.request.GET.get('post_id')
        post = Post.objects.get(id=post_id)

        if not Like.objects.filter(post=post, user=self.request.user).exists():
            Like.objects.create(post=post, user=self.request.user)
            button = ['Dislike', 'danger']
        else:
            Like.objects.filter(post=post, user=self.request.user).delete()
            button = ['Like', 'success']

        res = Like.objects.filter(post__id=post_id).count()

        data = {
            'res': res,
            'button': button
        }
        return JsonResponse(data)


class SearchView(ListView):
    template_name = 'posts/main.html'
    model = Post
    context_object_name = 'posts'
    paginate_by = 1

    def get_queryset(self):
        qs = Post.objects.all()
        query = self.request.GET.get('q')
        if query:
            qs = Post.objects.filter(Q(title__icontains=query)|Q(content__icontains = query))
        return qs

    def get_context_data(self, *args, **kwargs):
        context = super(SearchView, self).get_context_data(*args, **kwargs)
        context['profile'] = self.request.user
        context['search_cond'] = f"?q={self.request.GET.get('q').replace(' ', '+')}"

        return context