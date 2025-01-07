from django.urls import path
from . import views

app_name = 'fitness'

urlpatterns = [
    path('workouts/', views.workout_list, name='workout_list'),
    path('workouts/create/', views.workout_create, name='workout_create'),
    path('workouts/<slug:slug>/', views.workout_detail, name='workout_detail'),
    path('workouts/<slug:slug>/edit/', views.workout_edit, name='workout_edit'),
    path('workouts/<slug:slug>/delete/', views.workout_delete, name='workout_delete'),
    path('exercises/', views.exercise_list, name='exercise_list'),
    path('exercises/create/', views.exercise_create, name='exercise_create'),
    path('exercises/<int:pk>/', views.exercise_detail, name='exercise_detail'),
    path('exercises/<int:pk>/edit/', views.exercise_edit, name='exercise_edit'),
    path('exercises/<int:pk>/delete/', views.exercise_delete, name='exercise_delete'),
    path('achievements/', views.achievement_list, name='achievement_list'),
]
