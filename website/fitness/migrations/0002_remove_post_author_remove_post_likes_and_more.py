# Generated by Django 5.1.3 on 2025-01-07 04:19

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fitness', '0001_initial'),
        ('posts', '0002_alter_comment_options_alter_polloption_options_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='author',
        ),
        migrations.RemoveField(
            model_name='post',
            name='likes',
        ),
        migrations.RemoveField(
            model_name='post',
            name='workout',
        ),
        migrations.AlterModelOptions(
            name='userachievement',
            options={'ordering': ['-created_at'], 'verbose_name': 'Conquista do Usuário', 'verbose_name_plural': 'Conquistas do Usuário'},
        ),
        migrations.RemoveField(
            model_name='userachievement',
            name='achieved_at',
        ),
        migrations.AddField(
            model_name='userachievement',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Conquistado em'),
        ),
        migrations.AddField(
            model_name='userachievement',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='Atualizado em'),
        ),
        migrations.AlterField(
            model_name='workout',
            name='exercises',
            field=models.ManyToManyField(through='fitness.WorkoutExercise', to='fitness.exercise', verbose_name='Exercícios'),
        ),
        migrations.AlterField(
            model_name='workout',
            name='likes',
            field=models.ManyToManyField(blank=True, related_name='%(class)s_likes', to=settings.AUTH_USER_MODEL, verbose_name='Curtidas'),
        ),
        migrations.AlterField(
            model_name='workoutexercise',
            name='exercise',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fitness.exercise', verbose_name='Exercício'),
        ),
        migrations.AlterField(
            model_name='workoutexercise',
            name='workout',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fitness.workout', verbose_name='Treino'),
        ),
        migrations.CreateModel(
            name='FitnessPost',
            fields=[
                ('post_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='posts.post')),
                ('workout', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='posts', to='fitness.workout', verbose_name='Treino')),
            ],
            options={
                'verbose_name': 'Post de Fitness',
                'verbose_name_plural': 'Posts de Fitness',
            },
            bases=('posts.post',),
        ),
        migrations.DeleteModel(
            name='Comment',
        ),
        migrations.DeleteModel(
            name='Post',
        ),
    ]
