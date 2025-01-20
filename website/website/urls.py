"""
URL configuration for website project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required
<<<<<<< HEAD
from posts.views import HomeView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', login_required(HomeView.as_view()), name='home'),
    path('home/', login_required(HomeView.as_view()), name='home'),
    path('users/', include('users.urls')),
    path('fitness/', include('fitness.urls')),
    path('posts/', include('posts.urls')),
    path('accounts/', include('allauth.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
=======
from django.shortcuts import redirect
from posts.views import HomeView

def redirect_to_login(request):
    return redirect('login')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', redirect_to_login, name='root'),  # Redireciona a raiz para o login
    path('home/', login_required(HomeView.as_view()), name='home'),
    path('users/', include('users.urls')),
    path('fitness/', include('fitness.urls')),
    path('posts/', include('posts.urls', namespace='posts')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
>>>>>>> 1bc9d9e56d8d9d501d44190eefe542470fb6ea9f
