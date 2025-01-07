from django.db import models
from django.conf import settings
from django.utils.text import slugify

class Exercise(models.Model):
    MUSCLE_GROUP_CHOICES = [
        ('chest', 'Peito'),
        ('back', 'Costas'),
        ('shoulders', 'Ombros'),
        ('legs', 'Pernas'),
        ('arms', 'Braços'),
        ('abs', 'Abdômen'),
        ('cardio', 'Cardio'),
    ]

    EQUIPMENT_CHOICES = [
        ('none', 'Nenhum'),
        ('dumbbells', 'Halteres'),
        ('barbell', 'Barra'),
        ('machine', 'Máquina'),
        ('cables', 'Cabos'),
        ('bodyweight', 'Peso Corporal'),
    ]

    name = models.CharField('Nome', max_length=100)
    description = models.TextField('Descrição')
    muscle_group = models.CharField('Grupo Muscular', max_length=20, choices=MUSCLE_GROUP_CHOICES)
    equipment = models.CharField('Equipamento', max_length=20, choices=EQUIPMENT_CHOICES)
    image = models.ImageField('Imagem', upload_to='exercises/', blank=True, null=True)
    video_url = models.URLField('URL do Vídeo', blank=True, null=True)
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)

    class Meta:
        verbose_name = 'Exercício'
        verbose_name_plural = 'Exercícios'
        ordering = ['name']

    def __str__(self):
        return self.name

class Workout(models.Model):
    title = models.CharField('Título', max_length=100)
    description = models.TextField('Descrição')
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='created_workouts',
        verbose_name='Criador'
    )
    exercises = models.ManyToManyField(Exercise, through='WorkoutExercise')
    is_public = models.BooleanField('Público', default=True)
    likes = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='liked_workouts',
        blank=True,
        verbose_name='Curtidas'
    )
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)
    slug = models.SlugField(unique=True, max_length=100)

    class Meta:
        verbose_name = 'Treino'
        verbose_name_plural = 'Treinos'
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

class WorkoutExercise(models.Model):
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE)
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    sets = models.PositiveIntegerField('Séries')
    reps = models.CharField('Repetições', max_length=50)  # Permite formatos como "8-12" ou "Até falha"
    rest_time = models.PositiveIntegerField('Tempo de Descanso (segundos)')
    order = models.PositiveIntegerField('Ordem', default=0)

    class Meta:
        verbose_name = 'Exercício do Treino'
        verbose_name_plural = 'Exercícios do Treino'
        ordering = ['order']
        unique_together = ['workout', 'order']

    def __str__(self):
        return f"{self.exercise.name} - {self.sets}x{self.reps}"

class Post(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name='Autor'
    )
    content = models.TextField('Conteúdo')
    image = models.ImageField('Imagem', upload_to='posts/', blank=True, null=True)
    workout = models.ForeignKey(
        Workout,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='posts',
        verbose_name='Treino'
    )
    likes = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='liked_posts',
        blank=True,
        verbose_name='Curtidas'
    )
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)

    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'
        ordering = ['-created_at']

    def __str__(self):
        return f"Post de {self.author.get_full_name()} em {self.created_at.strftime('%d/%m/%Y')}"

class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Post'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Usuário'
    )
    content = models.TextField('Conteúdo')
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)

    class Meta:
        verbose_name = 'Comentário'
        verbose_name_plural = 'Comentários'
        ordering = ['created_at']

    def __str__(self):
        return f"Comentário de {self.user.get_full_name()} em {self.created_at.strftime('%d/%m/%Y')}"

class Achievement(models.Model):
    name = models.CharField('Nome', max_length=100)
    description = models.TextField('Descrição')
    icon = models.ImageField('Ícone', upload_to='achievements/')
    requirement = models.TextField('Requisito')
    points = models.PositiveIntegerField('Pontos')

    class Meta:
        verbose_name = 'Conquista'
        verbose_name_plural = 'Conquistas'
        ordering = ['name']

    def __str__(self):
        return self.name

class UserAchievement(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='achievements',
        verbose_name='Usuário'
    )
    achievement = models.ForeignKey(
        Achievement,
        on_delete=models.CASCADE,
        related_name='users',
        verbose_name='Conquista'
    )
    achieved_at = models.DateTimeField('Conquistado em', auto_now_add=True)

    class Meta:
        verbose_name = 'Conquista do Usuário'
        verbose_name_plural = 'Conquistas do Usuário'
        unique_together = ['user', 'achievement']
        ordering = ['-achieved_at']

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.achievement.name}"
