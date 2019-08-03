import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
    os.path.join(BASE_DIR, "home", "static"),
    os.path.join(BASE_DIR, "dashboard", "static"),
]
LOGIN_REDIRECT_URL = '/accounts/personalize'
LOGOUT_REDIRECT_URL = '/'
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '&tm9%utcwp=rzanx9%jxn27gnck^4#65316g&6fei94==dml*6'
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
ALLOWED_HOSTS = ['*']
INSTALLED_APPS = [
    'home.apps.HomeConfig',
    'accounts.apps.AccountsConfig',
    'dashboard.apps.DashboardConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.facebook',
    'tz_detect',
    'rest_framework',
    'rest_framework.authtoken',
    'rest_auth',
    'rest_auth.registration',
    'webpack_loader',
]
SITE_ID = 2
WEBPACK_LOADER = {
    'DEFAULT': {
        'BUNDLE_DIR_NAME': 'bundles/',
        'STATS_FILE': os.path.join(BASE_DIR, 'webpack-stats.json'),
    }
}
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
    )
}
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'tz_detect.middleware.TimezoneMiddleware',
]
ROOT_URLCONF = 'schedule_lessons.urls'
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, "templates")],
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
WSGI_APPLICATION = 'schedule_lessons.wsgi.application'
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
AUTHENTICATION_BACKENDS = (
 'django.contrib.auth.backends.ModelBackend',
 "allauth.account.auth_backends.AuthenticationBackend"
)
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
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_LOGOUT_ON_GET = True
ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_EMAIL_REQUIRED = True
REST_AUTH_REGISTER_SERIALIZERS = {
    'REGISTER_SERIALIZER': 'api.serializers.RegisterSerializer',
}
ACCOUNT_FORMS = {'signup': 'accounts.forms.MyCustomSignupForm'}
ACCOUNT_LOGIN_ATTEMPTS_LIMIT = 7
ACCOUNT_LOGIN_ATTEMPTS_TIMEOUT = 180
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True
STATIC_URL = '/static/'
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'static/images/media/')
STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'

# ie if Heroku server
if 'DATABASE_URL' in os.environ:
    import dj_database_url
    db_from_env = dj_database_url.config()
    DATABASES['default'].update(db_from_env)

try:
    from .local_settings import *
except ImportError:
    pass
