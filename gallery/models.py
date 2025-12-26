from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.db.models import Count
from django.db.models.signals import post_save
from django.dispatch import receiver

class Genre(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название жанра")
    description = models.TextField(blank=True, verbose_name="Описание")
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"

class Artist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='artist_profile', null=True, blank=True)
    first_name = models.CharField(max_length=100, verbose_name="Имя")
    last_name = models.CharField(max_length=100, verbose_name="Фамилия")
    birth_date = models.DateField(verbose_name="Дата рождения", null=True, blank=True)
    death_date = models.DateField(verbose_name="Дата смерти", null=True, blank=True)
    biography = models.TextField(verbose_name="Биография")
    country = models.CharField(max_length=100, verbose_name="Страна")
    portrait = models.ImageField(upload_to='artists/', verbose_name="Портрет", null=True, blank=True, help_text="Аватар художника")
    avatar = models.ImageField(upload_to='artists/avatars/', verbose_name="Аватар", null=True, blank=True, help_text="Аватар художника (если не указан, используется портрет)")
    
    # Соцсети
    has_social_networks = models.BooleanField(default=False, verbose_name="Есть социальные сети", help_text="Отметьте, если у художника есть социальные сети")
    instagram = models.URLField(blank=True, null=True, verbose_name="Instagram", help_text="Ссылка на профиль Instagram")
    artstation = models.URLField(blank=True, null=True, verbose_name="ArtStation", help_text="Ссылка на профиль ArtStation")
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    def get_absolute_url(self):
        return reverse('artist_detail', kwargs={'pk': self.pk})
    
    @property
    def like_count(self):
        """Количество подписчиков (followers)"""
        return self.followers.count()
    
    @property
    def followers_count(self):
        """Количество подписчиков (альтернативное название для ясности)"""
        return self.followers.count()
    
    @property
    def get_avatar(self):
        """Возвращает аватар или портрет"""
        try:
            # Пытаемся получить avatar, если поле существует в БД
            if hasattr(self, '_state') and hasattr(self._state, 'db'):
                # Проверяем через _meta, есть ли поле в модели
                field_names = [f.name for f in self._meta.get_fields()]
                if 'avatar' in field_names:
                    avatar_value = getattr(self, 'avatar', None)
                    if avatar_value:
                        return avatar_value
        except (AttributeError, Exception):
            pass
        # Если поле еще не создано в БД или пустое, используем portrait
        try:
            return self.portrait if self.portrait else None
        except (AttributeError, Exception):
            return None
    
    @property
    def has_any_social_network(self):
        """Проверяет, есть ли хотя бы одна социальная сеть"""
        return self.has_social_networks and (bool(self.instagram) or bool(self.artstation))
    
    class Meta:
        verbose_name = "Художник"
        verbose_name_plural = "Художники"

class Painting(models.Model):
    ART_TYPES = [
        ('classical', 'Классическая живопись'),
        ('modern', 'Современное искусство'),
        ('digital', 'Цифровое искусство'),
        ('other', 'Другое'),
    ]
    
    art_type = models.CharField(
        max_length=20, 
        choices=ART_TYPES, 
        default='classical',
        verbose_name="Тип искусства"
    )
    
    title = models.CharField(max_length=200, verbose_name="Название")
    artist = models.ForeignKey('Artist', on_delete=models.CASCADE, verbose_name="Художник", related_name='paintings')
    year = models.IntegerField(verbose_name="Год создания")
    technique = models.CharField(max_length=100, verbose_name="Техника")
    dimensions = models.CharField(max_length=100, verbose_name="Размеры", blank=True)
    location = models.CharField(max_length=200, verbose_name="Местонахождение", blank=True)
    image = models.ImageField(upload_to='paintings/', verbose_name="Изображение")
    description = models.TextField(verbose_name="Описание", blank=True)
    genres = models.ManyToManyField('Genre', verbose_name="Жанры")
    
    # Поле для лайков
    likes = models.ManyToManyField(User, related_name='liked_paintings', blank=True)
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('painting_detail', kwargs={'pk': self.pk})
    
    @property
    def like_count(self):
        return self.likes.count()
    
    def is_liked_by_user(self, user):
        """Проверяет, лайкнул ли пользователь картину"""
        if user.is_authenticated:
            return self.likes.filter(id=user.id).exists()
        return False
    
    class Meta:
        verbose_name = "Картина"
        verbose_name_plural = "Картины"

class UserProfile(models.Model):
    """Профиль пользователя с дополнительной информацией"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True, verbose_name="Биография")
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True, verbose_name="Аватар")
    
    # Подписки на художников
    following_artists = models.ManyToManyField(Artist, related_name='followers', blank=True, verbose_name="Подписки на художников")
    
    # Избранные картины
    favorite_paintings = models.ManyToManyField(Painting, related_name='favorited_by', blank=True, verbose_name="Избранные картины")
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    
    def __str__(self):
        return f"Профиль {self.user.username}"
    
    @property
    def following_count(self):
        return self.following_artists.count()
    
    @property
    def favorites_count(self):
        return self.favorite_paintings.count()
    
    def follow_artist(self, artist):
        """Подписаться на художника"""
        self.following_artists.add(artist)
        self.save()
    
    def unfollow_artist(self, artist):
        """Отписаться от художника"""
        self.following_artists.remove(artist)
        self.save()
    
    def is_following(self, artist):
        """Проверяет, подписан ли пользователь на художника"""
        return self.following_artists.filter(id=artist.id).exists()
    
    def add_to_favorites(self, painting):
        """Добавить картину в избранное"""
        self.favorite_paintings.add(painting)
        self.save()
    
    def remove_from_favorites(self, painting):
        """Удалить картину из избранного"""
        self.favorite_paintings.remove(painting)
        self.save()
    
    def is_in_favorites(self, painting):
        """Проверяет, есть ли картина в избранном"""
        return self.favorite_paintings.filter(id=painting.id).exists()
    
    class Meta:
        verbose_name = "Профиль пользователя"
        verbose_name_plural = "Профили пользователей"

class UserPreference(models.Model):
    """Модель для хранения предпочтений пользователя на основе его активности"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='preferences')
    favorite_genres = models.ManyToManyField(Genre, blank=True, verbose_name="Любимые жанры")
    favorite_artists = models.ManyToManyField(Artist, blank=True, verbose_name="Любимые художники")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    
    def __str__(self):
        return f"Предпочтения {self.user.username}"
    
    def update_preferences(self):
        """Обновляет предпочтения на основе активности пользователя"""
        # Любимые жанры (на основе лайков картин)
        liked_paintings = Painting.objects.filter(likes=self.user)
        favorite_genres = Genre.objects.filter(
            painting__in=liked_paintings
        ).annotate(
            count=Count('painting')
        ).order_by('-count')[:5]
        
        self.favorite_genres.set(favorite_genres)
        
        # Любимые художники (на основе лайков и подписок)
        favorite_artists = Artist.objects.filter(
            paintings__likes=self.user
        ).distinct()
        
        self.favorite_artists.set(favorite_artists)
        self.save()
    
    def get_recommended_paintings(self, limit=6):
        """Получить рекомендованные картины на основе предпочтений"""
        from django.db.models import Q
        
        # Если нет предпочтений, показываем популярные картины
        if not self.favorite_genres.exists() and not self.favorite_artists.exists():
            return Painting.objects.annotate(
                likes_count=Count('likes')
            ).order_by('-likes_count')[:limit]
        
        # Рекомендации на основе жанров и художников
        recommended = Painting.objects.filter(
            Q(genres__in=self.favorite_genres.all()) |
            Q(artist__in=self.favorite_artists.all())
        ).exclude(
            likes=self.user  # Исключаем уже лайкнутые
        ).distinct().annotate(
            likes_count=Count('likes')
        ).order_by('-likes_count')[:limit]
        
        return recommended
    
    def get_recommended_artists(self, limit=6):
        """Получить рекомендованных художников"""
        # Исключаем уже лайкнутых художников и тех, на кого уже подписан
        liked_artist_ids = self.favorite_artists.values_list('id', flat=True)
        
        # Рекомендуем художников с похожими жанрами
        favorite_genre_ids = self.favorite_genres.values_list('id', flat=True)
        
        recommended = Artist.objects.filter(
            paintings__genres__in=favorite_genre_ids
        ).exclude(
            id__in=liked_artist_ids
        ).exclude(
            followers=self.user  # Исключаем тех, на кого уже подписан
        ).distinct().annotate(
            painting_count=Count('paintings'),
            follower_count=Count('followers')
        ).order_by('-follower_count', '-painting_count')[:limit]
        
        return recommended
    
    class Meta:
        verbose_name = "Предпочтения пользователя"
        verbose_name_plural = "Предпочтения пользователей"

class Book(models.Model):
    """Модель книги по рисованию"""
    title = models.CharField(max_length=200, verbose_name="Название")
    author = models.CharField(max_length=200, verbose_name="Автор")
    description = models.TextField(verbose_name="Описание", blank=True)
    cover = models.ImageField(upload_to='books/covers/', verbose_name="Обложка")
    pdf_file = models.FileField(upload_to='books/pdfs/', verbose_name="PDF файл")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата добавления")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('book_detail', kwargs={'pk': self.pk})
    
    class Meta:
        verbose_name = "Книга"
        verbose_name_plural = "Книги"
        ordering = ['-created_at']

# Сигналы для автоматического создания профиля и предпочтений
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Автоматически создает профиль и предпочтения при создании пользователя"""
    if created:
        UserProfile.objects.create(user=instance)
        UserPreference.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Сохраняет профиль при сохранении пользователя"""
    if hasattr(instance, 'profile'):
        instance.profile.save()
    if hasattr(instance, 'preferences'):
        instance.preferences.save()

