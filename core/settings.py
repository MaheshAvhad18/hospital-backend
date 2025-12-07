import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# ---------------------------------------------------------
# SECURITY SETTINGS
# ---------------------------------------------------------

# Load secret key from Render environment variable
SECRET_KEY = os.environ.get("SECRET_KEY", "development-secret-key")

# DEBUG should be False in production
DEBUG = os.environ.get("DEBUG", "True") == "True"

# Render automatically sets this environment variable "RENDER_EXTERNAL_HOSTNAME"
RENDER_HOSTNAME = os.environ.get("RENDER_EXTERNAL_HOSTNAME")

if RENDER_HOSTNAME:
    ALLOWED_HOSTS = [RENDER_HOSTNAME, ".onrender.com"]
else:
    ALLOWED_HOSTS =os.environ.get("ALLOWED_HOSTS", "*").split(",")  # local development


# ---------------------------------------------------------
# Application definition
# ---------------------------------------------------------

INSTALLED_APPS = [
    'admin_interface',
    'colorfield',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third-party
    'rest_framework',
    'corsheaders',

    # Local apps
    'api',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',

    # Whitenoise — serves static files in production
    'whitenoise.middleware.WhiteNoiseMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',

    # CORS middleware (must be above CommonMiddleware)
    "corsheaders.middleware.CorsMiddleware",

    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

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

WSGI_APPLICATION = 'core.wsgi.application'


# ---------------------------------------------------------
# DATABASE CONFIG (SQLite for now)
# ---------------------------------------------------------

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# ---------------------------------------------------------
# Password validation
# ---------------------------------------------------------

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


# ---------------------------------------------------------
# Internationalization
# ---------------------------------------------------------

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata'  # better for India
USE_I18N = True
USE_TZ = True


# ---------------------------------------------------------
# Static files (CSS, JavaScript, Images)
# ---------------------------------------------------------

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = []
# Whitenoise static optimization
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


# ---------------------------------------------------------
# CORS Settings
# ---------------------------------------------------------

CORS_ALLOW_ALL_ORIGINS = True
# (Later, change to your Vercel domain)


# ---------------------------------------------------------
# Default primary key field type
# ---------------------------------------------------------

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
