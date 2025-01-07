from django.contrib import admin
from .models import Exercise, Workout, WorkoutExercise, FitnessPost, Achievement, UserAchievement

@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    list_display = ('name', 'muscle_group', 'equipment')
    list_filter = ('muscle_group', 'equipment')
    search_fields = ('name', 'description')

class WorkoutExerciseInline(admin.TabularInline):
    model = WorkoutExercise
    extra = 1

@admin.register(Workout)
class WorkoutAdmin(admin.ModelAdmin):
    list_display = ('title', 'creator', 'is_public', 'created_at')
    list_filter = ('is_public', 'created_at')
    search_fields = ('title', 'description', 'creator__username')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [WorkoutExerciseInline]

@admin.register(FitnessPost)
class FitnessPostAdmin(admin.ModelAdmin):
    list_display = ('author', 'workout', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('content', 'author__username')
    date_hierarchy = 'created_at'

@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = ('name', 'points')
    search_fields = ('name', 'description', 'requirement')

@admin.register(UserAchievement)
class UserAchievementAdmin(admin.ModelAdmin):
    list_display = ('user', 'achievement', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'achievement__name')
