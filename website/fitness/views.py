from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Exercise, Workout, WorkoutExercise, UserAchievement, Achievement

@login_required
def workout_list(request):
    workouts = Workout.objects.all()
    return render(request, 'fitness/workout_list.html', {'workouts': workouts})

@login_required
def workout_create(request):
    return render(request, 'fitness/workout_form.html')

@login_required
def workout_detail(request, slug):
    workout = get_object_or_404(Workout, slug=slug)
    return render(request, 'fitness/workout_detail.html', {'workout': workout})

@login_required
def workout_edit(request, slug):
    workout = get_object_or_404(Workout, slug=slug)
    return render(request, 'fitness/workout_form.html', {'workout': workout})

@login_required
def workout_delete(request, slug):
    workout = get_object_or_404(Workout, slug=slug)
    if request.method == 'POST':
        workout.delete()
        messages.success(request, 'Treino excluído com sucesso.')
        return redirect('fitness:workout_list')
    return render(request, 'fitness/workout_confirm_delete.html', {'workout': workout})

@login_required
def exercise_list(request):
    exercises = Exercise.objects.all()
    return render(request, 'fitness/exercise_list.html', {'exercises': exercises})

@login_required
def exercise_create(request):
    return render(request, 'fitness/exercise_form.html')

@login_required
def exercise_detail(request, pk):
    exercise = get_object_or_404(Exercise, pk=pk)
    return render(request, 'fitness/exercise_detail.html', {'exercise': exercise})

@login_required
def exercise_edit(request, pk):
    exercise = get_object_or_404(Exercise, pk=pk)
    return render(request, 'fitness/exercise_form.html', {'exercise': exercise})

@login_required
def exercise_delete(request, pk):
    exercise = get_object_or_404(Exercise, pk=pk)
    if request.method == 'POST':
        exercise.delete()
        messages.success(request, 'Exercício excluído com sucesso.')
        return redirect('fitness:exercise_list')
    return render(request, 'fitness/exercise_confirm_delete.html', {'exercise': exercise})

@login_required
def achievement_list(request):
    user_achievements = UserAchievement.objects.filter(
        user=request.user
    ).select_related('achievement').order_by('-created_at')
    
    available_achievements = Achievement.objects.exclude(
        id__in=user_achievements.values_list('achievement_id', flat=True)
    )
    
    context = {
        'user_achievements': user_achievements,
        'available_achievements': available_achievements
    }
    return render(request, 'fitness/achievement_list.html', context)
