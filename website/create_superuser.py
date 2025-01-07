import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'website.settings')
django.setup()

from users.models import CustomUser

# Criar superusuário se não existir
if not CustomUser.objects.filter(email='admin@example.com').exists():
    CustomUser.objects.create_superuser(
        'admin',
        'admin@example.com',
        'admin123',
        first_name='Admin',
        last_name='User'
    )
    print('Superuser created successfully!')
else:
    print('Superuser already exists.')
