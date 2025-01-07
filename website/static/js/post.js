// Funções para manipulação de posts
function toggleLike(postId) {
    fetch(`/posts/${postId}/like/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
        },
    })
    .then(response => response.json())
    .then(data => {
        const likeCount = document.getElementById(`likes-count-${postId}`);
        likeCount.textContent = data.likes_count;
        const heartIcon = likeCount.previousElementSibling;
        if (data.liked) {
            heartIcon.classList.add('text-red-500');
        } else {
            heartIcon.classList.remove('text-red-500');
        }
    });
}

function toggleComments(postId) {
    const commentsDiv = document.getElementById(`comments-${postId}`);
    commentsDiv.classList.toggle('hidden');
}

// Funções para manipulação do formulário de post
function showPostType(type) {
    // Atualiza o campo hidden
    document.getElementById('post_type').value = type;
    
    // Remove a classe active de todas as tabs
    document.querySelectorAll('.tab').forEach(tab => tab.classList.remove('tab-active'));
    
    // Adiciona a classe active na tab selecionada
    event.currentTarget.classList.add('tab-active');
    
    // Esconde todos os campos especiais
    document.getElementById('image-field').classList.add('hidden');
    document.getElementById('poll-fields').classList.add('hidden');
    
    // Mostra o campo específico
    if (type === 'image') {
        document.getElementById('image-field').classList.remove('hidden');
    } else if (type === 'poll') {
        document.getElementById('poll-fields').classList.remove('hidden');
    }
}

function addPollOption() {
    const pollOptions = document.getElementById('poll-options');
    const newOption = document.createElement('input');
    newOption.type = 'text';
    newOption.name = 'poll_options[]';
    newOption.className = 'input input-bordered w-full mb-2';
    newOption.placeholder = `Opção ${pollOptions.children.length + 1}`;
    pollOptions.appendChild(newOption);
}

// Funções para manipulação de enquetes
function votePoll(optionId) {
    fetch(`/posts/poll/option/${optionId}/vote/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
        },
    })
    .then(response => response.json())
    .then(data => {
        // Atualiza todas as opções da enquete
        data.options.forEach(option => {
            const optionElement = document.getElementById(`poll-option-${option.id}`);
            const progressBar = optionElement.querySelector('.progress-bar');
            const votesCount = optionElement.querySelector('.votes-count');
            const percentage = optionElement.querySelector('.percentage');
            
            // Atualiza a barra de progresso
            progressBar.style.width = `${option.percentage}%`;
            
            // Atualiza o contador de votos
            votesCount.textContent = `${option.votes_count} votos`;
            
            // Atualiza a porcentagem
            percentage.textContent = `${Math.round(option.percentage)}%`;
            
            // Atualiza o estado de votado
            if (option.voted) {
                optionElement.classList.add('voted');
            } else {
                optionElement.classList.remove('voted');
            }
        });
    });
}

// Funções para manipulação de comentários
function likeComment(commentId) {
    fetch(`/posts/comment/${commentId}/like/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
        },
    })
    .then(response => response.json())
    .then(data => {
        const likeCount = document.getElementById(`comment-likes-${commentId}`);
        likeCount.textContent = data.likes_count;
        const heartIcon = likeCount.previousElementSibling;
        if (data.liked) {
            heartIcon.classList.add('text-red-500');
        } else {
            heartIcon.classList.remove('text-red-500');
        }
    });
}

function editComment(commentId) {
    const commentContent = document.getElementById(`comment-content-${commentId}`);
    const commentForm = document.getElementById(`comment-form-${commentId}`);
    
    commentContent.classList.add('hidden');
    commentForm.classList.remove('hidden');
}

function cancelEditComment(commentId) {
    const commentContent = document.getElementById(`comment-content-${commentId}`);
    const commentForm = document.getElementById(`comment-form-${commentId}`);
    
    commentContent.classList.remove('hidden');
    commentForm.classList.add('hidden');
}

// Inicialização
document.addEventListener('DOMContentLoaded', function() {
    // Inicializa os tooltips
    const tooltips = document.querySelectorAll('[data-tooltip]');
    tooltips.forEach(tooltip => {
        tooltip.addEventListener('mouseenter', function() {
            const tooltipText = this.getAttribute('data-tooltip');
            const tooltipElement = document.createElement('div');
            tooltipElement.className = 'tooltip';
            tooltipElement.textContent = tooltipText;
            document.body.appendChild(tooltipElement);
            
            const rect = this.getBoundingClientRect();
            tooltipElement.style.top = `${rect.top - tooltipElement.offsetHeight - 5}px`;
            tooltipElement.style.left = `${rect.left + (rect.width - tooltipElement.offsetWidth) / 2}px`;
        });
        
        tooltip.addEventListener('mouseleave', function() {
            const tooltips = document.querySelectorAll('.tooltip');
            tooltips.forEach(tooltip => tooltip.remove());
        });
    });
});
