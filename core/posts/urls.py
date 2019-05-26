from django.urls import path
from .views import PostListView, PostDetailView


app_name='core'
urlpatterns = [
    path('', PostListView.as_view(), name='base_view'),
    path('post-detail/<str:post_slug>', PostDetailView.as_view(), name='post-detail'),
]