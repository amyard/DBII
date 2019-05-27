from django.urls import path
from .views import PostListView, PostDetailView, PostCreateView, PostUpdateView


app_name='posts'

urlpatterns = [
    path('', PostListView.as_view(), name='base_view'),
    path('post-detail/<str:post_slug>', PostDetailView.as_view(), name='post_detail'),
    path('post-update/<str:post_slug>', PostUpdateView.as_view(), name='post_update'),
    path('post-create', PostCreateView.as_view(), name='post_create'),
]