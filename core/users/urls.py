from django.urls import path, reverse_lazy
from .views import CustomLogoutView

app_name='users'
urlpatterns = [
    path('logout/', CustomLogoutView.as_view(next_page = reverse_lazy('core:base_view')), name='logout'),
]