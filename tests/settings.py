import os
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve(strict=True).parent.parent
sys.path.append(str(BASE_DIR / "tests"))

SECRET_KEY = "=bodvqgkt@)emfe2!($i#1zd(x27@u!9*9+)^$8bu#sqsmm^*n"

DEBUG = True

ALLOWED_HOSTS = ["*"]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "literature",
    "example",
    "formset",
    "neapolitan",
    "sortedm2m",
    "crispy_forms",
    "crispy_bootstrap5",
    "adminsortable2",
    "django_select2",
    "django_jsonform",
    "django_json_widget",
    "admin_extra_buttons",
    "django_tables2",
    "django_extensions",
    "easy_icons",
    "flex_menu",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.middleware.common.CommonMiddleware",
]

ROOT_URLCONF = "tests.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            os.path.join(BASE_DIR, "templates"),
        ],
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

WSGI_APPLICATION = "tests.wsgi.application"

# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
    }
}

AUTH_PASSWORD_VALIDATORS = []

STATIC_URL = "/static/"

CORS_ALLOW_ALL_ORIGINS = True

# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/
STATIC_ROOT = "static"
STATIC_URL = "/static/"

MEDIA_ROOT = "media"
MEDIA_URL = "/media/"

X_FRAME_OPTIONS = "SAMEORIGIN"

# CACHES = {
#     "default": {
#         "BACKEND": "django.core.cache.backends.dummy.DummyCache",
#     }
# }

# STATIC_URL = '/static/'
# STATIC_ROOT = 'dist/static/'
STATICFILES_DIRS = (
    # os.path.join(BASE_DIR, 'static'),
    # This defines a prefix so the url paths will become `/static/node_modules/...`
    ("node_modules", os.path.join(BASE_DIR, "node_modules/")),
)


CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"

CRISPY_TEMPLATE_PACK = "bootstrap5"

DJANGO_TABLES2_TABLE_ATTRS = {
    "class": "table table-hover table-striped",
    # "thead": {
    #     "class": "table-light",
    # },
}

DJANGO_TABLES2_TEMPLATE = "django_tables2/bootstrap5-responsive.html"

DATA_UPLOAD_MAX_MEMORY_SIZE = 5242880  # 5 MB
