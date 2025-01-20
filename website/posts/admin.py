from django.contrib import admin
<<<<<<< HEAD
from .models import Post, Comment, PollOption

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('author', 'post_type', 'created_at', 'edited')
    list_filter = ('post_type', 'created_at', 'edited')
    search_fields = ('content', 'author__username')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'post', 'created_at', 'edited')
    list_filter = ('created_at', 'edited')
    search_fields = ('content', 'author__username')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(PollOption)
class PollOptionAdmin(admin.ModelAdmin):
    list_display = ('text', 'post', 'votes_count')
    search_fields = ('text', 'post__content')
    readonly_fields = ('votes_count',)
=======

# Register your models here.
>>>>>>> 1bc9d9e56d8d9d501d44190eefe542470fb6ea9f
