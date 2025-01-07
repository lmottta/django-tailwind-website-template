from django.db import models
from users.models import CustomUser

# Create your models here.

class Post(models.Model):
    POST_TYPE_CHOICES = [
        ('regular', 'Regular Post'),
        ('poll', 'Poll')
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='posts_created')
    content = models.TextField()
    post_type = models.CharField(max_length=10, choices=POST_TYPE_CHOICES, default='regular')
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(CustomUser, related_name='posts_liked', blank=True)
    edited = models.BooleanField(default=False)
    edited_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f'Post by {self.user.username} at {self.created_at}'

    class Meta:
        ordering = ['-created_at']

    @property
    def likes_count(self):
        return self.likes.count()

    @property
    def comments_count(self):
        return self.post_comments.count()

class PostImage(models.Model):
    post = models.ForeignKey(Post, related_name='post_images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='post_images/')
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f'Image {self.order + 1} for {self.post}'

class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='post_comments', on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, related_name='posts_comments', on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    edited = models.BooleanField(default=False)
    edited_at = models.DateTimeField(null=True, blank=True)
    likes = models.ManyToManyField(CustomUser, related_name='posts_comments_liked', blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'Comment by {self.user.username} on {self.post}'

    @property
    def likes_count(self):
        return self.likes.count()

class PollOption(models.Model):
    post = models.ForeignKey(Post, related_name='poll_options', on_delete=models.CASCADE)
    text = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    votes = models.ManyToManyField(CustomUser, related_name='poll_votes', blank=True)

    def __str__(self):
        return self.text

    @property
    def votes_count(self):
        return self.votes.count()

    @property
    def percentage(self):
        total_votes = sum(option.votes.count() for option in self.post.poll_options.all())
        if total_votes > 0:
            return int((self.votes.count() / total_votes) * 100)
        return 0
