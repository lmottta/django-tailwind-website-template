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
    }
}

function addPollOption() {
    const pollOptions = document.getElementById('poll-options');
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
        },
    })
    .then(response => response.json())
    .then(data => {
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
            }
        });
    });
}

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
}

// Inicialização
document.addEventListener('DOMContentLoaded', function() {
    // Remover mensagens após 5 segundos
    const messages = document.querySelectorAll('#messages-container .alert');
    messages.forEach(message => {
        setTimeout(() => {
            message.style.opacity = '0';
            setTimeout(() => message.remove(), 300);
        }, 5000);
    });
});
