from django.urls import path, reverse_lazy
from .views import CustomLogoutView, CustomLoginView

app_name='users'
urlpatterns = [
    path('logout/', CustomLogoutView.as_view(next_page = reverse_lazy('core:base_view')), name='logout'),
    path('signin/', CustomLoginView.as_view(), name='signin'),
]