# Django settings for box project.

from __future__ import absolute_import, unicode_literals

from env import env
import dj_database_url
import django_cache_url
from django.utils.translation import ugettext_lazy as _
import os
import sys

DEBUG = any(r in sys.argv for r in ('runserver', 'shell', 'dbshell'))
TESTING = any(r in sys.argv for r in ('test',))
LIVE = env('LIVE', default=False)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DEBUG_TOOLBAR = False
if DEBUG:
    try:
        __import__('debug_toolbar')
        DEBUG_TOOLBAR = True
        DEBUG_TOOLBAR_PATCH_SETTINGS = False
    except ImportError:
        DEBUG_TOOLBAR = False

ADMINS = (
    ('FEINHEIT Developers', 'dev@feinheit.ch'),
)
MANAGERS = ADMINS
DEFAULT_FROM_EMAIL = 'no-reply@fcz.ch'
SERVER_EMAIL = 'root@oekohosting.ch'

DATABASES = {
    'default': dj_database_url.config(),
}

CACHES = {
    'default': django_cache_url.config(),
}

SECRET_KEY = env('SECRET_KEY', required=True)
FORCE_DOMAIN = env('FORCE_DOMAIN')
ALLOWED_HOSTS = env('ALLOWED_HOSTS', required=True)

TIME_ZONE = 'Europe/Zurich'
LANGUAGE_CODE = 'de'
LANGUAGES = (
    ('de', _('German')),
    # ('fr', _('French')),
    # ('en', _('English')),
)

USE_I18N = True
USE_L10N = True
USE_TZ = True

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

MIDDLEWARE_CLASSES = [m for m in [
    'mkweb.middleware.ForceDomainMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware' if DEBUG_TOOLBAR else '',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    # '' if LIVE else 'app.middleware.OnlyStaffMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
] if m]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'app', 'templates'),
        ],
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'blog.context_processors.blog',
            ],
            'loaders': [
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
            ] if DEBUG else [
                ('django.template.loaders.cached.Loader', [
                    'django.template.loaders.filesystem.Loader',
                    'django.template.loaders.app_directories.Loader',
                ]),
            ],
            'debug': DEBUG,
        },
    },
]

ROOT_URLCONF = 'mkweb.urls'
WSGI_APPLICATION = 'wsgi.application'

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'conf', 'locale'),
)

INSTALLED_APPS = [app for app in [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',

    'mkweb',
    'blog',

    'admin_sso',
    'webpack_loader',
    'raven.contrib.django.raven_compat',

    'debug_toolbar.apps.DebugToolbarConfig' if DEBUG_TOOLBAR else '',
] if app]

WEBPACK_LOADER = {
    'DEFAULT': {
        'BUNDLE_DIR_NAME': 'build/' if DEBUG else 'dist/',
        'STATS_FILE': os.path.join(
            BASE_DIR,
            'tmp',
            'webpack-stats.json' if DEBUG else 'webpack-stats-prod.json',
        ),
        'POLL_DELAY': 0.2,
        'IGNORE': ['.+\.hot-update.js', '.+\.map']
    },
}

DJANGO_ADMIN_SSO_OAUTH_CLIENT_ID = env(
    'DJANGO_ADMIN_SSO_OAUTH_CLIENT_ID')
DJANGO_ADMIN_SSO_OAUTH_CLIENT_SECRET = env(
    'DJANGO_ADMIN_SSO_OAUTH_CLIENT_SECRET')
DJANGO_ADMIN_SSO_ADD_LOGIN_BUTTON = all((
    DJANGO_ADMIN_SSO_OAUTH_CLIENT_ID,
    DJANGO_ADMIN_SSO_OAUTH_CLIENT_SECRET,
))
DJANGO_ADMIN_SSO_AUTH_URI = 'https://accounts.google.com/o/oauth2/auth'
DJANGO_ADMIN_SSO_TOKEN_URI = 'https://accounts.google.com/o/oauth2/token'
DJANGO_ADMIN_SSO_REVOKE_URI = 'https://accounts.google.com/o/oauth2/revoke'
AUTHENTICATION_BACKENDS = (
    'admin_sso.auth.DjangoSSOAuthBackend',
    'django.contrib.auth.backends.ModelBackend',
)

SESSION_ENGINE = 'django.contrib.sessions.backends.signed_cookies'
SESSION_COOKIE_HTTPONLY = True

RAVEN_CONFIG = {
    'dsn': env('SENTRY_DSN'),
}

CKEDITOR_CONFIGS = {
    'richtext-plugin': {
        'toolbar': 'Custom',
        'format_tags': 'h1;h2;h3;p;pre',
        'toolbar_Custom': [
            ['Format', 'RemoveFormat'],
            ['Bold', 'Italic', 'Strike', '-',
             'NumberedList', 'BulletedList', '-',
             'Anchor', 'Link', 'Unlink', '-',
             'Source'],
        ]
    }
}

if DEBUG:
    # `debug` is only True in templates if the vistor IP is in INTERNAL_IPS.
    INTERNAL_IPS = type(str('c'), (), {'__contains__': lambda *a: True})()
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

    # DEFAULT_FILE_STORAGE = 'http_fallback_storage.FallbackStorage'
    # FALLBACK_STORAGE_URL = 'http://fcz.ch.fcz01.nine.ch/media/'

# Avoid a problem with PIL's too small blocksize when decoding really big
# JPEGs.
# https://github.com/matthewwithanm/django-imagekit/issues/50

from PIL import ImageFile  # noqa, avoid warning

if ImageFile.MAXBLOCK < 1024 * 1024:
    ImageFile.MAXBLOCK = 1024 * 1024

X_FRAME_OPTIONS = 'DENY'
CSRF_COOKIE_HTTPONLY = True
