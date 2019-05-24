from django.urls import path, reverse_lazy
from .views import CustomLogoutView, CustomLoginView, ActivateView, SignUpView, ProfileDetailView

from django.contrib.auth import views as auth_views


app_name='users'
urlpatterns = [
    path('logout/', CustomLogoutView.as_view(next_page = reverse_lazy('core:base_view')), name='logout'),
    path('signin/', CustomLoginView.as_view(), name='signin'),

    path('signup/', SignUpView.as_view(), name='signup'),
    path('activate/<uidb64>/<token>/', ActivateView.as_view(), name='activate'),

    path('user-detail/<int:pk>-<str:username>', ProfileDetailView.as_view(), name='user_detail'),

    # RESET PASSWORD
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='users/reset_password/password_reset.html',
                                                                 email_template_name='users/reset_password/password_reset_email.html',
                                                                 subject_template_name='users/reset_password/password_reset_subject.txt',
                                                                 success_url=reverse_lazy('users:password_reset_done')),
         name='password_reset'),
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(template_name='users/reset_password/password_reset_done.html'),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>',
         auth_views.PasswordResetConfirmView.as_view(template_name='users/reset_password/password_reset_confirm.html',
                                                     success_url=reverse_lazy('users:password_reset_complete')),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='users/reset_password/password_reset_complete.html'),
         name='password_reset_complete'),
]