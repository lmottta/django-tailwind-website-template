from django.urls import path
from . import views

<<<<<<< HEAD
app_name = 'fitness'

urlpatterns = [
    path('workouts/', views.workout_list, name='workout_list'),
    path('workouts/create/', views.workout_create, name='workout_create'),
    path('workouts/<slug:slug>/', views.workout_detail, name='workout_detail'),
    path('workouts/<slug:slug>/edit/', views.workout_edit, name='workout_edit'),
    path('workouts/<slug:slug>/delete/', views.workout_delete, name='workout_delete'),
    path('exercises/', views.exercise_list, name='exercise_list'),
=======
urlpatterns = [
    # Workout URLs
    path('workouts/', views.workout_list, name='workouts'),
    path('workouts/create/', views.workout_create, name='workout_create'),
    path('workouts/<int:pk>/', views.workout_detail, name='workout_detail'),
    path('workouts/<int:pk>/edit/', views.workout_edit, name='workout_edit'),
    path('workouts/<int:pk>/delete/', views.workout_delete, name='workout_delete'),
    
    # Exercise URLs
    path('exercises/', views.exercise_list, name='exercises'),
>>>>>>> 1bc9d9e56d8d9d501d44190eefe542470fb6ea9f
    path('exercises/create/', views.exercise_create, name='exercise_create'),
    path('exercises/<int:pk>/', views.exercise_detail, name='exercise_detail'),
    path('exercises/<int:pk>/edit/', views.exercise_edit, name='exercise_edit'),
    path('exercises/<int:pk>/delete/', views.exercise_delete, name='exercise_delete'),
<<<<<<< HEAD
    path('achievements/', views.achievement_list, name='achievement_list'),
=======
    
    # Post URLs
    path('posts/create/', views.create_post, name='create_post'),
    path('posts/<int:pk>/like/', views.like_post, name='like_post'),
    path('posts/<int:pk>/comment/', views.add_comment, name='add_comment'),
    
    # Achievement URLs
    path('achievements/', views.achievement_list, name='achievements'),
>>>>>>> 1bc9d9e56d8d9d501d44190eefe542470fb6ea9f
]
