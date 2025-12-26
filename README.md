# ArtVerse - Цифровая галерея искусства
# Подготовила Солодовникова Милена К0709-23/3

ArtVerse - это веб-приложение для цифровой галереи искусства, созданное на Django. Платформа позволяет пользователям просматривать коллекции картин, изучать информацию о художниках, добавлять произведения в избранное, лайкать картины и читать книги для улучшения своего скилла.

## Основные возможности:

- **Галерея картин**: Просмотр коллекции картин с фильтрацией по типу искусства
- **Художники**: Информация о художниках с биографией, портретами, аватарами и социальными сетями
- **Жанры**: Категоризация картин по жанрам
- **Система лайков**: Возможность лайкать понравившиеся картины
- **Избранное**: Сохранение любимых картин в личную коллекцию
- **Подписки**: Подписка на любимых художников
- **Книги по рисованию**: Раздел с книгами в формате PDF и обложками
- **Сортировка**: Сортировка картин по дате создания и количеству лайков
- **Профиль пользователя**: Личный профиль с избранными картинами и подписками

## Технологии:

- **Backend**: Django 4.x
- **Frontend**: HTML, CSS, JavaScript
- **База данных**: SQLite (для разработки)
- **Медиа**: Pillow для работы с изображениями

## Требования:

- Python 3.8+
- Django 4.x
- Pillow

## Установка и запуск

### 1. Клонирование репозитория

```bash
git clone https://github.com/yourusername/art_g.git
cd art_g
git checkout art
```

### 2. Создание виртуального окружения

```bash
python -m venv venv
source venv/bin/activate  # Для Linux/Mac
# или
venv\Scripts\activate  # Для Windows
```

### 3. Установка зависимостей

```bash
pip install -r requirements.txt
```

Если файл requirements.txt отсутствует, установите зависимости вручную:

```bash
pip install django pillow
```

### 4. Настройка базы данных

```bash
python manage.py migrate
```

### 5. Создание суперпользователя 

```bash
python manage.py createsuperuser
```

### 6. Запуск сервера

```bash
python manage.py runserver
```

Lоступно по адресу: `http://127.0.0.1:8000/`

## Структура проекта

```
art/
├── art_gallery/          # Основные настройки Django проекта
│   ├── settings.py       # Настройки приложения
│   ├── urls.py          # Главный файл маршрутизации
│   └── wsgi.py          # WSGI конфигурация
├── gallery/             # Основное приложение
│   ├── models.py        # Модели данных
│   ├── views.py         # Представления (views)
│   ├── urls.py          # Маршруты приложения
│   ├── admin.py         # Административная панель
│   ├── forms.py         # Формы
│   └── migrations/      # Миграции базы данных
├── templates/           # HTML шаблоны
│   ├── base.html        # Базовый шаблон
│   └── gallery/         # Шаблоны галереи
├── static/              # Статические файлы (CSS, JS)
│   └── js/              # JavaScript файлы
├── media/               # Загруженные файлы (изображения, PDF)
│   ├── artists/         # Изображения художников
│   ├── paintings/       # Изображения картин
│   └── books/           # Книги (PDF и обложки)
├── manage.py            # Управляющий скрипт Django
├── requirements.txt     # Зависимости проекта
└── db.sqlite3           # База данных SQLite
```

## ER-диаграмма базы данных

```
┌─────────────┐
│    User     │
│ (Django)    │
└──────┬──────┘
       │
       │ 1:1
       ├─────────────────┐
       │                 │
       │                 │
┌──────▼──────┐   ┌──────▼──────────┐
│ UserProfile │   │ Artist          │
├─────────────┤   ├─────────────────┤
│ bio         │   │ first_name      │
│ avatar      │   │ last_name       │
│             │   │ biography       │
│             │   │ country         │
│             │   │ portrait        │
│             │   │ avatar          │
│             │   │ has_social_networks│
│             │   │ instagram       │
│             │   │ artstation      │
└──────┬──────┘   └────────┬────────┘
       │                    │
       │ M:M                │ 1:N
       │                    │
       │            ┌───────▼────────┐
       │            │   Painting    │
       │            ├───────────────┤
       │            │ title         │
       │            │ year          │
       │            │ technique     │
       │            │ image         │
       │            │ description   │
       │            │ art_type      │
       │            └───────┬───────┘
       │                    │
       │                    │ M:M
       │                    │
       │            ┌───────▼────────┐
       │            │    Genre       │
       │            ├───────────────┤
       │            │ name          │
       │            │ description   │
       │            └───────────────┘
       │
       │ 1:1
       │
┌──────▼──────────┐
│ UserPreference  │
├─────────────────┤
│ favorite_genres │ (M:M)
│ favorite_artists│ (M:M)
└─────────────────┘

┌─────────────┐
│    Book     │
├─────────────┤
│ title       │
│ author      │
│ description │
│ cover       │
│ pdf_file    │
└─────────────┘
```

### Описание связей:

- **User ↔ UserProfile**: Один к одному (OneToOne)
- **User ↔ Artist**: Один к одному (OneToOne, опционально)
- **Artist ↔ Painting**: Один ко многим (ForeignKey)
- **Painting ↔ Genre**: Многие ко многим (ManyToMany)
- **User ↔ Painting (likes)**: Многие ко многим (ManyToMany)
- **UserProfile ↔ Painting (favorites)**: Многие ко многим (ManyToMany)
- **UserProfile ↔ Artist (following)**: Многие ко многим (ManyToMany)
- **UserPreference ↔ Genre**: Многие ко многим (ManyToMany)
- **UserPreference ↔ Artist**: Многие ко многим (ManyToMany)

## API Endpoints

### Основные маршруты

| Метод | URL | Описание |
|-------|-----|----------|
| GET | `/` | Главная страница |
| GET | `/paintings/` | Список всех картин |
| GET | `/painting/<id>/` | Детальная страница картины |
| GET | `/artists/` | Список художников |
| GET | `/artist/<id>/` | Детальная страница художника |
| GET | `/genres/` | Список жанров |
| GET | `/genre/<id>/` | Детальная страница жанра |
| GET | `/books/` | Список книг |
| GET | `/book/<id>/` | Детальная страница книги |

### Пользовательские маршруты

| Метод | URL | Описание |
|-------|-----|----------|
| GET | `/register/` | Регистрация |
| GET/POST | `/login/` | Вход |
| POST | `/logout/` | Выход |
| GET | `/profile/` | Профиль пользователя |
| GET | `/favorites/` | Избранные картины |
| GET | `/following/` | Подписки на художников |
| GET | `/recommendations/` | Рекомендации |

### API для взаимодействий 

| Метод | URL | Описание | Параметры |
|-------|-----|----------|-----------|
| POST | `/api/paintings/<id>/like/` | Лайк/дизлайк картины | - |
| POST | `/api/paintings/<id>/favorite/` | Добавить/удалить из избранного | - |
| POST | `/artist/<id>/follow/` | Подписаться/отписаться от художника | - |

### Примеры API запросов

#### Лайк картины

```javascript
fetch('/api/paintings/1/like/', {
    method: 'POST',
    headers: {
        'X-CSRFToken': getCookie('csrftoken'),
        'Content-Type': 'application/json',
        'X-Requested-With': 'XMLHttpRequest'
    }
})
.then(response => response.json())
.then(data => {
    console.log(data);
    // {success: true, liked: true, likes_count: 5}
});
```

#### Добавление в избранное

```javascript
fetch('/api/paintings/1/favorite/', {
    method: 'POST',
    headers: {
        'X-CSRFToken': getCookie('csrftoken'),
        'Content-Type': 'application/json',
        'X-Requested-With': 'XMLHttpRequest'
    }
})
.then(response => response.json())
.then(data => {
    console.log(data);
    // {success: true, favorited: true}
});
```

## Основные разделы (скрины)

### Главная страница
<img width="1374" height="895" alt="Снимок экрана от 2025-12-26 12-18-28" src="https://github.com/user-attachments/assets/83854b05-1cae-42e1-add8-4d54d926a407" />

*Главная страница с коллекцией картин*

### Галерея картин
<img width="1904" height="902" alt="Снимок экрана от 2025-12-26 10-37-59" src="https://github.com/user-attachments/assets/9fbee7dc-60c9-4ff0-90d1-4b34b7d93fe8" />

*Список картин с возможностью сортировки и фильтрации*


### Управление профилем
<img width="247" height="373" alt="Снимок экрана от 2025-12-26 10-41-58" src="https://github.com/user-attachments/assets/bbe187dd-d373-4908-a60e-8808033be7e8" />


### Раздел книг
<img width="1388" height="860" alt="Снимок экрана от 2025-12-26 10-38-53" src="https://github.com/user-attachments/assets/f7177e9b-2bc5-4be3-9ff5-0397f0124252" />

*Коллекция книг по рисованию с возможностью просмотра PDF*

