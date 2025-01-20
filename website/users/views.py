from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.decorators.http import require_http_methods
from .models import CustomUser, Anamnesis, UserFollowing, UserBlock, Post, PostImage, Comment
from .forms import CustomUserCreationForm, CustomUserChangeForm, AnamnesisForm, UserUpdateForm, UserPreferencesForm, UserPrivacyForm, UserNotificationsForm

class CustomLoginView(LoginView):
    template_name = 'users/login.html'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        return reverse_lazy('home')
    
    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('home')
        return super().get(request, *args, **kwargs)

    def form_invalid(self, form):
        email = form.cleaned_data.get('username')  # Django usa username para o campo de email
        password = form.cleaned_data.get('password')
        
        user = authenticate(self.request, username=email, password=password)
        
        if user is None:
            # Verifica se o email existe
            try:
                CustomUser.objects.get(email=email)
                messages.error(self.request, 'Senha incorreta. Por favor, tente novamente.')
            except CustomUser.DoesNotExist:
                messages.error(self.request, 'Email não encontrado. Verifique se digitou corretamente.')
        
        return super().form_invalid(form)

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            # Especificando o backend de autenticação
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            messages.success(request, 'Registro realizado com sucesso!')
            return redirect('users:anamnesis_create')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def profile(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
    else:
        form = CustomUserChangeForm(instance=request.user)
    
    context = {
        'form': form,
        'anamnesis': Anamnesis.objects.filter(user=request.user).first(),
    }
    return render(request, 'users/profile.html', context)

@login_required
def anamnesis_create(request):
    try:
        anamnesis = Anamnesis.objects.get(user=request.user)
        return redirect('anamnesis_edit')
    except Anamnesis.DoesNotExist:
        if request.method == 'POST':
            form = AnamnesisForm(request.POST)
            if form.is_valid():
                anamnesis = form.save(commit=False)
                anamnesis.user = request.user
                anamnesis.save()
                messages.success(request, 'Anamnesis created successfully!')
                return redirect('profile')
        else:
            form = AnamnesisForm()
        return render(request, 'users/anamnesis_form.html', {'form': form})

@login_required
def anamnesis_edit(request):
    anamnesis = get_object_or_404(Anamnesis, user=request.user)
    if request.method == 'POST':
        form = AnamnesisForm(request.POST, instance=anamnesis)
        if form.is_valid():
            form.save()
            messages.success(request, 'Anamnesis updated successfully!')
            return redirect('profile')
    else:
        form = AnamnesisForm(instance=anamnesis)
    return render(request, 'users/anamnesis_form.html', {'form': form, 'edit': True})

@login_required
def follow_user(request, user_id):
    user_to_follow = get_object_or_404(CustomUser, id=user_id)
    if user_to_follow != request.user:
        UserFollowing.objects.get_or_create(
            user=request.user,
            following_user=user_to_follow
        )
        messages.success(request, f'You are now following {user_to_follow.get_full_name()}')
    return redirect('profile')

@login_required
def unfollow_user(request, user_id):
    user_to_unfollow = get_object_or_404(CustomUser, id=user_id)
    UserFollowing.objects.filter(
        user=request.user,
        following_user=user_to_unfollow
    ).delete()
    messages.success(request, f'You have unfollowed {user_to_unfollow.get_full_name()}')
    return redirect('profile')

@login_required
def block_user(request, user_id):
    user_to_block = get_object_or_404(CustomUser, id=user_id)
    if user_to_block != request.user:
        UserBlock.objects.get_or_create(
            user=request.user,
            blocked_user=user_to_block
        )
        # Remove any following relationships
        UserFollowing.objects.filter(
            Q(user=request.user, following_user=user_to_block) |
            Q(user=user_to_block, following_user=request.user)
        ).delete()
        messages.success(request, f'You have blocked {user_to_block.get_full_name()}')
    return redirect('profile')

@login_required
def unblock_user(request, user_id):
    user_to_unblock = get_object_or_404(CustomUser, id=user_id)
    UserBlock.objects.filter(
        user=request.user,
        blocked_user=user_to_unblock
    ).delete()
    messages.success(request, f'You have unblocked {user_to_unblock.get_full_name()}')
    return redirect('profile')

@login_required
def user_search(request):
    query = request.GET.get('q', '')
    if query:
        users = CustomUser.objects.filter(
            Q(username__icontains=query) |
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(email__icontains=query)
        ).exclude(
            id__in=UserBlock.objects.filter(user=request.user).values_list('blocked_user', flat=True)
        ).exclude(
            id__in=UserBlock.objects.filter(blocked_user=request.user).values_list('user', flat=True)
        )
    else:
        users = CustomUser.objects.none()
    
    return render(request, 'users/user_search.html', {'users': users, 'query': query})

@login_required
def settings(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, request.FILES, instance=request.user)
        if user_form.is_valid():
            user = user_form.save(commit=False)
            
            # Atualizar paleta de cores
            color_palette = request.POST.get('color_palette')
            if color_palette in dict(CustomUser.COLOR_PALETTE_CHOICES):
                user.color_palette = color_palette
            
            # Atualizar configurações de notificação
            user.email_notifications = request.POST.get('email_notifications') == 'on'
            user.follower_notifications = request.POST.get('follower_notifications') == 'on'
            user.workout_notifications = request.POST.get('workout_notifications') == 'on'
            user.login_notifications = request.POST.get('login_notifications') == 'on'
            
            # Atualizar configurações de privacidade
            user.private_profile = request.POST.get('private_profile') == 'on'
            user.show_workout_stats = request.POST.get('show_workout_stats') == 'on'
            
            # Atualizar configurações de segurança
            user.two_factor_auth = request.POST.get('two_factor_auth') == 'on'
            
            user.save()
            messages.success(request, 'Suas configurações foram atualizadas com sucesso!')
            return redirect('settings')
    else:
        user_form = UserUpdateForm(instance=request.user)
    
    return render(request, 'users/settings.html', {
        'user_form': user_form,
    })

@require_http_methods(["POST"])
def logout_view(request):
    logout(request)
    messages.success(request, 'Você saiu com sucesso!')
    return redirect('login')

@login_required
def delete_account(request):
    if request.method == 'POST':
        user = request.user
        # Fazer logout antes de deletar
        logout(request)
        # Deletar o usuário
        user.delete()
        messages.success(request, 'Sua conta foi excluída permanentemente.')
        return redirect('login')
    return redirect('settings')

@login_required
def create_post(request):
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            # Criar o post
            post = Post.objects.create(
                user=request.user,
                content=content
            )
            
            # Processar as imagens
            images = request.FILES.getlist('images')
            for index, image in enumerate(images[:3]):  # Limita a 3 imagens
                PostImage.objects.create(
                    post=post,
                    image=image,
                    order=index
                )
            
            messages.success(request, 'Post criado com sucesso!')
        else:
            messages.error(request, 'O conteúdo do post não pode estar vazio.')
    return redirect('home')

@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user in post.likes.all():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    return redirect('home')

@login_required
def comment_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            Comment.objects.create(
                post=post,
                user=request.user,
                content=content
            )
            messages.success(request, 'Comentário adicionado com sucesso!')
        else:
            messages.error(request, 'O comentário não pode estar vazio.')
    return redirect('home')

@login_required
def profile_edit(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Perfil atualizado com sucesso!')
            return redirect('users:profile_edit')
    else:
        form = CustomUserChangeForm(instance=request.user)
    
    return render(request, 'users/profile_edit.html', {
        'form': form
    })

@login_required
def preferences(request):
    if request.method == 'POST':
        user = request.user
        user.color_palette = request.POST.get('color_palette', 'default')
        user.email_notifications = request.POST.get('email_notifications') == 'on'
        user.push_notifications = request.POST.get('push_notifications') == 'on'
        user.account_privacy = request.POST.get('account_privacy') == 'on'
        user.save()
        
        messages.success(request, 'Preferências atualizadas com sucesso!')
        return redirect('users:preferences')
    
    return render(request, 'users/preferences.html')

@login_required
def privacy(request):
    if request.method == 'POST':
        form = UserPrivacyForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Configurações de privacidade atualizadas com sucesso!')
            return redirect('users:privacy')
    else:
        form = UserPrivacyForm(instance=request.user)
    
    return render(request, 'users/privacy.html', {
        'form': form
    })

@login_required
def notifications(request):
    if request.method == 'POST':
        form = UserNotificationsForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Configurações de notificações atualizadas com sucesso!')
            return redirect('users:notifications')
    else:
        form = UserNotificationsForm(instance=request.user)
    
    return render(request, 'users/notifications.html', {
        'form': form
    })
