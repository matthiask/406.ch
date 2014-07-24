# Django settings for mkweb project.

import os
import re
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEBUG = any(r in sys.argv for r in ('runserver', 'shell', 'dbshell', 'test'))
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Matthias Kestenholz', 'mk@406.ch'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'data.db',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}

CACHES = {
    'default': {
        'BACKEND': 'redis_cache.cache.RedisCache',
        'LOCATION': '127.0.0.1:6379:1',
        'KEY_PREFIX': re.sub(r'[^\w]+', '_', '406.ch'),
        'OPTIONS': {
            'PARSER_CLASS': 'redis.connection.HiredisParser',
        },
    },
}
SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'

TIME_ZONE = 'Europe/Zurich'
LANGUAGE_CODE = 'de-ch'
USE_I18N = True
USE_L10N = True
USE_TZ = True

MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')
MEDIA_URL = '/media/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')
STATIC_URL = '/static/'

THUMBNAIL_BASEDIR = 'thumbs'

STATICFILES_DIRS = (
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '4ki81g93*_23vqxsqssws&amp;3oxzkpd^%um#!l6#006jp%vf#7e^'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'mkweb.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'mkweb.wsgi.application'

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'mkweb', 'templates'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',

    'mkadmin',
    'django.contrib.admin',

    'mkweb',
    'blog',
    'chet',
    'compressor',
    'easy_thumbnails',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.core.context_processors.request',
    'django.contrib.messages.context_processors.messages',
    'blog.context_processors.blog',
)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'root': {
        'level': 'WARNING',
        'handlers': ['sentry'],
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'skip_unreadable_post_error': {
            '()': 'mkweb.utils.SkipUnreadablePostError',
        },
    },
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(message)s',
        },
    },
    'handlers': {
        'sentry': {
            'level': 'ERROR',
            'class': 'raven.contrib.django.handlers.SentryHandler',
            'filters': [
                'require_debug_false',
                # 'skip_unreadable_post_error',
            ],
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        # Root handler.
        '': {
            'handlers': ['sentry'],
        },
        'django.request': {
            'handlers': ['sentry'],
        },
    },
}

if DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
    LOGGING['loggers'].update({
        'django.db.backends': {
            'level': 'DEBUG',
            # 'handlers': ['console'],  # Uncomment to dump SQL statements.
            'propagate': False,
        },
        'django.request': {
            'level': DEBUG,
            'handlers': ['console'],  # Dump exceptions to the console.
            'propagate': False,
        },
    })
    INSTALLED_APPS += (
        'debug_toolbar',  # Django 1.7: debug_toolbar.apps.DebugToolbarConfig
    )
    INTERNAL_IPS = ('127.0.0.1',)
    MIDDLEWARE_CLASSES = (
        'debug_toolbar.middleware.DebugToolbarMiddleware',
    ) + MIDDLEWARE_CLASSES
    DEBUG_TOOLBAR_PATCH_SETTINGS = False

try:
    from mkweb.local_settings import *  # noqa
except ImportError:
    pass

MKADMIN_CREATE = [
    'blog.Post',
    # 'blog',  # Take all models from the blog app.
    'chet.Album',
]

MKADMIN_DASHBOARD = [
    ('mkadmin.dashboard.AtAGlance', {
        'models': ['blog.Post', 'chet.Album', 'chet.Photo'],
    }),
    ('mkadmin.dashboard.AllApps', {
    }),
    ('mkadmin.dashboard.RecentActions', {
    }),
    ('mkadmin.dashboard.QuickDraft', {
    }),
    ('mkadmin.dashboard.Feed', {
        'url': 'http://www.feinheit.ch/news/feed/',
    }),
]
