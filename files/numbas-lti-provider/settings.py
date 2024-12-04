#######################################################################
# Settings for the Numbas LTI provider
# For help with this file, see
#   https://docs.numbas.org.uk/lti/en/latest/installation/settings.html
#######################################################################

import os
import pylti1p3.roles
import environ

env = environ.Env(
    DEBUG = (bool, False),
    LOGLEVEL = (str,' WARNING'),
    INSTANCE_NAME = (str, 'Docker'),
    LANGUAGE_CODE = (str, 'en'),
    TIME_ZONE = (str, 'UTC'),
    SUPPORT_NAME = (str, 'the Numbas team'),
    SUPPORT_URL = (str, None),
    EMAIL_COMPLETION_RECEIPTS = (bool, False),
    DEFAULT_FROM_EMAIL = (str,None),
    NUMBAS_LOCKDOWN_APP_PASSWORD = (str, ''),
)

# Show debug information when there are errors?
# Set this to False when running in production!
DEBUG = env('DEBUG')

##########################
# Settings that shouldn't change.
# You can ignore these, but they must be present.
##########################

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DEFAULT_AUTO_FIELD='django.db.models.AutoField'

SESSION_COOKIE_NAME = 'numbas_lti_provider'

LOGIN_URL = '/login'

INSTALLED_APPS = [
    'daphne',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'numbas_lti.apps.PyLTI1p3ToolConfigBigAutoField',
    'channels',
    'statici18n',
    'huey.contrib.djhuey',
    'numbas_lti',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django_auth_lti.middleware_patched.MultiLTILaunchAuthMiddleware',
    'numbas_lti.middleware.NumbasLTIResourceMiddleware',
]

AUTHENTICATION_BACKENDS = [
    'numbas_lti.backends.LTI_11_AuthBackend',
    'numbas_lti.backends.LTI_13_AuthBackend',
    'django.contrib.auth.backends.ModelBackend'
]

ROOT_URLCONF = 'numbasltiprovider.urls'

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
                'django.template.context_processors.i18n',
                'numbas_lti.context_processors.global_settings',
            ],
        },
    },
]

ASGI_APPLICATION = 'numbasltiprovider.asgi.application'

# A secret key used for cryptography - this is set by the setup script.
SECRET_KEY = env('SECRET_KEY')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': env('LOGLEVEL').upper(),
    },
}

HUEY = {
	'huey_class': 'huey.PriorityRedisHuey',
    'connection': {
        'host': 'redis',
        'port': 6379,
    },
}

# Password validation
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

LOCALE_PATHS = (os.path.join(BASE_DIR,'locale'),)

USE_I18N = True

USE_L10N = True

USE_TZ = True

MEDIA_URL = '/media/'

STATIC_URL = '/static/'

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage',
    }
}

SECURE_CONTENT_TYPE_NOSNIFF = True

SECURE_SSL_REDIRECT = False

SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SAMESITE = 'None'
CSRF_COOKIE_SAMESITE = 'None'
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

##############################
# Settings you can change.
##############################

# The name of this instance.
# Shown in the footer of most pages.
INSTANCE_NAME = env('INSTANCE_NAME')

# Which domain names can this server be accessed through?
ALLOWED_HOSTS = [env('SERVERNAME'), '127.0.0.1', 'localhost']

# Which roles should be interpreted as conferring instructor privileges?
LTI_INSTRUCTOR_ROLES = {
    'lti_11': ['Instructor','Administrator','ContentDeveloper','Manager','TeachingAssistant'],
    'lti_13': [pylti1p3.roles.TeacherRole, pylti1p3.roles.TeachingAssistantRole, pylti1p3.roles.StaffRole, pylti1p3.roles.DesignerRole,]
}

# Database connection details
# This is normally set by the setup script.
# See https://docs.djangoproject.com/en/3.2/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'numbas_lti',
        'USER': 'numbas_lti',
        'PASSWORD': env('POSTGRES_PASSWORD'),
        'HOST': 'postgres',
    }
}

# Cache details.
# See https://docs.djangoproject.com/en/4.2/topics/cache/
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        "LOCATION": os.environ.get('REDIS_URL','redis://redis:6379'),
    }
}

# Channels communication layers.
# This is normally set by the setup script.
# See https://channels.readthedocs.io/en/stable/topics/channel_layers.html
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [os.environ.get('REDIS_URL','redis://redis:6379')],
        },
    },
}

# The language to use for the interface.
# Available languages: 'en' (English), 'de' (German/Deutsch)
LANGUAGE_CODE = env('LANGUAGE_CODE')

# The time zone that the server should use to display dates and times.
# See https://docs.djangoproject.com/en/3.2/ref/settings/#std:setting-TIME_ZONE
TIME_ZONE = env('TIME_ZONE')

# The filesystem path where media files are stored.
MEDIA_ROOT = '/srv/numbas-lti-media/'

# The filesystem path where static files are stored.
STATIC_ROOT = '/srv/numbas-lti-static/'

# The name of your support contact.
SUPPORT_NAME = env('SUPPORT_NAME')

# An address to get support. When there's an error, students will be shown a link to this address.
# Set to "mailto:your_email_address", or the URL of a page containing contact info.
# Or set to None if you don't want to show a link.
SUPPORT_URL = env('SUPPORT_URL')

# Enable sending attempt completion receipts by email?
EMAIL_COMPLETION_RECEIPTS = env('EMAIL_COMPLETION_RECEIPTS')

# The email address to send emails from.
DEFAULT_FROM_EMAIL = env('DEFAULT_FROM_EMAIL')

# Connection details for sending email through SMTP
EMAIL_CONFIG = env.email_url('EMAIL_URL', default = 'smtp://localhost')

if EMAIL_CONFIG is not None:
    vars().update(EMAIL_CONFIG)

# The number of seconds to wait for requests to timeout, such as outcome reports or fetching SCORM packages.
REQUEST_TIMEOUT = 60

# The number of days after creation to keep report files before deleting them.
REPORT_FILE_EXPIRY_DAYS = 30

# Settings for the lockdown app
LOCKDOWN_APP = {
    # Password that users must enter to decrypt launch info
    'password': env('NUMBAS_LOCKDOWN_APP_PASSWORD'),

    # Salt for encrypted links to launch the lockdown app.
    # This is built into the lockdown app, so shouldn't change unless you have your own version.
    'salt': '45ab2cf2e139c01f8447d17dc653d585',

    # The URL to download the Numbas lockdown app from.
    'install_url': 'https://www.numbas.org.uk/lockdown-app',

    # The URL to download the Safe Exam Browser app from.
    'seb_install_url': 'https://safeexambrowser.org/download_en.html',
}

# The User-Agent header string to use for any requests made by this tool. The version of the software is appended to the string given here.
REQUESTS_USER_AGENT = 'Numbas LTI provider'

# The root URL of the documentation. If not set here, it's set based on the current version, relative to docs.numbas.org.uk.
#HELP_URL = 'https://docs.numbas.org/uk/lti/latest/'

# Presets for Canvas LTI 1.3 settings.
CANVAS_LTI_13_PRESETS = {
    'canvas': {
        'label': 'Production',
        'issuer': 'https://canvas.instructure.com',
        'key_set_url': 'https://canvas.instructure.com/api/lti/security/jwks',
        'auth_login_url': 'https://canvas.instructure.com/api/lti/authorize_redirect',
        'auth_token_url': 'http://canvas.instructure.com/login/oauth2/token',
    },
    'canvas_beta': {
        'label': 'Beta',
        'issuer': 'https://canvas.beta.instructure.com',
        'key_set_url': 'https://canvas.beta.instructure.com/api/lti/security/jwks',
        'auth_login_url': 'https://canvas.beta.instructure.com/api/lti/authorize_redirect',
        'auth_token_url': 'http://canvas.beta.instructure.com/login/oauth2/token',
    },
    'canvas_test': {
        'label': 'Test',
        'issuer': 'https://canvas.test.instructure.com',
        'key_set_url': 'https://canvas.test.instructure.com/api/lti/security/jwks',
        'auth_login_url': 'https://canvas.test.instructure.com/api/lti/authorize_redirect',
        'auth_token_url': 'http://canvas.test.instructure.com/login/oauth2/token',
    },
}

