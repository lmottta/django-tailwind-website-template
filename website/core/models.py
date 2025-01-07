from django.db import models
from django.conf import settings

class TimestampedModel(models.Model):
    """Modelo base abstrato que fornece campos de timestamp"""
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)

    class Meta:
        abstract = True

class LikeableModel(models.Model):
    """Modelo base abstrato que fornece funcionalidade de likes"""
    likes = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='%(class)s_likes',
        verbose_name='Curtidas',
        blank=True
    )

    class Meta:
        abstract = True

    @property
    def likes_count(self):
        return self.likes.count()

class ContentModel(models.Model):
    """Modelo base abstrato que fornece campos de conteúdo"""
    content = models.TextField('Conteúdo')
    image = models.ImageField('Imagem', upload_to='%(class)s/', blank=True, null=True)

    class Meta:
        abstract = True
