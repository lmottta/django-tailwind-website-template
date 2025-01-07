// Função para alternar a visibilidade dos comentários adicionais
function toggleAdditionalComments(postId) {
    const additionalComments = document.getElementById(`additional-comments-${postId}`);
    const toggleButton = document.getElementById(`toggle-comments-btn-${postId}`);
    
    if (additionalComments.classList.contains('hidden')) {
        additionalComments.classList.remove('hidden');
        toggleButton.textContent = 'Mostrar menos comentários';
    } else {
        additionalComments.classList.add('hidden');
        toggleButton.textContent = 'Mostrar mais comentários';
    }
}

// Função para dar like em um post
async function likePost(postId) {
    try {
        const response = await fetch(`/posts/${postId}/like/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
                'Content-Type': 'application/json'
            }
        });
        
        if (response.ok) {
            const data = await response.json();
            const likeCount = document.getElementById(`post-likes-${postId}`);
            const likeIcon = document.querySelector(`#post-like-icon-${postId}`);
            
            likeCount.textContent = data.likes_count;
            
            if (data.liked) {
                likeIcon.classList.add('text-red-500');
            } else {
                likeIcon.classList.remove('text-red-500');
            }
        }
    } catch (error) {
        console.error('Erro ao dar like:', error);
    }
}

// Função para dar like em um comentário
async function likeComment(commentId) {
    try {
        const response = await fetch(`/posts/comment/${commentId}/like/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
                'Content-Type': 'application/json'
            }
        });
        
        if (response.ok) {
            const data = await response.json();
            const likeCount = document.getElementById(`comment-likes-${commentId}`);
            const likeIcon = document.querySelector(`#comment-like-icon-${commentId}`);
            
            likeCount.textContent = data.likes_count;
            
            if (data.liked) {
                likeIcon.classList.add('text-red-500');
            } else {
                likeIcon.classList.remove('text-red-500');
            }
        }
    } catch (error) {
        console.error('Erro ao dar like no comentário:', error);
    }
}

// Função auxiliar para obter o token CSRF
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Função para editar comentário
function editComment(commentId) {
    const contentDiv = document.getElementById(`comment-content-${commentId}`);
    const form = document.getElementById(`comment-form-${commentId}`);
    
    contentDiv.classList.add('hidden');
    form.classList.remove('hidden');
}

// Função para cancelar edição de comentário
function cancelEditComment(commentId) {
    const contentDiv = document.getElementById(`comment-content-${commentId}`);
    const form = document.getElementById(`comment-form-${commentId}`);
    
    contentDiv.classList.remove('hidden');
    form.classList.add('hidden');
} 