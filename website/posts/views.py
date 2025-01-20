from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
<<<<<<< HEAD
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.db.models import Count, Q, Exists, OuterRef
from .models import Post, Comment, PollOption, PostImage
from fitness.models import Workout, Achievement, UserAchievement
from users.models import UserFollowing
from django.views.decorators.http import require_POST
import logging
logger = logging.getLogger(__name__)

User = get_user_model()

class HomeView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'posts/home.html'
    context_object_name = 'posts'
    paginate_by = 10
    ordering = ['-created_at']

    def get_queryset(self):
        return Post.objects.select_related('author').prefetch_related(
            'likes', 'post_comments', 'poll_options'
        ).filter(fitnesspost__isnull=True)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Sugestões para seguir (usuários mais ativos que o usuário atual não segue)
        following_users = UserFollowing.objects.filter(
            user=self.request.user,
            following_user=OuterRef('pk')
        )
        
        context['suggestions'] = User.objects.annotate(
            posts_count=Count('posts'),
            followers_count=Count('followers')
        ).exclude(
            id=self.request.user.id
        ).exclude(
            Exists(following_users)
        ).order_by('-posts_count', '-followers_count')[:5]
        
        # Conquistas do usuário
        context['user_achievements'] = UserAchievement.objects.filter(
            user=self.request.user
        ).select_related('achievement').order_by('-created_at')[:4]
        
        # Treinos recentes do usuário
        context['recent_workouts'] = Workout.objects.filter(
            creator=self.request.user
        ).prefetch_related('exercises').order_by('-created_at')[:3]
        
        return context
=======
from django.contrib import messages
from django.utils import timezone
from django.http import JsonResponse
from .models import Post, PostImage, Comment, PollOption
from django.views.generic import TemplateView
>>>>>>> 1bc9d9e56d8d9d501d44190eefe542470fb6ea9f

@login_required
def create_post(request):
    if request.method == 'POST':
<<<<<<< HEAD
        content = request.POST.get('content')
        images = request.FILES.getlist('images')
        post_type = request.POST.get('post_type', 'text')
        
        # Verifica se há mais de 3 imagens
        if len(images) > 3:
            messages.error(request, 'Você pode enviar no máximo 3 imagens por post.')
            return redirect('home')
        
        # Cria o post
        post = Post.objects.create(
            author=request.user,
            content=content,
            post_type=post_type if post_type != 'image' or images else 'image'
        )
        
        # Se houver imagens, cria os objetos PostImage
        if images:
            for image in images:
                PostImage.objects.create(
                    post=post,
                    image=image
                )
        
        # Se for uma enquete, criar as opções
        if post_type == 'poll':
            poll_options = request.POST.getlist('poll_options[]')
            for option_text in poll_options:
                if option_text.strip():  # Só cria se não estiver vazio
                    PollOption.objects.create(
                        post=post,
                        text=option_text.strip()
                    )
            
            # Se não tiver opções válidas, exclui o post e retorna erro
            if not post.poll_options.exists():
                post.delete()
                messages.error(request, 'A enquete precisa ter pelo menos uma opção válida.')
                return redirect('home')
        
        messages.success(request, 'Post criado com sucesso!')
        return redirect('home')
    return redirect('home')

@login_required
@require_POST
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    user = request.user
    
    if user in post.likes.all():
        post.likes.remove(user)
        liked = False
    else:
        post.likes.add(user)
        liked = True
    
    return JsonResponse({
        'liked': liked,
        'likes_count': post.likes.count()
    })

@login_required
@require_POST
def like_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    user = request.user
    
    if user in comment.likes.all():
        comment.likes.remove(user)
        liked = False
    else:
        comment.likes.add(user)
        liked = True
    
    return JsonResponse({
        'liked': liked,
        'likes_count': comment.likes.count()
=======
        post_type = request.POST.get('post_type', 'regular')
        content = request.POST.get('content', '')
        
        # Criar o post
        post = Post.objects.create(
            user=request.user,
            content=content,
            post_type=post_type
        )
        
        # Processar imagens se houver
        if 'images' in request.FILES:
            for image in request.FILES.getlist('images'):
                PostImage.objects.create(post=post, image=image)
        
        # Processar opções de enquete se for do tipo poll
        if post_type == 'poll':
            poll_options = request.POST.getlist('poll_options[]')
            for option_text in poll_options:
                if option_text.strip():  # Só cria opção se não estiver vazia
                    PollOption.objects.create(post=post, text=option_text.strip())
        
        messages.success(request, 'Post criado com sucesso!')
        return redirect('home')
    
    return redirect('home')

@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user in post.likes.all():
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user)
        liked = True
    return JsonResponse({
        'likes_count': post.likes.count(),
        'liked': liked
    })

@login_required
def like_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.user in comment.likes.all():
        comment.likes.remove(request.user)
        liked = False
    else:
        comment.likes.add(request.user)
        liked = True
    return JsonResponse({
        'likes_count': comment.likes.count(),
        'liked': liked
>>>>>>> 1bc9d9e56d8d9d501d44190eefe542470fb6ea9f
    })

@login_required
def comment_post(request, post_id):
<<<<<<< HEAD
    if request.method == 'POST':
        post = get_object_or_404(Post, id=post_id)
        content = request.POST.get('content')
        
        if not content:
            messages.error(request, 'O comentário não pode estar vazio.')
            return redirect('home')
        
        comment = post.add_comment(
            author=request.user,
            content=content
        )
        
        messages.success(request, 'Comentário adicionado com sucesso!')
        return redirect('home')
=======
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
>>>>>>> 1bc9d9e56d8d9d501d44190eefe542470fb6ea9f
    return redirect('home')

@login_required
def edit_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
<<<<<<< HEAD
    
    if comment.author != request.user:
=======
    if comment.user != request.user:
>>>>>>> 1bc9d9e56d8d9d501d44190eefe542470fb6ea9f
        messages.error(request, 'Você não tem permissão para editar este comentário.')
        return redirect('home')
    
    if request.method == 'POST':
        content = request.POST.get('content')
<<<<<<< HEAD
        
        if not content:
            messages.error(request, 'O comentário não pode estar vazio.')
            return redirect('home')
        
        comment.content = content
        comment.edited = True
        comment.save()
        
        messages.success(request, 'Comentário atualizado com sucesso!')
        return redirect('home')
=======
        if content:
            comment.content = content
            comment.edited = True
            comment.edited_at = timezone.now()
            comment.save()
            messages.success(request, 'Comentário atualizado com sucesso!')
        else:
            messages.error(request, 'O comentário não pode estar vazio.')
>>>>>>> 1bc9d9e56d8d9d501d44190eefe542470fb6ea9f
    return redirect('home')

@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
<<<<<<< HEAD
    
    if comment.author != request.user:
=======
    if comment.user != request.user:
>>>>>>> 1bc9d9e56d8d9d501d44190eefe542470fb6ea9f
        messages.error(request, 'Você não tem permissão para excluir este comentário.')
        return redirect('home')
    
    comment.delete()
    messages.success(request, 'Comentário excluído com sucesso!')
    return redirect('home')

@login_required
def vote_poll(request, option_id):
<<<<<<< HEAD
    try:
        option = get_object_or_404(PollOption, id=option_id)
        
        logger.error(f"Vote attempt - User: {request.user}, Option: {option.text}")
        logger.error(f"Request method: {request.method}")
        
        if request.method != 'POST':
            logger.error("Not a POST request")
            return JsonResponse({'error': 'Método inválido'}, status=405)
        
        # Realiza o toggle do voto
        voted = option.toggle_vote(request.user)
        
        # Recupera os dados atualizados das opções
        poll_options = option.post.poll_options.all()
        options_data = [{
            'id': opt.id,
            'text': opt.text,
            'votes_count': opt.votes_count,
            'percentage': opt.percentage,
            'voted': request.user in opt.votes.all()
        } for opt in poll_options]
        
        logger.error(f"Vote result - Voted: {voted}, Options: {options_data}")
        
        return JsonResponse({
            'voted': voted,
            'options': options_data
        })
    
    except Exception as e:
        logger.error(f"Error in vote_poll: {str(e)}")
        return JsonResponse({'error': str(e)}, status=500)
=======
    option = get_object_or_404(PollOption, id=option_id)
    post = option.post
    
    # Remove votos anteriores do usuário nesta enquete
    for old_option in post.poll_options.all():
        old_option.votes.remove(request.user)
    
    # Adiciona o novo voto
    option.votes.add(request.user)
    
    # Se for uma requisição HTMX, retorna o template parcial
    if request.headers.get('HX-Request'):
        return render(request, 'posts/poll_options.html', {'post': post})
        
    return redirect('home')

class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = Post.objects.all().order_by('-created_at')
        return context
>>>>>>> 1bc9d9e56d8d9d501d44190eefe542470fb6ea9f
