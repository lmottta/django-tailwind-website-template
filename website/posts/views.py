from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.http import JsonResponse
from .models import Post, PostImage, Comment, PollOption
from django.views.generic import TemplateView

@login_required
def create_post(request):
    if request.method == 'POST':
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
    })

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
def edit_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if comment.user != request.user:
        messages.error(request, 'Você não tem permissão para editar este comentário.')
        return redirect('home')
    
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            comment.content = content
            comment.edited = True
            comment.edited_at = timezone.now()
            comment.save()
            messages.success(request, 'Comentário atualizado com sucesso!')
        else:
            messages.error(request, 'O comentário não pode estar vazio.')
    return redirect('home')

@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if comment.user != request.user:
        messages.error(request, 'Você não tem permissão para excluir este comentário.')
        return redirect('home')
    
    comment.delete()
    messages.success(request, 'Comentário excluído com sucesso!')
    return redirect('home')

@login_required
def vote_poll(request, option_id):
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
