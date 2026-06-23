"""
Django settings for the "Mots sur Maux" project.

Mots sur Maux est un projet artistique, thérapeutique, éducatif et social qui
vise à favoriser le mieux-être psychologique et l'expression de soi à travers
l'écriture.

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.2/ref/settings/
"""

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


def env_bool(name, default=False):
    """Read a boolean from the environment ("1/true/yes/on")."""
    value = os.environ.get(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get(
    "DJANGO_SECRET_KEY",
    "django-insecure-#0+wz^)vn^pk#0)1evn#3(ypk^c&%lw@fx%lu29ln-ljrr1(@g",
)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env_bool("DJANGO_DEBUG", default=True)

ALLOWED_HOSTS = os.environ.get(
    "DJANGO_ALLOWED_HOSTS", "localhost,127.0.0.1,0.0.0.0"
).split(",")

CSRF_TRUSTED_ORIGINS = [
    origin
    for origin in os.environ.get("DJANGO_CSRF_TRUSTED_ORIGINS", "").split(",")
    if origin
]

# Common free hosting domains are allowed by default, so deploying needs no
# extra host configuration (works on PythonAnywhere and Render out of the box).
ALLOWED_HOSTS += [".pythonanywhere.com", ".onrender.com"]
CSRF_TRUSTED_ORIGINS += [
    "https://*.pythonanywhere.com",
    "https://*.onrender.com",
]

# Convenience: when developing locally (DEBUG on), allow sharing the dev server
# through an ngrok tunnel without any extra configuration. Any ngrok subdomain
# is accepted for both host and CSRF checks. This block does nothing in
# production (DEBUG off), so it stays safe.
if DEBUG:
    ALLOWED_HOSTS += [".ngrok-free.dev", ".ngrok-free.app", ".ngrok.io"]
    CSRF_TRUSTED_ORIGINS += [
        "https://*.ngrok-free.dev",
        "https://*.ngrok-free.app",
        "https://*.ngrok.io",
    ]


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Mots sur Maux apps
    "core",
    "blog",
    "submissions",
    "workshops",
    "resources",
    "accounts",
    "team",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# WhiteNoise lets the app serve its own static files in production.
# Added only if installed, so local dev works without it.
try:
    import whitenoise  # noqa: F401

    MIDDLEWARE.insert(1, "whitenoise.middleware.WhiteNoiseMiddleware")
except ImportError:
    pass

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "core.context_processors.site_context",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

# Authentication.
# Members sign in at /compte/ ; the team has its own login at /equipe/ which
# overrides the redirect to its own dashboard.
LOGIN_URL = "accounts:login"
LOGIN_REDIRECT_URL = "accounts:dashboard"
LOGOUT_REDIRECT_URL = "core:home"

# Email — used for password reset. In development (no SMTP configured), emails
# are printed to the terminal so the reset link is easy to copy. In production,
# set the DJANGO_EMAIL_* variables to send real messages.
DEFAULT_FROM_EMAIL = os.environ.get(
    "DJANGO_DEFAULT_FROM_EMAIL", "Mots sur Maux <bonjour@motssurmaux.ca>"
)
if os.environ.get("DJANGO_EMAIL_HOST"):
    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
    EMAIL_HOST = os.environ["DJANGO_EMAIL_HOST"]
    EMAIL_PORT = int(os.environ.get("DJANGO_EMAIL_PORT", "587"))
    EMAIL_HOST_USER = os.environ.get("DJANGO_EMAIL_HOST_USER", "")
    EMAIL_HOST_PASSWORD = os.environ.get("DJANGO_EMAIL_HOST_PASSWORD", "")
    EMAIL_USE_TLS = env_bool("DJANGO_EMAIL_USE_TLS", default=True)
else:
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"


# Database — SQLite locally; any DATABASE_URL (e.g. Postgres) in production.
try:
    import dj_database_url

    DATABASES = {
        "default": dj_database_url.config(
            default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}",
            conn_max_age=600,
        )
    }
except ImportError:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }


# Password validation
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


# Internationalization — the site is in French (Canada).
LANGUAGE_CODE = "fr-ca"

TIME_ZONE = "America/Toronto"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"

# User-uploaded files (article covers, workshop photos, ...)
MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"

# Use WhiteNoise's compressed static storage in production (if installed).
STORAGES = {
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"
    },
}
try:
    import whitenoise  # noqa: F401

    STORAGES["staticfiles"]["BACKEND"] = (
        "whitenoise.storage.CompressedManifestStaticFilesStorage"
    )
except ImportError:
    pass

# Production hardening — only kicks in when DEBUG is off (i.e. on the server).
if not DEBUG:
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_SSL_REDIRECT = env_bool("DJANGO_SECURE_SSL_REDIRECT", default=True)

# Default primary key field type
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Messages framework -> Bootstrap-free CSS classes used in templates.
from django.contrib.messages import constants as messages  # noqa: E402

MESSAGE_TAGS = {
    messages.DEBUG: "debug",
    messages.INFO: "info",
    messages.SUCCESS: "success",
    messages.WARNING: "warning",
    messages.ERROR: "error",
}
