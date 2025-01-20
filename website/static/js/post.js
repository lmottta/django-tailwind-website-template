<<<<<<< HEAD
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
=======
// Gerenciamento de imagens
function previewImages(input) {
    const preview = document.getElementById('image-preview');
    const imageCountElement = document.getElementById('imageCount');
    preview.innerHTML = '';
    let count = 0;

    if (input.files) {
        Array.from(input.files).slice(0, 3).forEach(file => {
            const reader = new FileReader();
            reader.onload = function(e) {
                const div = document.createElement('div');
                div.className = 'relative';
                div.innerHTML = `
                    <img src="${e.target.result}" class="w-full h-32 object-cover rounded-lg">
                    <button type="button" onclick="this.parentElement.remove(); updateImageCount();" 
                            class="absolute top-1 right-1 btn btn-circle btn-xs btn-error">×</button>
                `;
                preview.appendChild(div);
                count++;
                updateImageCount();
            };
            reader.readAsDataURL(file);
        });
    }
}

function updateImageCount() {
    const preview = document.getElementById('image-preview');
    const imageCountElement = document.getElementById('imageCount');
    const count = preview.children.length;
    imageCountElement.textContent = `${count}/3 imagens`;
}

// Gerenciamento de enquetes
function switchPostType(type) {
    const regularForm = document.getElementById('regularPostForm');
    const pollForm = document.getElementById('pollPostForm');
    const tabs = document.querySelectorAll('.tab');

    if (type === 'regular') {
        regularForm.classList.remove('hidden');
        pollForm.classList.add('hidden');
        tabs[0].classList.add('tab-active');
        tabs[1].classList.remove('tab-active');
    } else {
        regularForm.classList.add('hidden');
        pollForm.classList.remove('hidden');
        tabs[0].classList.remove('tab-active');
        tabs[1].classList.add('tab-active');
>>>>>>> 1bc9d9e56d8d9d501d44190eefe542470fb6ea9f
    }
}

function addPollOption() {
    const pollOptions = document.getElementById('poll-options');
<<<<<<< HEAD
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
=======
    if (!pollOptions) return;

    const optionsCount = pollOptions.children.length;
    if (optionsCount >= 5) return; // Limite de 5 opções

    const newOption = document.createElement('div');
    newOption.className = 'flex items-center gap-2';
    newOption.innerHTML = `
        <input type="text" name="poll_options[]" placeholder="Nova opção" 
            class="input input-bordered w-full focus:outline-none focus:border-teal-500">
        <button type="button" onclick="removePollOption(this)" class="btn btn-ghost btn-circle btn-sm">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd" />
            </svg>
        </button>
    `;
    pollOptions.appendChild(newOption);
}

function removePollOption(button) {
    const pollOptions = document.getElementById('poll-options');
    if (!pollOptions) return;

    const optionsCount = pollOptions.children.length;
    if (optionsCount > 2) {
        button.closest('.flex').remove();
    }
}

function previewImages(event) {
    const preview = document.getElementById('image-preview');
    if (!preview) return;

    preview.innerHTML = ''; // Limpa o preview atual
    const files = event.target.files;
    
    for (let i = 0; i < Math.min(files.length, 3); i++) {
        const file = files[i];
        if (file.type.startsWith('image/')) {
            const reader = new FileReader();
            const div = document.createElement('div');
            div.className = 'relative group';
            
            reader.onload = function(e) {
                div.innerHTML = `
                    <img src="${e.target.result}" class="w-full h-48 object-cover rounded-lg">
                    <button type="button" onclick="removeImage(this)" class="absolute top-2 right-2 btn btn-circle btn-sm bg-black/50 hover:bg-black/70 border-none text-white opacity-0 group-hover:opacity-100 transition-opacity">
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" viewBox="0 0 20 20" fill="currentColor">
                            <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd" />
                        </svg>
                    </button>
                `;
            };
            
            reader.readAsDataURL(file);
            preview.appendChild(div);
        }
    }
}

function removeImage(button) {
    const imageDiv = button.closest('.relative');
    if (imageDiv) {
        imageDiv.remove();
        // Limpa o input de arquivo para permitir selecionar a mesma imagem novamente
        const fileInput = document.querySelector('input[type="file"]');
        if (fileInput) {
            fileInput.value = '';
        }
    }
}

function openPollModal() {
    document.getElementById('poll-modal').showModal();
}

function openImageModal() {
    document.getElementById('image-modal').showModal();
}

// Interações com posts e comentários
function toggleMoreComments(postId) {
    const olderComments = document.getElementById(`older-comments-${postId}`);
    const toggleBtn = document.getElementById(`toggle-btn-${postId}`);
    
    if (olderComments.style.display === 'none') {
        olderComments.style.display = 'block';
        toggleBtn.textContent = 'Ver menos comentários';
    } else {
        olderComments.style.display = 'none';
        const commentCount = olderComments.querySelectorAll('.flex.gap-4').length;
        toggleBtn.textContent = `Ver mais comentários (${commentCount})`;
    }
}

function likePost(postId) {
    const likeButton = document.querySelector(`#like-button-${postId}`);
    const likeCount = document.querySelector(`#like-count-${postId}`);
    
    fetch(`/posts/${postId}/like/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),
>>>>>>> 1bc9d9e56d8d9d501d44190eefe542470fb6ea9f
        },
    })
    .then(response => response.json())
    .then(data => {
<<<<<<< HEAD
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
=======
        if (data.liked) {
            likeButton.classList.add('text-red-500');
        } else {
            likeButton.classList.remove('text-red-500');
        }
        likeCount.textContent = data.likes_count;
    });
}

function likeComment(commentId) {
    const likeSpan = document.getElementById(`comment-like-${commentId}`);
    
    fetch(`/posts/comment/${commentId}/like/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),
        },
    })
    .then(response => response.json())
    .then(data => {
        const text = data.liked ? 'Descurtir' : 'Curtir';
        likeSpan.textContent = `${text} (${data.likes_count})`;
    });
}

function votePoll(optionId) {
    fetch(`/posts/poll/option/${optionId}/vote/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),
        },
    })
    .then(response => response.json())
    .then(data => {
        // Atualizar a interface com os novos dados da enquete
        const pollOptions = document.querySelectorAll(`button[onclick^="votePoll"]`);
        data.poll_data.forEach(option => {
            const optionButton = Array.from(pollOptions).find(btn => btn.onclick.toString().includes(option.id));
            if (optionButton) {
                const voteCount = optionButton.querySelector('span:last-child');
                voteCount.textContent = `(${option.votes_count} votos)`;
>>>>>>> 1bc9d9e56d8d9d501d44190eefe542470fb6ea9f
            }
        });
    });
}

<<<<<<< HEAD
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
=======
// Função auxiliar para obter o cookie CSRF
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
>>>>>>> 1bc9d9e56d8d9d501d44190eefe542470fb6ea9f
}

// Inicialização
document.addEventListener('DOMContentLoaded', function() {
<<<<<<< HEAD
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
=======
    // Remover mensagens após 5 segundos
    const messages = document.querySelectorAll('#messages-container .alert');
    messages.forEach(message => {
        setTimeout(() => {
            message.style.opacity = '0';
            setTimeout(() => message.remove(), 300);
        }, 5000);
>>>>>>> 1bc9d9e56d8d9d501d44190eefe542470fb6ea9f
    });
});
