from django.db import models
from django.conf import settings
from django.utils import timezone
from django.db.models import Count
from django.core.exceptions import ValidationError
from core.models import TimestampedModel, LikeableModel, ContentModel
from django.contrib.auth import get_user_model

User = get_user_model()

class Post(TimestampedModel, LikeableModel, ContentModel):
    POST_TYPES = [
        ('text', 'Texto'),
        ('image', 'Imagem'),
        ('poll', 'Enquete'),
    ]
    
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts',
        null=True,
        blank=True
    )
    post_type = models.CharField(
        max_length=10,
        choices=POST_TYPES,
        default='text'
    )
    edited = models.BooleanField(default=False)
    edited_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        author_name = self.author.get_full_name() if self.author else 'Unknown'
        return f'Post by {author_name} at {self.created_at}'

    def add_comment(self, author, content):
        return Comment.objects.create(
            post=self,
            author=author,
            content=content
        )

    @property
    def comments_count(self):
        return self.post_comments.count()

    @property
    def poll_options_list(self):
        if self.post_type == 'poll':
            return self.poll_options.all()
        return []

    def save(self, *args, **kwargs):
        if self.edited and not self.edited_at:
            self.edited_at = timezone.now()
        super().save(*args, **kwargs)

class Comment(TimestampedModel, LikeableModel, ContentModel):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='post_comments'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        null=True,
        blank=True
    )
    edited = models.BooleanField(default=False)
    edited_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        author_name = self.author.get_full_name() if self.author else 'Unknown'
        return f'Comment by {author_name} on {self.post}'

    def save(self, *args, **kwargs):
        if self.edited and not self.edited_at:
            self.edited_at = timezone.now()
        super().save(*args, **kwargs)

class PollOption(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='poll_options'
    )
    text = models.CharField(max_length=200)
    votes = models.ManyToManyField(
        User,
        related_name='poll_votes',
        blank=True
    )

    def __str__(self):
        return str(self.text)

    @property
    def votes_count(self):
        return self.votes.count()

    @property
    def percentage(self):
        total_votes = sum(option.votes.count() for option in self.post.poll_options.all())
        if total_votes > 0:
            return (self.votes.count() / total_votes) * 100
        return 0

    def toggle_vote(self, user):
        # Log para depuração
        print(f"Toggle vote - User: {user}, Option: {self.text}")
        print(f"Current votes: {list(self.votes.all())}")
        
        # Verifica se o usuário já votou em alguma opção desta enquete
        existing_vote = self.post.poll_options.filter(votes=user).first()
        
        # Log adicional
        print(f"Existing vote: {existing_vote}")
        
        if existing_vote:
            # Se já votou na mesma opção, remove o voto
            if existing_vote == self:
                self.votes.remove(user)
                print("Removing vote from same option")
                return False
            else:
                # Remove o voto da opção anterior
                existing_vote.votes.remove(user)
                print(f"Removing vote from option: {existing_vote.text}")
        
        # Adiciona o voto na opção atual
        self.votes.add(user)
        print(f"Adding vote to option: {self.text}")
        return True

class PostImage(TimestampedModel):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='posts/images/')

    class Meta:
        ordering = ['created_at']
