from django.urls import path
from .views import PostListView


app_name='core'
urlpatterns = [
    path('', PostListView.as_view(), name='base_view'),
]