from django.contrib import admin
from .models import Artist, Painting, Genre, Book

class ArtistAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'country', 'has_social_networks', 'has_avatar']
    search_fields = ['first_name', 'last_name', 'country']
    list_filter = ['has_social_networks', 'country']
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('first_name', 'last_name', 'country', 'biography')
        }),
        ('Даты', {
            'fields': ('birth_date', 'death_date'),
            'classes': ('collapse',)
        }),
        ('Изображения', {
            'fields': ('portrait', 'avatar'),
            'description': 'Портрет используется как основной, аватар - как дополнительное изображение'
        }),
        ('Социальные сети', {
            'fields': ('has_social_networks', 'instagram', 'artstation'),
            'description': 'Отметьте "Есть социальные сети" и укажите ссылки на профили'
        }),
        ('Пользователь', {
            'fields': ('user',),
            'classes': ('collapse',)
        }),
    )
    
    def has_avatar(self, obj):
        """Проверяет наличие аватара или портрета"""
        return bool(obj.get_avatar)
    has_avatar.boolean = True
    has_avatar.short_description = 'Есть изображение'

class PaintingAdmin(admin.ModelAdmin):
    list_display = ['title', 'artist', 'year']
    search_fields = ['title', 'artist__first_name']

class GenreAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']

class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'created_at']
    search_fields = ['title', 'author']
    list_filter = ['created_at']

# Регистрируем модели
admin.site.register(Artist, ArtistAdmin)
admin.site.register(Painting, PaintingAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Book, BookAdmin)