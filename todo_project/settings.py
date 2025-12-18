"""
Django settings for todo_project project.
"""

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-^pi7+&47e-*tm*#8!#1vhn-xb*q121+uel8ih(4g8b+*p1mbga'

DEBUG = True

ALLOWED_HOSTS = []


# ------------------ Installed Apps ------------------
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Your App
    'todo',
]


# ------------------ Middleware ------------------
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


# ------------------ URL Config ------------------
ROOT_URLCONF = 'todo_project.urls'


# ------------------ Templates Settings ------------------
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',

        # ⭐ ADDED — to load templates folder
        'DIRS': [BASE_DIR / 'templates'],

        'APP_DIRS': True,

        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'todo_project.wsgi.application'


# ------------------ Database ------------------
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# ------------------ Password Validators ------------------
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# ------------------ Internationalization ------------------
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# ------------------ Static Files ------------------
STATIC_URL = 'static/'

STATICFILES_DIRS = [
    BASE_DIR / "static"
]


# ------------------ Primary Key ------------------
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# ------------------ Authentication Redirects ------------------

# ⭐ FIXED — without this it gives NoReverseMatch: 'login'
LOGIN_URL = 'login'

# After login redirect to dashboard/home
LOGIN_REDIRECT_URL = '/'

# Logout redirect
LOGOUT_REDIRECT_URL = 'login'
