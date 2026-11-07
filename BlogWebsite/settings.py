from pathlib import Path
import os
import dj_database_url
from dotenv import load_dotenv
from django.core.exceptions import ImproperlyConfigured

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent


# Render's Blueprint uses DJANGO_SECRET_KEY. Keep SECRET_KEY as a
# backwards-compatible fallback for existing local environments.
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY') or os.environ.get('SECRET_KEY')

DEBUG = os.environ.get('DEBUG', 'False').strip().lower() in {'1', 'true', 'yes', 'on'}

if not SECRET_KEY:
    if DEBUG:
        raise ImproperlyConfigured(
            "Set SECRET_KEY (or DJANGO_SECRET_KEY) in your local environment."
        )
    raise ImproperlyConfigured(
        "DJANGO_SECRET_KEY must be configured in production."
    )

# Do not use a wildcard host in production. Add custom domains through the
# ALLOWED_HOSTS environment variable as a comma-separated list.
ALLOWED_HOSTS = ['localhost', '127.0.0.1', '.onrender.com']
ALLOWED_HOSTS.extend(
    host.strip()
    for host in os.environ.get('ALLOWED_HOSTS', '').split(',')
    if host.strip()
)

CSRF_TRUSTED_ORIGINS = [
    origin.strip()
    for origin in os.environ.get('CSRF_TRUSTED_ORIGINS', '').split(',')
    if origin.strip()
]


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',

    'portfolio',

    'django.contrib.staticfiles',
    
    'cloudinary_storage',
    'cloudinary',

    'import_export',
]


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',

    'django.middleware.csrf.CsrfViewMiddleware',

    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',

    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


# Render terminates HTTPS at its proxy. Trust the forwarded protocol so Django
# can enforce HTTPS without creating redirect loops.
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = not DEBUG
SESSION_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_SECURE = not DEBUG
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_REFERRER_POLICY = 'strict-origin-when-cross-origin'
X_FRAME_OPTIONS = 'DENY'

if not DEBUG:
    SECURE_HSTS_SECONDS = 31536000
    # Avoid imposing HSTS on unrelated subdomains or preload lists.
    SECURE_HSTS_INCLUDE_SUBDOMAINS = False
    SECURE_HSTS_PRELOAD = False


ROOT_URLCONF = 'BlogWebsite.urls'


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],

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


WSGI_APPLICATION = 'BlogWebsite.wsgi.application'


# Database

DATABASE_URL = os.environ.get("DATABASE_URL", "").strip()


if DATABASE_URL and DATABASE_URL.startswith((
    "postgres://",
    "postgresql://",
    "mysql://",
    "sqlite://"
)):

    DATABASES = {
        "default": dj_database_url.parse(
            DATABASE_URL,
            conn_max_age=600
        )
    }

else:

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }



AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME':
        'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'
    },
    {
        'NAME':
        'django.contrib.auth.password_validation.MinimumLengthValidator'
    },
    {
        'NAME':
        'django.contrib.auth.password_validation.CommonPasswordValidator'
    },
    {
        'NAME':
        'django.contrib.auth.password_validation.NumericPasswordValidator'
    },
]


LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True



# Static files

STATIC_URL = '/static/'

STATIC_ROOT = BASE_DIR / 'staticfiles'




# Cloudinary config

CLOUDINARY_STORAGE = {

    'CLOUD_NAME':
        os.environ.get('CLOUDINARY_CLOUD_NAME'),

    'API_KEY':
        os.environ.get('CLOUDINARY_API_KEY'),

    'API_SECRET':
        os.environ.get('CLOUDINARY_API_SECRET'),
}



# Django 6 storage configuration
# Static files
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

STATICFILES_STORAGE = (
    "whitenoise.storage.CompressedStaticFilesStorage"
)


# Media files
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"


# Cloudinary only for media uploads
STORAGES = {

    "default": {
        "BACKEND": "cloudinary_storage.storage.MediaCloudinaryStorage",
    },

    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedStaticFilesStorage",
    },

}


MEDIA_URL = '/media/'

MEDIA_ROOT = BASE_DIR / 'media'


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'