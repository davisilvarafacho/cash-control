import os
from pathlib import Path
from datetime import timedelta

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY")

DEBUG = os.environ.get("DJANGO_DEBUG") == "True"

MODE = os.environ.get("DJANGO_MODE")

DEV = MODE == "development"

PROD = MODE == "production"

ALLOWED_HOSTS = [
    "127.0.0.1",
    "localhost",
]

CSRF_TRUSTED_ORIGINS = []


DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

LIBS_APPS = [
    # rest framework and his extensions
    "rest_framework",
    "corsheaders",
    "django_filters",
    # unfold packages
    "unfold",
    "unfold.contrib.import_export",
    # unfold dependencies
    "import_export",
]

LOGIX_APPS = [
    "apps.system.base",
    "apps.system.core",
    "apps.system.conf",
    "apps.users",
    "apps.financeiro",
]

INSTALLED_APPS = LIBS_APPS + DJANGO_APPS + LOGIX_APPS


DJANGO_MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

LIBS_MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
]

LOGIX_MIDDLEWARE = []

if DEBUG:
    LOGIX_MIDDLEWARE.append("apps.system.core.middlewares.DevMiddleware")

MIDDLEWARE = DJANGO_MIDDLEWARE + LIBS_MIDDLEWARE + LOGIX_MIDDLEWARE


ROOT_URLCONF = "api.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "api.wsgi.application"


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    },
}


AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


AUTH_USER_MODEL = "users.Usuario"


DATE_FORMAT = "d/m/Y"

LANGUAGE_CODE = "pt-br"

TIME_ZONE = "America/Sao_Paulo"

USE_I18N = True

USE_TZ = True


STATIC_ROOT = BASE_DIR / "staticfiles"

STATIC_URL = "static/"


MEDIA_ROOT = BASE_DIR / "media"

MEDIA_URL = "media/"


EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

EMAIL_USE_TLS = True

EMAIL_HOST = "smtp.hostinger.com"

EMAIL_HOST_USER = "no-reply@sistemas-rafacho.tech"

EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_PASSWORD")

EMAIL_PORT = 587


DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


CORS_ALLOW_ALL_ORIGINS = True


UNFOLD = {
    "ENVIRONMENT": "apps.system.conf.enviroments.enviroment_callback",
    "SITE_SYMBOL": "money",
    "SHOW_VIEW_ON_SITE": False,
}


REST_FRAMEWORK = {
    "PAGE_SIZE": 12,
    "DEFAULT_PAGINATION_CLASS": "apps.system.core.pagination.CustomPagination",
    "DEFAULT_FILTER_BACKENDS": [
        "rest_framework.filters.SearchFilter",
        "rest_framework.filters.OrderingFilter",
        "django_filters.rest_framework.DjangoFilterBackend",
    ],
}


SIMPLE_JWT = {
    "AUTH_HEADER_TYPES": ("Bearer", "JWT"),
    "ACCESS_TOKEN_LIFETIME": timedelta(days=90 if DEBUG else 1),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=120 if DEBUG else 3),
    "TOKEN_OBTAIN_SERIALIZER": "apps.users.serializers.CustomTokenObtainPairSerializer",
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "sub",
    "AUDIENCE": "ZETTABYTE MIDAS v0.0.1",
    "ISSUER": "ZETTABYTE MIDAS v0.0.1",
}
