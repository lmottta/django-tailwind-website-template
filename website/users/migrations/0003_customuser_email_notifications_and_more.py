# Generated by Django 5.1.3 on 2025-01-06 14:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_remove_userachievement_achievement_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='email_notifications',
            field=models.BooleanField(default=True, verbose_name='Notificações por E-mail'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='follower_notifications',
            field=models.BooleanField(default=True, verbose_name='Notificações de Seguidores'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='login_notifications',
            field=models.BooleanField(default=True, verbose_name='Notificações de Login'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='private_profile',
            field=models.BooleanField(default=False, verbose_name='Perfil Privado'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='show_workout_stats',
            field=models.BooleanField(default=True, verbose_name='Mostrar Estatísticas de Treino'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='two_factor_auth',
            field=models.BooleanField(default=False, verbose_name='Autenticação de Dois Fatores'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='workout_notifications',
            field=models.BooleanField(default=True, verbose_name='Notificações de Treinos'),
        ),
    ]
