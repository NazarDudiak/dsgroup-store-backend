from pathlib import Path
from decouple import config, Csv

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = config('SECRET_KEY', default='unsafe-development-key')
DEBUG = config('DEBUG', default=False, cast=bool)
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost,127.0.0.1', cast=Csv())
DATABASE_URL = config('DATABASE_URL', default=f'sqlite:///{BASE_DIR / "db.sqlite3"}')

INSTALLED_APPS = [
    'unfold', 'django.contrib.admin', 'django.contrib.auth', 'django.contrib.contenttypes',
    'django.contrib.sessions', 'django.contrib.messages', 'django.contrib.staticfiles',
    'corsheaders', 'rest_framework', 'catalog',
]
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware', 'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware', 'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware', 'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware', 'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
ROOT_URLCONF = 'config.urls'
TEMPLATES = [{'BACKEND': 'django.template.backends.django.DjangoTemplates', 'DIRS': [], 'APP_DIRS': True,
              'OPTIONS': {'context_processors': ['django.template.context_processors.request', 'django.contrib.auth.context_processors.auth', 'django.contrib.messages.context_processors.messages']}}]
WSGI_APPLICATION = 'config.wsgi.application'
if DATABASE_URL.startswith('sqlite'):
    DATABASES = {'default': {'ENGINE': 'django.db.backends.sqlite3', 'NAME': DATABASE_URL.replace('sqlite:///', '')}}
else:
    import dj_database_url
    DATABASES = {'default': dj_database_url.parse(DATABASE_URL)}
LANGUAGE_CODE, TIME_ZONE, USE_TZ = 'uk', 'Europe/Kyiv', True
STATIC_URL, STATIC_ROOT = '/static/', BASE_DIR / 'staticfiles'
MEDIA_URL, MEDIA_ROOT = '/media/', BASE_DIR / 'media'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
REST_FRAMEWORK = {'DEFAULT_PERMISSION_CLASSES': ['rest_framework.permissions.AllowAny']}
CORS_ALLOWED_ORIGINS = config('CORS_ALLOWED_ORIGINS', default='http://localhost:3000', cast=Csv())
STORE_URL = config('STORE_URL', default='http://localhost:3000')
UNFOLD = {'SITE_TITLE': 'Store Admin', 'SITE_HEADER': 'Store', 'SITE_SYMBOL': 'storefront', 'THEME': 'light'}
