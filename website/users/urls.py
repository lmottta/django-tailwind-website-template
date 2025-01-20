from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

<<<<<<< HEAD
app_name = 'users'

=======
>>>>>>> 1bc9d9e56d8d9d501d44190eefe542470fb6ea9f
urlpatterns = [
    # Authentication URLs
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),  # Usando nossa própria view de logout
    path('register/', views.register, name='register'),
    
    # Password Reset URLs
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='users/password_reset.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'), name='password_reset_complete'),
    
    # Profile URLs
    path('profile/', views.profile, name='profile'),
    path('settings/', views.settings, name='settings'),
    path('delete-account/', views.delete_account, name='delete_account'),
    path('anamnesis/create/', views.anamnesis_create, name='anamnesis_create'),
    path('anamnesis/edit/', views.anamnesis_edit, name='anamnesis_edit'),
<<<<<<< HEAD
    path('profile/edit/', views.profile_edit, name='profile_edit'),
    path('profile/preferences/', views.preferences, name='preferences'),
    path('profile/privacy/', views.privacy, name='privacy'),
    path('profile/notifications/', views.notifications, name='notifications'),
=======
>>>>>>> 1bc9d9e56d8d9d501d44190eefe542470fb6ea9f
    
    # Social URLs
    path('follow/<int:user_id>/', views.follow_user, name='follow_user'),
    path('unfollow/<int:user_id>/', views.unfollow_user, name='unfollow_user'),
    path('block/<int:user_id>/', views.block_user, name='block_user'),
    path('unblock/<int:user_id>/', views.unblock_user, name='unblock_user'),
    path('search/', views.user_search, name='user_search'),
    
    # Post URLs
    path('post/create/', views.create_post, name='create_post'),
    path('post/<int:post_id>/like/', views.like_post, name='like_post'),
    path('post/<int:post_id>/comment/', views.comment_post, name='comment_post'),
]
