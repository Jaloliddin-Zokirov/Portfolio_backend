import environ
from pathlib import Path
from datetime import timedelta
from decouple import config
import cloudinary.api

BASE_DIR = Path(__file__).resolve().parent.parent
env = environ.Env()
environ.Env.read_env(env_file=BASE_DIR / ".env")

SECRET_KEY = env.str("SECRET_KEY", default="django-insecure-)uv2xyqk&vk$%67=k)yaf9q-+#!bc3mt#6h(bojwsg+=!3x^oy")

DEBUG = env.bool("DEBUG", default=True)

def _clean_host(value: str) -> str:
    """Return a host name without protocol prefixes or trailing paths."""

    value = value.strip()
    if not value:
        return ""

    if value.startswith(("http://", "https://")):
        value = value.split("://", 1)[1]

    # Remove any trailing path fragments if present (e.g. example.com/foo).
    value = value.split("/", 1)[0]
    return value


def _normalise_hosts(values: list[str]) -> list[str]:
    seen: set[str] = set()
    normalised: list[str] = []

    for value in values:
        host = _clean_host(value)
        if host and host not in seen:
            seen.add(host)
            normalised.append(host)

    return normalised


raw_allowed_hosts = [
    "localhost",
    "127.0.0.1",
    "jaloliddindev.uz",
    "www.jaloliddindev.uz",
    "api.jaloliddindev.uz",
    "www.api.jaloliddindev.uz",
]

if "*" in raw_allowed_hosts:
    ALLOWED_HOSTS = [
        "localhost",
        "127.0.0.1",
        "jaloliddindev.uz",
        "www.jaloliddindev.uz",
        "api.jaloliddindev.uz",
        "www.api.jaloliddindev.uz",
    ]
    
else:
    ALLOWED_HOSTS = _normalise_hosts(raw_allowed_hosts)

raw_csrf_trusted_origins = env.list(
    "CSRF_TRUSTED_ORIGINS",
    default=["https://api.jaloliddindev.uz"],
)

CSRF_TRUSTED_ORIGINS = raw_csrf_trusted_origins

if "*" not in ALLOWED_HOSTS:
    for origin_host in _normalise_hosts(raw_csrf_trusted_origins):
        if origin_host not in ALLOWED_HOSTS:
            ALLOWED_HOSTS.append(origin_host)

raw_cors_allowed_origins = env.list(
    "CORS_ALLOWED_ORIGINS",
    default=[
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:8000",
        "https://jaloliddindev.uz",
        "https://www.jaloliddindev.uz",
        "https://api.jaloliddindev.uz",
        "https://www.api.jaloliddindev.uz",
    ],
)

if "*" in raw_cors_allowed_origins:
    CORS_ALLOW_ALL_ORIGINS = True
    CORS_ALLOWED_ORIGINS: list[str] = []
else:
    CORS_ALLOW_ALL_ORIGINS = False
    CORS_ALLOWED_ORIGINS = raw_cors_allowed_origins

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'cloudinary',
    'cloudinary_storage',

    'corsheaders',
    'main',
    'rest_framework',
    'drf_yasg',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'portfolio.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'portfolio.wsgi.application'

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
}

# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": env.str("POSTGRES_DB", default="portfolio"),
        "USER": env.str("POSTGRES_USER", default="postgres"),
        "PASSWORD": env.str("POSTGRES_PASSWORD", default="postgres"),
        "HOST": env.str("POSTGRES_HOST", default="localhost"),
        "PORT": env.str("POSTGRES_PORT", default="5432"),
        'ATOMIC_REQUESTS': True,
        "OPTIONS": {
            "sslmode": "require",
        },
    }
}

# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = "Asia/Tashkent"

USE_I18N = True

USE_TZ = True


STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

STATIC_ROOT = BASE_DIR / 'staticfiles'
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

CLOUDINARY_STORAGE = {
    "CLOUD_NAME": config("CLOUDINARY_CLOUD_NAME"),
    "API_KEY": config("CLOUDINARY_API_KEY"),
    "API_SECRET": config("CLOUDINARY_API_SECRET"),
}

cloudinary.config(
    cloud_name=CLOUDINARY_STORAGE["CLOUD_NAME"],
    api_key=CLOUDINARY_STORAGE["API_KEY"],
    api_secret=CLOUDINARY_STORAGE["API_SECRET"]
)

DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
USE_X_FORWARDED_HOST = True