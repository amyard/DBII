from django.urls import path
from .views import PostListView, PostDetailView, PostCreateView, PostUpdateView, BookDeleteView, CommentCreateView, CommentDeleteView, CommentUpdateView, LikeToggleView, SearchView


app_name='posts'

urlpatterns = [
    path('', PostListView.as_view(), name='base_view'),
    path('like/', LikeToggleView.as_view(), name='like_toggle'),
    path('search/', SearchView.as_view(), name='search'),

    path('add_comment/', CommentCreateView.as_view(), name='add_comment'),
    path('comment-delete/<int:pk>', CommentDeleteView.as_view(), name='comment_delete'),
    path('comment-update/<int:pk>', CommentUpdateView.as_view(), name='comment_update'),

    path('post-detail/<str:post_slug>', PostDetailView.as_view(), name='post_detail'),
    path('post-delete/<int:pk>', BookDeleteView.as_view(), name='post_delete'),
    path('post-update/<str:post_slug>', PostUpdateView.as_view(), name='post_update'),
    path('post-create', PostCreateView.as_view(), name='post_create'),
]