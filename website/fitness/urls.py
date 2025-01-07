from django.urls import path
from . import views

urlpatterns = [
    # Workout URLs
    path('workouts/', views.workout_list, name='workouts'),
    path('workouts/create/', views.workout_create, name='workout_create'),
    path('workouts/<int:pk>/', views.workout_detail, name='workout_detail'),
    path('workouts/<int:pk>/edit/', views.workout_edit, name='workout_edit'),
    path('workouts/<int:pk>/delete/', views.workout_delete, name='workout_delete'),
    
    # Exercise URLs
    path('exercises/', views.exercise_list, name='exercises'),
    path('exercises/create/', views.exercise_create, name='exercise_create'),
    path('exercises/<int:pk>/', views.exercise_detail, name='exercise_detail'),
    path('exercises/<int:pk>/edit/', views.exercise_edit, name='exercise_edit'),
    path('exercises/<int:pk>/delete/', views.exercise_delete, name='exercise_delete'),
    
    # Post URLs
    path('posts/create/', views.create_post, name='create_post'),
    path('posts/<int:pk>/like/', views.like_post, name='like_post'),
    path('posts/<int:pk>/comment/', views.add_comment, name='add_comment'),
    
    # Achievement URLs
    path('achievements/', views.achievement_list, name='achievements'),
]
