# Django settings for djangonyc project.
import os.path

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ROOT_URLCONF = 'djangonyc.urls'

FACEBOOK_API_KEY='192420697463211'    		# change to your facebook api key
FACEBOOK_SECRET_KEY='22d1178e41580fb02fbfeb7706e2f1c2' 	# change to your facebook app secret key
FACEBOOK_INTERNAL=True
ACCOUNT_ACTIVATION_DAYS=30
NUM_FRIEND_RETRIEVE_LIMIT=50   # the limit to the # of friends to retrieve
#Cache facebook info for x seconds. Default is 30 minutes
FACEBOOK_CACHE_TIMEOUT = 1800


ADMINS = (
    # ('Michael Trosen', 'mrtrosen@lab305.com'),
)

MANAGERS = ADMINS

DATABASE_ENGINE = 'sqlite3'           # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'ado_mssql'.
DATABASE_NAME = 'fb'             # Or path to database file if using sqlite3.
DATABASE_USER = ''             # Not used with sqlite3.
DATABASE_PASSWORD = ''         # Not used with sqlite3.
DATABASE_HOST = ''             # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = ''             # Set to empty string for default. Not used with sqlite3.

# Local time zone for this installation. Choices can be found here:
# http://www.postgresql.org/docs/8.1/static/datetime-keywords.html#DATETIME-TIMEZONE-SET-TABLE
# although not all variations may be possible on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Asia/Kolkata'

# Language code for this installation. All choices can be found here:
# http://www.w3.org/TR/REC-html40/struct/dirlang.html#langcodes
# http://blogs.law.harvard.edu/tech/stories/storyReader$15
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True


# URL that handles the media served from MEDIA_ROOT.
# Example: "http://media.lawrence.com"
MEDIA_URL = ''

# make the session expire when the user closes their browser
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'ba#&)u3p0m0#cwmt-7-)%g#0p9t$6%uosf0k%ggk3yp(farr5y'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'facebook.djangofb.FacebookMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'facebookconnect.middleware.FacebookConnectMiddleware',
)


TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    #'/home/mrtrosen/work/djangonyc/templates'
    os.path.join(os.path.dirname(__file__), 'templates').replace('\\','/'),
)

AUTHENTICATION_BACKENDS = (
    'facebookconnect.models.FacebookBackend',
    'django.contrib.auth.backends.ModelBackend',
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'socmov.exampleapp',
    'socmov.facebookconnect',
)

