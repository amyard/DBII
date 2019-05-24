from django.urls import path, reverse_lazy
from .views import CustomLogoutView, CustomLoginView, ActivateView, SignUpView

app_name='users'
urlpatterns = [
    path('logout/', CustomLogoutView.as_view(next_page = reverse_lazy('core:base_view')), name='logout'),
    path('signin/', CustomLoginView.as_view(), name='signin'),

    path('signup/', SignUpView.as_view(), name='signup'),
    path('activate/<uidb64>/<token>/', ActivateView.as_view(), name='activate'),
]