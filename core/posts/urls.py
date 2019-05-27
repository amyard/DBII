from django.urls import path
from .views import PostListView, PostDetailView, PostCreateView, PostUpdateView, BookDeleteView, CommentCreateView


app_name='posts'

urlpatterns = [
    path('', PostListView.as_view(), name='base_view'),

    path('add_comment/', CommentCreateView.as_view(), name='add_comment'),
    path('post-detail/<str:post_slug>', PostDetailView.as_view(), name='post_detail'),
    path('post-update/<str:post_slug>', PostUpdateView.as_view(), name='post_update'),
    path('post-delete/<int:pk>', BookDeleteView.as_view(), name='post_delete'),
    path('post-create', PostCreateView.as_view(), name='post_create'),
]