from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q
from users.models import CustomUser
from .models import Exercise, Workout, WorkoutExercise, Post, Comment, Achievement, UserAchievement

@login_required
def workout_list(request):
    workouts = Workout.objects.filter(
        Q(creator=request.user) | Q(is_public=True)
    ).exclude(
        creator__in=request.user.blocking.all()
    ).order_by('-created_at')
    return render(request, 'fitness/workout_list.html', {'workouts': workouts})

@login_required
def workout_create(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        is_public = request.POST.get('is_public', False) == 'on'
        
        workout = Workout.objects.create(
            title=title,
            description=description,
            creator=request.user,
            is_public=is_public
        )
        
        # Handle exercises
        exercises = request.POST.getlist('exercises[]')
        sets = request.POST.getlist('sets[]')
        reps = request.POST.getlist('reps[]')
        rest_times = request.POST.getlist('rest_times[]')
        
        for i, exercise_id in enumerate(exercises):
            WorkoutExercise.objects.create(
                workout=workout,
                exercise_id=exercise_id,
                sets=sets[i],
                reps=reps[i],
                rest_time=rest_times[i],
                order=i+1
            )
        
        messages.success(request, 'Workout created successfully!')
        return redirect('workout_detail', pk=workout.pk)
    
    exercises = Exercise.objects.all()
    return render(request, 'fitness/workout_form.html', {'exercises': exercises})

@login_required
def workout_detail(request, pk):
    workout = get_object_or_404(Workout, pk=pk)
    if not workout.is_public and workout.creator != request.user:
        messages.error(request, 'You do not have permission to view this workout.')
        return redirect('workout_list')
    return render(request, 'fitness/workout_detail.html', {'workout': workout})

@login_required
def workout_edit(request, pk):
    workout = get_object_or_404(Workout, pk=pk)
    if workout.creator != request.user:
        messages.error(request, 'You do not have permission to edit this workout.')
        return redirect('workout_list')
    
    if request.method == 'POST':
        workout.title = request.POST.get('title')
        workout.description = request.POST.get('description')
        workout.is_public = request.POST.get('is_public', False) == 'on'
        workout.save()
        
        # Update exercises
        workout.workoutexercise_set.all().delete()
        exercises = request.POST.getlist('exercises[]')
        sets = request.POST.getlist('sets[]')
        reps = request.POST.getlist('reps[]')
        rest_times = request.POST.getlist('rest_times[]')
        
        for i, exercise_id in enumerate(exercises):
            WorkoutExercise.objects.create(
                workout=workout,
                exercise_id=exercise_id,
                sets=sets[i],
                reps=reps[i],
                rest_time=rest_times[i],
                order=i+1
            )
        
        messages.success(request, 'Workout updated successfully!')
        return redirect('workout_detail', pk=workout.pk)
    
    exercises = Exercise.objects.all()
    return render(request, 'fitness/workout_form.html', {
        'workout': workout,
        'exercises': exercises
    })

@login_required
def workout_delete(request, pk):
    workout = get_object_or_404(Workout, pk=pk)
    if workout.creator != request.user:
        messages.error(request, 'You do not have permission to delete this workout.')
        return redirect('workout_list')
    
    workout.delete()
    messages.success(request, 'Workout deleted successfully!')
    return redirect('workout_list')

@login_required
def exercise_list(request):
    exercises = Exercise.objects.all()
    return render(request, 'fitness/exercise_list.html', {'exercises': exercises})

@login_required
def exercise_create(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        muscle_group = request.POST.get('muscle_group')
        equipment = request.POST.get('equipment')
        video_url = request.POST.get('video_url')
        image = request.FILES.get('image')
        
        exercise = Exercise.objects.create(
            name=name,
            description=description,
            muscle_group=muscle_group,
            equipment=equipment,
            video_url=video_url,
            image=image
        )
        
        messages.success(request, 'Exercise created successfully!')
        return redirect('exercise_detail', pk=exercise.pk)
    
    return render(request, 'fitness/exercise_form.html')

@login_required
def exercise_detail(request, pk):
    exercise = get_object_or_404(Exercise, pk=pk)
    return render(request, 'fitness/exercise_detail.html', {'exercise': exercise})

@login_required
def exercise_edit(request, pk):
    exercise = get_object_or_404(Exercise, pk=pk)
    if request.method == 'POST':
        exercise.name = request.POST.get('name')
        exercise.description = request.POST.get('description')
        exercise.muscle_group = request.POST.get('muscle_group')
        exercise.equipment = request.POST.get('equipment')
        exercise.video_url = request.POST.get('video_url')
        
        if 'image' in request.FILES:
            exercise.image = request.FILES['image']
        
        exercise.save()
        messages.success(request, 'Exercise updated successfully!')
        return redirect('exercise_detail', pk=exercise.pk)
    
    return render(request, 'fitness/exercise_form.html', {'exercise': exercise})

@login_required
def exercise_delete(request, pk):
    exercise = get_object_or_404(Exercise, pk=pk)
    exercise.delete()
    messages.success(request, 'Exercise deleted successfully!')
    return redirect('exercise_list')

@login_required
def create_post(request):
    if request.method == 'POST':
        content = request.POST.get('content')
        image = request.FILES.get('image')
        
        post = Post.objects.create(
            user=request.user,
            content=content,
            image=image
        )
        
        messages.success(request, 'Post created successfully!')
        return redirect('home')
    return redirect('home')

@login_required
def like_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user in post.likes.all():
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user)
        liked = True
    
    return JsonResponse({
        'liked': liked,
        'likes_count': post.likes.count()
    })

@login_required
def add_comment(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        content = request.POST.get('content')
        comment = Comment.objects.create(
            user=request.user,
            post=post,
            content=content
        )
        return JsonResponse({
            'status': 'success',
            'comment': {
                'user': comment.user.get_full_name(),
                'content': comment.content,
                'created_at': comment.created_at.strftime('%b %d, %Y %H:%M')
            }
        })
    return JsonResponse({'status': 'error'}, status=400)

@login_required
def achievement_list(request):
    user_achievements = UserAchievement.objects.filter(user=request.user)
    available_achievements = Achievement.objects.exclude(
        id__in=user_achievements.values_list('achievement_id', flat=True)
    )
    return render(request, 'fitness/achievement_list.html', {
        'user_achievements': user_achievements,
        'available_achievements': available_achievements
    })
