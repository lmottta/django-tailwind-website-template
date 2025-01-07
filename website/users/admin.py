from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Anamnesis, UserFollowing, UserBlock, Post, PostImage, Comment

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'username', 'first_name', 'last_name', 'is_staff')
    search_fields = ('email', 'username', 'first_name', 'last_name')
    ordering = ('email',)

@admin.register(Anamnesis)
class AnamnesisAdmin(admin.ModelAdmin):
    list_display = ('user', 'weight', 'height', 'activity_level', 'created_at')
    search_fields = ('user__email', 'user__username')
    list_filter = ('activity_level', 'created_at')

@admin.register(UserFollowing)
class UserFollowingAdmin(admin.ModelAdmin):
    list_display = ('user', 'following_user', 'created_at')
    search_fields = ('user__email', 'following_user__email')
    list_filter = ('created_at',)

@admin.register(UserBlock)
class UserBlockAdmin(admin.ModelAdmin):
    list_display = ('user', 'blocked_user', 'created_at')
    search_fields = ('user__email', 'blocked_user__email')
    list_filter = ('created_at',)

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('user', 'content', 'created_at')
    search_fields = ('user__email', 'content')
    list_filter = ('created_at',)

@admin.register(PostImage)
class PostImageAdmin(admin.ModelAdmin):
    list_display = ('post', 'order', 'created_at')
    list_filter = ('created_at',)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'content', 'created_at')
    search_fields = ('user__email', 'content')
    list_filter = ('created_at',)
