from django.urls import path
from . import views

urlpatterns = [
    path('', views.blog_list, name='blog_list'),
    path('create/', views.create_blog, name='create_blog'),
    path('myblogs/', views.my_blogs, name='my_blogs'),
    path('edit/<int:id>/', views.edit_blog, name='edit_blog'),
    path('delete/<int:id>/', views.delete_blog, name='delete_blog'),
    path('details/<int:id>/', views.blog_detail, name='blog_detail'),

    path('pending-blogs/', views.pending_blogs, name='pending_blogs'),
    path('approve-blog/<int:id>/', views.approve_blog, name='approve_blog'),
    path('reject-blog/<int:id>/', views.reject_blog, name='reject_blog'),

    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-blogs/', views.admin_blog_list, name='admin_blog_list'),
    path('admin/users/', views.user_list, name='user_list'),

    path('upload-logo/', views.upload_logo, name='upload_logo'),

    # ✅ LIKE FEATURE
    path('like/<int:blog_id>/', views.toggle_like, name='toggle_like'),
    path('search-suggestions/',views.search_suggestions, name='search_suggestions'),

    path('comment/edit/<int:comment_id>/', views.edit_comment, name='edit_comment'),

    path('comment/delete/<int:comment_id>/', views.delete_comment, name='delete_comment'),
]