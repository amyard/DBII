from django.urls import path
from .views import PostListView, PostDetailView, PostCreateView


app_name='posts'

urlpatterns = [
    path('', PostListView.as_view(), name='base_view'),
    path('post-detail/<str:post_slug>', PostDetailView.as_view(), name='post_detail'),
    path('post-create', PostCreateView.as_view(), name='post_create',)
]