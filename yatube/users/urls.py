from django.contrib.auth.views import (
    LogoutView, 
    LoginView, 
    PasswordChangeView, 
    PasswordChangeDoneView, 
    PasswordResetView,     
    PasswordResetDoneView, 
    PasswordResetConfirmView, 
    PasswordResetCompleteView
    )
from django.urls import path, reverse_lazy

from users import views
from users.apps import UsersConfig


app_name = UsersConfig.name

urlpatterns = [
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('logout/', LogoutView.as_view(template_name='users/logged_out.html'), name='logout'),
    path('login/', LoginView.as_view(template_name='users/login.html'), name='login'),
    path(
        'password_change/', 
        PasswordChangeView.as_view(template_name='users/password_change_form.html'), 
        name='password_change_form'
    ),
    path(
        'password_change/done/', 
        PasswordChangeDoneView.as_view(template_name='users/password_change_done.html'),
        name='password_change_done'
    ),
    path(
        'password_reset/',
        PasswordResetView.as_view(
            template_name="users/password_reset_form.html",
            email_template_name="users/password_reset_email.html",
            success_url=reverse_lazy("users:password_reset_done")
        ), 
        name='password_reset_form'
    ),
    path(
        'password_reset/done/', 
        PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'),
        name='password_reset_done'
    ),
    path(
        'reset/<uidb64>/<token>/',
        PasswordResetConfirmView.as_view(
            template_name="users/password_reset_confirm.html",
            success_url=reverse_lazy("users:password_reset_complete")
        ), 
        name='password_reset_confirm'
    ),
    path(
        'reset/done/', 
        PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'),
        name='password_reset_complete'
    ),
]
