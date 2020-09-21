# Django settings for box project.

from __future__ import absolute_import, unicode_literals

import os
import sys

import dj_database_url
import django_cache_url
from django.utils.translation import gettext_lazy as _
from speckenv import env


DEBUG = env(
    "DEBUG", default=any(r in sys.argv for r in ("runserver", "shell", "dbshell"))
)
TESTING = any(r in sys.argv for r in ("test",))
LIVE = env("LIVE", default=False)
FORCE_SSL = env("FORCE_SSL", default=False)
FORCE_DOMAIN = env("FORCE_DOMAIN")
ALLOWED_HOSTS = env("ALLOWED_HOSTS", required=True)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DEBUG_TOOLBAR = False
if DEBUG:
    try:
        __import__("debug_toolbar")
        DEBUG_TOOLBAR = True
        DEBUG_TOOLBAR_PATCH_SETTINGS = False
    except ImportError:
        DEBUG_TOOLBAR = False

ADMINS = (("FEINHEIT Developers", "dev@feinheit.ch"),)
MANAGERS = ADMINS
DEFAULT_FROM_EMAIL = "no-reply@fcz.ch"
SERVER_EMAIL = "root@oekohosting.ch"

DATABASES = {"default": dj_database_url.config()}

CACHES = {"default": django_cache_url.config()}

SECRET_KEY = env("SECRET_KEY", required=True)

TIME_ZONE = "Europe/Zurich"
LANGUAGE_CODE = "en"
LANGUAGES = (
    # ('de', _('German')),
    # ('fr', _('French')),
    ("en", _("English")),
)

USE_I18N = True
USE_L10N = True
USE_TZ = True

MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_URL = "/media/"

STATIC_ROOT = os.path.join(BASE_DIR, "static")
STATIC_URL = "/static/"

STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
)

MIDDLEWARE = [
    m
    for m in [
        "debug_toolbar.middleware.DebugToolbarMiddleware" if DEBUG_TOOLBAR else "",
        (
            "django.middleware.security.SecurityMiddleware"
            if FORCE_SSL
            else "app.middleware.force_domain"
        ),
        "django.contrib.sessions.middleware.SessionMiddleware",
        "django.middleware.common.CommonMiddleware",
        "django.middleware.csrf.CsrfViewMiddleware",
        "django.middleware.locale.LocaleMiddleware",
        "django.contrib.auth.middleware.AuthenticationMiddleware",
        # '' if LIVE else 'app.middleware.only_staff',
        "django.contrib.messages.middleware.MessageMiddleware",
        "django.middleware.clickjacking.XFrameOptionsMiddleware",
    ]
    if m
]

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "app", "templates")],
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "blog.context_processors.blog",
            ],
            "loaders": [
                "django.template.loaders.filesystem.Loader",
                "django.template.loaders.app_directories.Loader",
            ]
            if DEBUG
            else [
                (
                    "django.template.loaders.cached.Loader",
                    [
                        "django.template.loaders.filesystem.Loader",
                        "django.template.loaders.app_directories.Loader",
                    ],
                )
            ],
            "debug": DEBUG,
        },
    }
]

ROOT_URLCONF = "app.urls"
WSGI_APPLICATION = "wsgi.application"

LOCALE_PATHS = (os.path.join(BASE_DIR, "conf", "locale"),)

INSTALLED_APPS = [
    app
    for app in [
        "django.contrib.auth",
        "django.contrib.contenttypes",
        "django.contrib.sessions",
        "django.contrib.messages",
        "django.contrib.staticfiles",
        "authlib.admin_oauth",
        "variable_admin",
        "django.contrib.admin",
        "django.contrib.sitemaps",
        "app",
        "blog",
        "cabinet",
        "authlib.little_auth",
        "webpack_loader",
        "raven.contrib.django.raven_compat",
        "debug_toolbar.apps.DebugToolbarConfig" if DEBUG_TOOLBAR else "",
    ]
    if app
]

WEBPACK_LOADER = {
    "DEFAULT": {
        "STATS_FILE": os.path.join(
            BASE_DIR, "static", "webpack-stats-%s.json" % ("dev" if DEBUG else "prod")
        )
    }
}

AUTHENTICATION_BACKENDS = (
    "authlib.backends.EmailBackend",
    "django.contrib.auth.backends.ModelBackend",
)
AUTH_USER_MODEL = "little_auth.User"

SESSION_ENGINE = "django.contrib.sessions.backends.signed_cookies"
SESSION_COOKIE_HTTPONLY = True

RAVEN_CONFIG = {"dsn": env("SENTRY_DSN")}

CKEDITOR_CONFIGS = {
    "richtext-plugin": {
        "toolbar": "Custom",
        "format_tags": "h1;h2;h3;p;pre",
        "toolbar_Custom": [
            ["Format", "RemoveFormat"],
            [
                "Bold",
                "Italic",
                "Strike",
                "-",
                "NumberedList",
                "BulletedList",
                "-",
                "Anchor",
                "Link",
                "Unlink",
                "-",
                "Source",
            ],
        ],
    }
}

if DEBUG:
    # `debug` is only True in templates if the vistor IP is in INTERNAL_IPS.
    INTERNAL_IPS = type(str("c"), (), {"__contains__": lambda *a: True})()
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

    # DEFAULT_FILE_STORAGE = 'http_fallback_storage.FallbackStorage'
    # FALLBACK_STORAGE_URL = 'http://fcz.ch.fcz01.nine.ch/media/'

if FORCE_SSL:
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    if FORCE_DOMAIN:
        SECURE_SSL_REDIRECT = True
        SECURE_SSL_HOST = FORCE_DOMAIN
    # SECURE_HSTS_SECONDS = 30 * 86400
    # SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTOCOL", "https")
else:
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

# Avoid a problem with PIL's too small blocksize when decoding really big
# JPEGs.
# https://github.com/matthewwithanm/django-imagekit/issues/50

from PIL import ImageFile  # noqa, avoid warning


if ImageFile.MAXBLOCK < 1024 * 1024:
    ImageFile.MAXBLOCK = 1024 * 1024

X_FRAME_OPTIONS = "DENY"
# CSRF_COOKIE_HTTPONLY = True

GOOGLE_CLIENT_ID = env("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = env("GOOGLE_CLIENT_SECRET")

ADMIN_OAUTH_PATTERNS = [(r"@406\.ch$", "mk@406.ch")]
