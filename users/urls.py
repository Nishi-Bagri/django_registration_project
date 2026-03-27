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
     # Change Password page
    path(
        'change-password/',
        auth_views.PasswordChangeView.as_view(
            template_name='users/change_password.html',
            success_url='/users/change-password-done/'  # redirect after success
        ),
        name='change_password'
    ),

    # Success page after changing password
    path(
        'change-password-done/',
        auth_views.PasswordChangeDoneView.as_view(
            template_name='users/change_password_done.html'
        ),
        name='password_change_done'
    ),
]
