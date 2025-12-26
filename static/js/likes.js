document.addEventListener('DOMContentLoaded', function() {
    // Лайки картин
    document.querySelectorAll('.like-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            const paintingId = this.dataset.paintingId;
            const likeUrl = this.dataset.likeUrl;
            
            fetch(likeUrl, {
                method: 'POST',
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': getCookie('csrftoken')
                }
            })
            .then(response => response.json())
            .then(data => {
                const heartIcon = this.querySelector('i');
                const likeCount = document.getElementById(`like-count-${paintingId}`);
                
                if (data.liked) {
                    this.classList.add('liked');
                    heartIcon.classList.remove('text-gray-400');
                    heartIcon.classList.add('text-red-500');
                    this.style.transform = 'scale(1.2)';
                    setTimeout(() => { this.style.transform = 'scale(1)'; }, 300);
                } else {
                    this.classList.remove('liked');
                    heartIcon.classList.remove('text-red-500');
                    heartIcon.classList.add('text-gray-400');
                }
                
                likeCount.textContent = `${data.like_count} лайков`;
            });
        });
    });
    
    // Лайки художников
    document.querySelectorAll('.artist-like-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            const artistId = this.dataset.artistId;
            const likeUrl = this.dataset.likeUrl;
            
            fetch(likeUrl, {
                method: 'POST',
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': getCookie('csrftoken')
                }
            })
            .then(response => response.json())
            .then(data => {
                const likeCount = document.getElementById(`artist-like-count-${artistId}`);
                
                if (data.liked) {
                    this.classList.add('liked');
                    this.textContent = '✓ Подписан';
                    this.style.background = '#10b981';
                } else {
                    this.classList.remove('liked');
                    this.textContent = 'Подписаться';
                    this.style.background = 'var(--accent)';
                }
                
                likeCount.textContent = `${data.like_count} подписчиков`;
            });
        });
    });
    
    // Функция для получения CSRF токена
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
});