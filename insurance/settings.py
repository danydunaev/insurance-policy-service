"""
Настройки Django-проекта «Сервис учёта страховых полисов».
ПР6: добавлен каталог шаблонов уровня проекта templates/.
"""

# ============================================================
# ВОПРОС ТАБЛИЦЫ №1: Структура проекта Django
# settings.py — конфигурация проекта: приложения, шаблоны,
# статика, middleware, БД, язык, часовой пояс.
# ============================================================

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-change-me-in-production'

# ============================================================
# ВОПРОС ТАБЛИЦЫ №5: Настройки режима отладки
# DEBUG=True — подробные ошибки, автоотдача статики,
#              ALLOWED_HOSTS не проверяется.
# Перед выключением: DEBUG=False, заполнить ALLOWED_HOSTS,
# настроить отдачу статики вне Django.
# ============================================================
DEBUG = True
ALLOWED_HOSTS = []

# ============================================================
# ВОПРОС ТАБЛИЦЫ №3: Регистрация приложений
# Если приложение не в INSTALLED_APPS — не найдутся его
# шаблоны (app/templates/) и статика; миграции не применятся.
# ============================================================
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # ========================================================
    # ВОПРОС ТАБЛИЦЫ №4: Структура приложений
    # homepage — главная страница;
    # web_users — список пользователей;
    # web_policies — список и карточка полисов.
    # Отдельное приложение для users не создаётся, потому что
    # нет отдельных страниц пользователя (только список).
    # ========================================================
    'homepage',
    'web_users',
    'web_policies',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'insurance.urls'

# ============================================================
# ШАБЛОНЫ: DIRS указывает на каталог templates/ в корне —
# именно там лежат base.html и includes/navigation.html.
# ============================================================
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'insurance.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'ru-ru'
TIME_ZONE = 'Europe/Moscow'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'homepage' / 'static']

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'