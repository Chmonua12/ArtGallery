# gallery/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # Основные страницы
    path('', views.home, name='home'),
    path('paintings/', views.painting_list, name='painting_list'),
    path('painting/<int:pk>/', views.painting_detail, name='painting_detail'),
    path('artists/', views.artist_list, name='artist_list'),
    path('artist/<int:pk>/', views.artist_detail, name='artist_detail'),
    path('genres/', views.genre_list, name='genre_list'),
    path('genre/<int:pk>/', views.genre_detail, name='genre_detail'),
    
    # Система пользователей
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile, name='profile'),
    
    # Взаимодействия
    path('painting/<int:painting_id>/like/', views.like_painting, name='like_painting'),
    path('artist/<int:artist_id>/follow/', views.follow_artist, name='follow_artist'),
    path('painting/<int:painting_id>/favorite/', views.favorite_painting, name='favorite_painting'),
    
    # Страницы пользователя
    path('favorites/', views.favorites, name='favorites'),
    path('following/', views.following, name='following'),
    path('recommendations/', views.recommendations, name='recommendations'),
    
    # API
    path('api/paintings/<int:painting_id>/like/', views.like_painting, name='like_painting'),
    path('api/paintings/<int:painting_id>/favorite/', views.favorite_painting, name='favorite_painting'),
    
    # Книги
    path('books/', views.book_list, name='book_list'),
    path('book/<int:pk>/', views.book_detail, name='book_detail'),
]