from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
import os
import uuid

def profile_picture_path(instance, filename):
    # Pega a extensão do arquivo original
    ext = filename.split('.')[-1]
    # Gera um novo nome usando UUID
    filename = f'{uuid.uuid4().hex[:10]}.{ext}'
    # Retorna o caminho completo
    return os.path.join('profile_pics', filename)

class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('student', 'Aluno'),
        ('trainer', 'Personal'),
        ('admin', 'Admin'),
    )
    
    COLOR_PALETTES = [
        ('forest', 'Floresta'),
        ('sunset', 'Pôr do Sol'),
        ('royal', 'Real'),
    ]
    
    email = models.EmailField(_('email address'), unique=True)
    user_type = models.CharField('Tipo de Usuário', max_length=10, choices=USER_TYPE_CHOICES, default='student')
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    bio = models.TextField(max_length=500, blank=True)
    birth_date = models.DateField('Data de Nascimento', null=True, blank=True)
    fitness_goals = models.TextField('Objetivos Fitness', max_length=500, blank=True)
    color_palette = models.CharField(
        max_length=20,
        choices=COLOR_PALETTES,
        default='default',
        verbose_name='Paleta de Cores'
    )
    
    # Configurações de Notificação
    email_notifications = models.BooleanField(default=True)
    follower_notifications = models.BooleanField('Notificações de Seguidores', default=True)
    workout_notifications = models.BooleanField('Notificações de Treinos', default=True)
    login_notifications = models.BooleanField('Notificações de Login', default=True)
    
    # Configurações de Privacidade
    private_profile = models.BooleanField('Perfil Privado', default=False)
    show_workout_stats = models.BooleanField('Mostrar Estatísticas de Treino', default=True)
    
    # Configurações de Segurança
    two_factor_auth = models.BooleanField('Autenticação de Dois Fatores', default=False)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'

    def __str__(self):
        return self.get_full_name() or self.email

class Anamnesis(models.Model):
    ACTIVITY_LEVEL_CHOICES = [
        ('sedentary', 'Sedentário'),
        ('light', 'Leve'),
        ('moderate', 'Moderado'),
        ('active', 'Ativo'),
        ('very_active', 'Muito Ativo'),
    ]

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, verbose_name='Usuário')
    weight = models.DecimalField('Peso (kg)', max_digits=5, decimal_places=2)
    height = models.DecimalField('Altura (m)', max_digits=5, decimal_places=2)
    activity_level = models.CharField('Nível de Atividade', max_length=50, choices=ACTIVITY_LEVEL_CHOICES)
    goals = models.TextField('Objetivos')
    medical_restrictions = models.TextField('Restrições Médicas', blank=True)
    available_days = models.CharField('Dias Disponíveis', max_length=200)
    injury_history = models.TextField('Histórico de Lesões', blank=True)
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)

    class Meta:
        verbose_name = 'Anamnese'
        verbose_name_plural = 'Anamneses'

    def __str__(self):
        return f"Anamnese de {self.user.get_full_name()}"

class UserFollowing(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Usuário'
    )
    following_user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='followers',
        verbose_name='Seguindo'
    )
    created_at = models.DateTimeField('Criado em', auto_now_add=True)

    class Meta:
        verbose_name = 'Seguidor'
        verbose_name_plural = 'Seguidores'
        unique_together = ('user', 'following_user')

    def __str__(self):
        return f"{self.user.get_full_name()} segue {self.following_user.get_full_name()}"

class UserBlock(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='blocking',
        verbose_name='Usuário'
    )
    blocked_user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='blocked_by',
        verbose_name='Usuário Bloqueado'
    )
    created_at = models.DateTimeField('Criado em', auto_now_add=True)

    class Meta:
        verbose_name = 'Bloqueio'
        verbose_name_plural = 'Bloqueios'
        unique_together = ('user', 'blocked_user')

    def __str__(self):
        return f"{self.user.get_full_name()} bloqueou {self.blocked_user.get_full_name()}"

class Post(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='user_posts')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(CustomUser, related_name='user_liked_posts', blank=True)

    def __str__(self):
        return f'Post by {self.user.username} at {self.created_at}'

    class Meta:
        ordering = ['-created_at']

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
    user = models.ForeignKey(CustomUser, related_name='user_comments', on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'Comment by {self.user.username} on {self.post}'
