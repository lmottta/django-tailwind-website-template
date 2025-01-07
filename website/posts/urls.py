from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [
    path('create/', views.create_post, name='create_post'),
    path('<int:post_id>/like/', views.like_post, name='like_post'),
    path('comment/<int:comment_id>/like/', views.like_comment, name='like_comment'),
    path('<int:post_id>/comment/', views.comment_post, name='comment_post'),
    path('comment/<int:comment_id>/edit/', views.edit_comment, name='edit_comment'),
    path('comment/<int:comment_id>/delete/', views.delete_comment, name='delete_comment'),
    path('poll/option/<int:option_id>/vote/', views.vote_poll, name='vote_poll'),
]
