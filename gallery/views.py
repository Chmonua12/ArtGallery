# gallery/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db.models import Q, Count



from .models import Painting, Artist, Genre, UserProfile, UserPreference, Book
from .forms import UserRegisterForm

def home(request):
    """Главная страница"""
    # Получаем классические и современные картины
    classical_paintings = Painting.objects.filter(art_type='classical').order_by('?')[:8]
    modern_paintings = Painting.objects.filter(art_type='modern').order_by('?')[:8]
    
    # Получаем художников
    artists = Artist.objects.all()[:6]
    
    # Рекомендации для авторизованных пользователей
    recommendations = None
    if request.user.is_authenticated and hasattr(request.user, 'preferences'):
        recommendations = request.user.preferences.get_recommended_paintings(limit=6)
    
    context = {
        'classical_paintings': classical_paintings,
        'modern_paintings': modern_paintings,
        'artists': artists,
        'recommendations': recommendations,
    }
    return render(request, 'gallery/home.html', context)

def painting_list(request):
    """Список всех картин"""
    paintings = Painting.objects.annotate(likes_count=Count('likes')).all()
    
    # Фильтрация по типу
    painting_type = request.GET.get('type')
    if painting_type:
        paintings = paintings.filter(art_type=painting_type)
    
    # Поиск
    search_query = request.GET.get('search')
    if search_query:
        paintings = paintings.filter(
            Q(title__icontains=search_query) |
            Q(artist__first_name__icontains=search_query) |
            Q(artist__last_name__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    
    # Сортировка
    sort_by = request.GET.get('sort', 'newest')
    if sort_by == 'likes':
        paintings = paintings.order_by('-likes_count', '-id')
    elif sort_by == 'oldest':
        paintings = paintings.order_by('year', 'id')
    elif sort_by == 'newest':
        paintings = paintings.order_by('-year', '-id')
    else:
        paintings = paintings.order_by('-id')
    
    # Добавляем информацию об избранном и лайках для авторизованных пользователей
    if request.user.is_authenticated and hasattr(request.user, 'profile'):
        favorite_ids = request.user.profile.favorite_paintings.values_list('id', flat=True)
        liked_ids = Painting.objects.filter(likes=request.user).values_list('id', flat=True)
        for painting in paintings:
            painting.is_favorited = painting.id in favorite_ids
            painting.is_liked = painting.id in liked_ids
    else:
        for painting in paintings:
            painting.is_favorited = False
            painting.is_liked = False
    
    # Пагинация
    from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
    paginator = Paginator(paintings, 12)  # 12 картин на странице
    page = request.GET.get('page')
    
    try:
        paintings = paginator.page(page)
    except PageNotAnInteger:
        paintings = paginator.page(1)
    except EmptyPage:
        paintings = paginator.page(paginator.num_pages)
    
    context = {
        'paintings': paintings,
        'painting_type': painting_type,
        'sort_by': sort_by,
    }
    return render(request, 'gallery/painting_list.html', context)

def painting_detail(request, pk):
    """Детальная страница картины"""
    painting = get_object_or_404(Painting, pk=pk)
    
    # Похожие картины
    similar_paintings = Painting.objects.filter(
        Q(genres__in=painting.genres.all()) |
        Q(artist=painting.artist)
    ).exclude(pk=pk).distinct()[:4]
    
    # Проверяем, лайкнул ли пользователь картину
    is_liked = painting.is_liked_by_user(request.user) if request.user.is_authenticated else False
    
    # Проверяем, в избранном ли у пользователя
    is_favorite = False
    if request.user.is_authenticated and hasattr(request.user, 'profile'):
        is_favorite = request.user.profile.is_in_favorites(painting)
    
    context = {
        'painting': painting,
        'similar_paintings': similar_paintings,
        'is_liked': is_liked,
        'is_favorite': is_favorite,
    }
    return render(request, 'gallery/painting_detail.html', context)

def artist_list(request):
    """Список художников"""
    artists = Artist.objects.all().order_by('last_name')
    
    # Добавляем информацию о подписках для авторизованных пользователей
    if request.user.is_authenticated:
        following_ids = request.user.profile.following_artists.values_list('id', flat=True)
        for artist in artists:
            artist.is_following = artist.id in following_ids
    else:
        for artist in artists:
            artist.is_following = False
    
    context = {'artists': artists}
    return render(request, 'gallery/artist_list.html', context)

def artist_detail(request, pk):
    """Детальная страница художника"""
    artist = get_object_or_404(Artist, pk=pk)
    
    # Работы художника
    paintings = artist.paintings.all()
    
    # Проверяем, подписан ли пользователь на художника
    is_following = False
    if request.user.is_authenticated and hasattr(request.user, 'profile'):
        is_following = request.user.profile.is_following(artist)
    
    context = {
        'artist': artist,
        'paintings': paintings,
        'is_following': is_following,
    }
    return render(request, 'gallery/artist_detail.html', context)

def genre_list(request):
    """Список всех жанров с количеством произведений в каждом"""
    # Аннотируем каждый жанр количеством связанных картин
    genres = Genre.objects.annotate(painting_count=Count('painting')).order_by('-painting_count', 'name')
    
    # Получаем общее количество произведений
    total_paintings = Painting.objects.count()
    
    # Получаем общее количество художников
    total_artists = Artist.objects.count()
    
    # Получаем количество жанров
    genres_count = genres.count()
    
    # Передаем данные в шаблон
    context = {
        'genres': genres,
        'genres_count': genres_count,
        'total_paintings': total_paintings or 0,
        'total_artists': total_artists or 0,
    }
    
    return render(request, 'gallery/genre_list.html', context)

def genre_detail(request, pk):
    """Детальная страница жанра"""
    genre = get_object_or_404(Genre, pk=pk)
    paintings = Painting.objects.filter(genres=genre)
    context = {
        'genre': genre,
        'paintings': paintings,
    }
    return render(request, 'gallery/genre_detail.html', context)

# ===== СИСТЕМА ПОЛЬЗОВАТЕЛЕЙ =====

def register(request):
    """Регистрация пользователя"""
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            # Автоматический вход после регистрации
            login(request, user)
            messages.success(request, f'Добро пожаловать, {user.username}! Регистрация прошла успешно.')
            return redirect('home')
    else:
        form = UserRegisterForm()
    
    return render(request, 'gallery/register.html', {'form': form})

def login_view(request):
    """Вход пользователя"""
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            
            if user is not None:
                login(request, user)
                messages.success(request, f'Добро пожаловать, {username}!')
                
                # Перенаправление на страницу, с которой пришел пользователь
                next_url = request.GET.get('next')
                if next_url:
                    return redirect(next_url)
                return redirect('home')
    else:
        form = AuthenticationForm()
    
    return render(request, 'gallery/login.html', {'form': form})

@login_required
def logout_view(request):
    """Выход пользователя"""
    logout(request)
    messages.info(request, 'Вы успешно вышли из системы.')
    return redirect('home')

@login_required
def profile(request):
    """Профиль пользователя"""
    user_profile = request.user.profile
    user_preferences = request.user.preferences
    
    # Получаем последние лайки пользователя
    liked_paintings = Painting.objects.filter(likes=request.user)[:6]
    
    # Получаем последние подписки
    following_artists = request.user.profile.following_artists.all()[:6]
    
    # Получаем избранные картины
    favorite_paintings = request.user.profile.favorite_paintings.all()[:6]
    
    context = {
        'profile': user_profile,
        'preferences': user_preferences,
        'liked_paintings': liked_paintings,
        'following_artists': following_artists,
        'favorite_paintings': favorite_paintings,
    }
    return render(request, 'gallery/profile.html', context)

# ===== ЛАЙКИ И ПОДПИСКИ =====

@require_POST
@login_required
def like_painting(request, painting_id):
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        try:
            painting = Painting.objects.get(id=painting_id)
            
            if request.user in painting.likes.all():
                painting.likes.remove(request.user)
                liked = False
            else:
                painting.likes.add(request.user)
                liked = True
            
            return JsonResponse({
                'success': True,
                'liked': liked,
                'likes_count': painting.likes.count()
            })
            
        except Painting.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Картина не найдена'})
    
    return JsonResponse({'success': False, 'error': 'Некорректный запрос'})

@require_POST
@login_required
def follow_artist(request, artist_id):
    """Подписаться/отписаться от художника"""
    artist = get_object_or_404(Artist, id=artist_id)
    profile = request.user.profile
    
    if profile.following_artists.filter(id=artist.id).exists():
        profile.unfollow_artist(artist)
        followed = False
    else:
        profile.follow_artist(artist)
        followed = True
        
        # Обновляем предпочтения пользователя
        if hasattr(request.user, 'preferences'):
            request.user.preferences.update_preferences()
    
    # Возвращаем JSON для AJAX запросов
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'followed': followed,
            'followers_count': artist.followers_count
        })
    
    messages.success(request, f'Вы {"подписались на" if followed else "отписались от"} художника {artist}!')
    return redirect(request.META.get('HTTP_REFERER', 'home'))

@require_POST
@login_required
def favorite_painting(request, painting_id):
    try:
        painting = Painting.objects.get(id=painting_id)
        
        # Проверяем, существует ли профиль, если нет - создаем
        profile, created = UserProfile.objects.get_or_create(user=request.user)
        
        # Проверяем текущее состояние
        is_currently_favorited = profile.is_in_favorites(painting)
        
        if is_currently_favorited:
            profile.remove_from_favorites(painting)
            favorited = False
        else:
            profile.add_to_favorites(painting)
            favorited = True
        
        # Проверяем, что изменение применилось
        is_now_favorited = profile.is_in_favorites(painting)
        
        return JsonResponse({
            'success': True,
            'favorited': favorited,
            'verified': is_now_favorited == favorited
        })
        
    except Painting.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Картина не найдена'}, status=404)
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        return JsonResponse({
            'success': False, 
            'error': str(e),
            'details': error_details
        }, status=500)

# ===== СТРАНИЦЫ ПОЛЬЗОВАТЕЛЯ =====

@login_required
def favorites(request):
    """Страница избранных картин пользователя"""
    favorite_paintings = request.user.profile.favorite_paintings.all().select_related('artist').prefetch_related('genres')
    
    # Пагинация
    from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
    paginator = Paginator(favorite_paintings, 12)
    page = request.GET.get('page')
    
    try:
        favorite_paintings = paginator.page(page)
    except PageNotAnInteger:
        favorite_paintings = paginator.page(1)
    except EmptyPage:
        favorite_paintings = paginator.page(paginator.num_pages)
    
    context = {'paintings': favorite_paintings}
    return render(request, 'gallery/favorites.html', context)

@login_required
def following(request):
    """Страница подписок пользователя"""
    following_artists = request.user.profile.following_artists.all()
    
    context = {'artists': following_artists}
    return render(request, 'gallery/following.html', context)

@login_required
def recommendations(request):
    """Страница рекомендаций"""
    if not hasattr(request.user, 'preferences'):
        messages.warning(request, 'Рекомендации будут доступны после оценки нескольких картин.')
        return redirect('painting_list')
    
    user_preferences = request.user.preferences
    
    # Получаем рекомендации
    recommended_paintings = user_preferences.get_recommended_paintings(limit=12)
    recommended_artists = user_preferences.get_recommended_artists(limit=6)
    
    # Популярные картины (если рекомендаций мало)
    if recommended_paintings.count() < 6:
        popular_paintings = Painting.objects.annotate(
            likes_count=Count('likes')
        ).order_by('-likes_count')[:12]
        
        # Объединяем рекомендации с популярными
        recommended_paintings = list(recommended_paintings) + list(popular_paintings[:12 - recommended_paintings.count()])
    
    context = {
        'recommended_paintings': recommended_paintings,
        'recommended_artists': recommended_artists,
    }
    return render(request, 'gallery/recommendations.html', context)

# ===== API =====

def painting_likes_api(request, painting_id):
    """API для получения информации о лайках картины"""
    painting = get_object_or_404(Painting, id=painting_id)
    
    is_liked = False
    if request.user.is_authenticated:
        is_liked = painting.is_liked_by_user(request.user)
    
    return JsonResponse({
        'likes_count': painting.like_count,
        'is_liked': is_liked,
    })

def artist_followers_api(request, artist_id):
    """API для получения информации о подписчиках художника"""
    artist = get_object_or_404(Artist, id=artist_id)
    
    is_following = False
    if request.user.is_authenticated and hasattr(request.user, 'profile'):
        is_following = request.user.profile.is_following(artist)
    
    return JsonResponse({
        'followers_count': artist.followers_count,
        'is_following': is_following,
    })

# ===== КНИГИ =====

def book_list(request):
    """Список всех книг"""
    books = Book.objects.all()
    
    # Поиск
    search_query = request.GET.get('search')
    if search_query:
        books = books.filter(
            Q(title__icontains=search_query) |
            Q(author__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    
    # Пагинация
    from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
    paginator = Paginator(books, 12)
    page = request.GET.get('page')
    
    try:
        books = paginator.page(page)
    except PageNotAnInteger:
        books = paginator.page(1)
    except EmptyPage:
        books = paginator.page(paginator.num_pages)
    
    context = {
        'books': books,
    }
    return render(request, 'gallery/book_list.html', context)

def book_detail(request, pk):
    """Детальная страница книги"""
    book = get_object_or_404(Book, pk=pk)
    
    # Похожие книги
    similar_books = Book.objects.exclude(pk=pk)[:4]
    
    context = {
        'book': book,
        'similar_books': similar_books,
    }
    return render(request, 'gallery/book_detail.html', context)