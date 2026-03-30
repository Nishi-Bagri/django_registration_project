from django.urls import path
from .views import register, user_login, profile, logout_user, edit_profile, user_list
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('profile/', profile, name='profile'),
    path('logout/', logout_user, name='logout'),
    path('edit-profile/', edit_profile, name= 'edit_profile'),
    path('users/', user_list, name='user_list'),

    # Password reset urls

     path(
        'password_reset/',
        auth_views.PasswordResetView.as_view(template_name='users/password_reset.html'),
        name='password_reset'
    ),

    path(
        'password_reset/done/',
        auth_views.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'),
        name='password_reset_done'
    ),

    path(
        'reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'),
        name='password_reset_confirm'
    ),

    path(
        'reset/done/',
        auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'),
        name='password_reset_complete'
    ),

       path(
        'change-password/',
        auth_views.PasswordChangeView.as_view(template_name='users/change_password.html'),
        name='change_password'
    ),
    path(
        'change-password/done/',
        auth_views.PasswordChangeDoneView.as_view(template_name='users/change_password_done.html'),
        name='password_change_done'
    ),
    
]
