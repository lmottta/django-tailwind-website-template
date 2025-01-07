from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.utils import timezone
from django.core.exceptions import ValidationError
from core.models import TimestampedModel, LikeableModel, ContentModel
from posts.models import Post as BasePost

class Exercise(TimestampedModel):
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

    class Meta:
        verbose_name = 'Exercício'
        verbose_name_plural = 'Exercícios'
        ordering = ['name']

    def __str__(self):
        return str(self.name)

    def clean(self):
        if not self.description:
            raise ValidationError('A descrição do exercício é obrigatória.')

class Workout(TimestampedModel, LikeableModel):
    title = models.CharField('Título', max_length=100)
    description = models.TextField('Descrição')
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='created_workouts',
        verbose_name='Criador'
    )
    exercises = models.ManyToManyField(
        Exercise,
        through='WorkoutExercise',
        verbose_name='Exercícios'
    )
    is_public = models.BooleanField('Público', default=True)
    slug = models.SlugField(unique=True, max_length=100)

    class Meta:
        verbose_name = 'Treino'
        verbose_name_plural = 'Treinos'
        ordering = ['-created_at']

    def __str__(self):
        return str(self.title)

    def clean(self):
        if not self.description:
            raise ValidationError('A descrição do treino é obrigatória.')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def toggle_like(self, user):
        if user in self.likes.all():
            self.likes.remove(user)
            return False
        self.likes.add(user)
        return True

    @property
    def total_exercises(self):
        return self.workoutexercise_set.count()

    def add_exercise(self, exercise, sets, reps, rest_time, order=None):
        if order is None:
            order = self.workoutexercise_set.count() + 1
        return WorkoutExercise.objects.create(
            workout=self,
            exercise=exercise,
            sets=sets,
            reps=reps,
            rest_time=rest_time,
            order=order
        )

class WorkoutExercise(models.Model):
    workout = models.ForeignKey(
        Workout,
        on_delete=models.CASCADE,
        verbose_name='Treino'
    )
    exercise = models.ForeignKey(
        Exercise,
        on_delete=models.CASCADE,
        verbose_name='Exercício'
    )
    sets = models.PositiveIntegerField('Séries')
    reps = models.CharField('Repetições', max_length=50)
    rest_time = models.PositiveIntegerField('Tempo de Descanso (segundos)')
    order = models.PositiveIntegerField('Ordem', default=0)

    class Meta:
        verbose_name = 'Exercício do Treino'
        verbose_name_plural = 'Exercícios do Treino'
        ordering = ['order']
        unique_together = ['workout', 'order']

    def __str__(self):
        return f"{self.exercise.name} - {self.sets}x{self.reps}"

    def clean(self):
        if self.sets < 1:
            raise ValidationError('O número de séries deve ser maior que zero.')
        if self.rest_time < 0:
            raise ValidationError('O tempo de descanso não pode ser negativo.')

class FitnessPost(BasePost):
    """
    Extensão do modelo Post base para posts específicos de fitness,
    adicionando relacionamento com workouts
    """
    workout = models.ForeignKey(
        Workout,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='posts',
        verbose_name='Treino'
    )

    class Meta:
        verbose_name = 'Post de Fitness'
        verbose_name_plural = 'Posts de Fitness'

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
        return str(self.name)

    def clean(self):
        if self.points < 0:
            raise ValidationError('A pontuação não pode ser negativa.')

class UserAchievement(TimestampedModel):
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
    created_at = models.DateTimeField('Conquistado em', default=timezone.now)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)

    class Meta:
        verbose_name = 'Conquista do Usuário'
        verbose_name_plural = 'Conquistas do Usuário'
        unique_together = ['user', 'achievement']
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user} - {self.achievement.name}"

    def clean(self):
        if self.pk is None:  # Só valida na criação
            existing = UserAchievement.objects.filter(
                user=self.user,
                achievement=self.achievement
            ).exists()
            if existing:
                raise ValidationError('O usuário já possui esta conquista.')
