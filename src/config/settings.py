import os
from configparser import ConfigParser


config = ConfigParser()
config.read('../config.ini')

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = config['settings']['DJANGO_SECRET_KEY']

DEBUG = config['settings']['DEBUG_MODE']

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.sites',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'tracker',
]

MIDDLEWARE = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.sites.middleware.CurrentSiteMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

AUTH_PASSWORD_VALIDATORS = []

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

SITE_ID = 1

SESSION_ENGINE = "django.contrib.sessions.backends.cache"

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')
]

# WHERE THE POSTERS ARE STORED
POSTER_PATH = os.path.join(BASE_DIR, 'static', 'images', 'posters')


# THE MOVIE DATABASE API KEY
''' 
https://developers.themoviedb.org
The Movie Database (TMDb) is a community built movie and TV database. 
Every piece of data has been added by our amazing community dating back to 2008. 
TMDb's strong international focus and breadth of data is largely unmatched and 
something we're incredibly proud of. Put simply, we live and breathe community 
and that's precisely what makes us different.
'''
API_KEY = config['api_keys']['TMDB_API_KEY']
