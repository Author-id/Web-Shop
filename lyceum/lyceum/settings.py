import os
from pathlib import Path

from django.utils.translation import gettext_lazy as _
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv("../.env-example")
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", default="NORMALNO-SREM")

COUNT = 0

DEBUG_ENV = os.getenv("DJANGO_DEBUG", default="false").lower()
DEBUG = DEBUG_ENV in ("true", "yes", "1", "y", "t")

ALLOWED_HOSTS_STRING = os.environ.get("DJANGO_ALLOWED_HOSTS", "*")
ALLOWED_HOSTS = list(map(str.strip, ALLOWED_HOSTS_STRING.split(",")))
ALLOW_REVERSE = os.environ.get(
    "DJANGO_ALLOW_REVERSE",
    default="true",
).lower() in (
    "true",
    "yes",
    "1",
    "y",
    "t",
)

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "homepage.apps.HomepageConfig",
    "catalog.apps.CatalogConfig",
    "about.apps.AboutConfig",
    "core.apps.CoreConfig",
    "django_cleanup.apps.CleanupConfig",
    "sorl.thumbnail",
    "tinymce",
]

if DEBUG:
    INSTALLED_APPS.append("debug_toolbar")

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.locale.LocaleMiddleware",
]

if DEBUG:
    MIDDLEWARE.append("debug_toolbar.middleware.DebugToolbarMiddleware")

if ALLOW_REVERSE:
    MIDDLEWARE.append("lyceum.middleware.ReverseRussianWordsMiddleware")

INTERNAL_IPS = ["127.0.0.1"]

ROOT_URLCONF = "lyceum.urls"

LANGUAGE_CODE = "ru"

USE_I18N = True

LANGUAGES = [
    ("ru", _("Russian")),
    ("en", _("English")),
]

LOCALE_PATHS = [
    BASE_DIR / "locale",
]

STATIC_URL = "/static/"

STATICFILES_DIRS = [
    BASE_DIR / "static_dev",
]

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
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

WSGI_APPLICATION = "lyceum.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    },
}

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "UserAttributeSimilarityValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation.MinimumLengthValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "CommonPasswordValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "NumericPasswordValidator"
        ),
    },
]

TIME_ZONE = "UTC"

USE_TZ = True

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
