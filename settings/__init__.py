"""
Django settings for ITT data-sources project.

Generated by 'django-admin startproject' using Django 1.10.1.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

import os
import sys
import logging

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE_ROOT = os.path.realpath(os.path.join(os.path.dirname(__file__), '..'))


# Add the local vendor libs path
sys.path.append(BASE_DIR + "/vendorlibs")


# DEFINE THE ENVIRONMENT TYPE
PRODUCTION = STAGE = DEMO = LOCAL = False
dt_key = os.environ.get('DEPLOYMENT_TYPE', 'LOCAL')
if dt_key == 'PRODUCTION':
    PRODUCTION = True
elif dt_key == 'DEMO':
    DEMO = True
elif dt_key == 'STAGE':
    STAGE = True
elif dt_key == 'LOCAL':
    LOCAL = True
else:
    raise Exception("Cannot find the DEPLOYMENT_TYPE environment variable. This is to be provided along with other vital env vars. If this instance is running locally, the '.env' file must be provided. If this instance is running on production, the environment variables have not been set up correctly. See the readme.md for more details.")


# Set up logger
if LOCAL:
    log_level = logging.DEBUG
elif PRODUCTION:
    log_level = logging.INFO
else:
    log_level = logging.DEBUG

logging.basicConfig(level=log_level)
logger = logging.getLogger(__name__)

if LOCAL or STAGE:
    logging.getLogger('boto').setLevel(logging.INFO)
    logging.getLogger('pyqs').setLevel(logging.INFO)

logger.info("Deployment environment detected: {}".format(dt_key))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = LOCAL or STAGE

WSGI_APPLICATION = 'settings.wsgi.application'

SITE_BASE_URL = os.environ.get('SITE_BASE_URL')
SERVICE_EMAIL_ADDRESS = "info@intelligenttrading.org"
SUPPORT_EMAIL_ADDRESS = "info@intelligenttrading.org"
DEFAULT_FROM_EMAIL = "info@intelligenttrading.org"

ALLOWED_HOSTS = [
    '.intelligenttrading.org',
    '.in7el.trade',
    '.herokuapp.com',
    'localhost',
]

# APPLICATION DEFINITION
INSTALLED_APPS = [
    # MAIN APPS
    'apps.common',
    'apps.channel',

    # DJANGO APPS
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.sessions',
    'django.contrib.contenttypes',

    # PLUGINS

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
]

ROOT_URLCONF = 'settings.urls'

TEMPLATES = []


# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = False
USE_L10N = False
USE_TZ = False # need for unixtimestamp

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/
STATIC_ROOT = STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    os.path.join(SITE_ROOT, 'static'),
)

LOGIN_REDIRECT_URL = '/'


# App setting
EXCHANGE_MARKETS = ('poloniex', 'binance', 'bittrex') #, 'bitfinex', 'kucoin') # 'gdax') # gdax API does not allow to fetch all tickers at once with a single call to fetch_tickers() for now
TICKERS_MINIMUM_USD_VOLUME = 5000
SNS_PRICES_BATCH_SIZE = 100 # Number of ohlc prices in one SNS message

(POLONIEX, BITTREX, BINANCE, BITFINEX, KUCOIN, GDAX, HITBTC) = list(range(7))
SOURCE_CHOICES = (
    (POLONIEX, 'poloniex'),
    (BITTREX, 'bittrex'),
    (BINANCE, 'binance'),
    (BITFINEX, 'bitfinex'),
    (KUCOIN, 'kucoin'),
    (GDAX, 'gdax'),
    (HITBTC, 'hitbtc'),
)

# list of supported counter currencies.
# We save to history trading pairs only with these counter currencies 
COUNTER_CURRENCIES = ('BTC', 'ETH', 'USDT')

(BTC, ETH, USDT, XMR) = list(range(4))
COUNTER_CURRENCY_CHOICES = (
    (BTC, 'BTC'),
    (ETH, 'ETH'),
    (USDT, 'USDT'),
    (XMR, 'XMR'),
)

# General apps settings
if PRODUCTION or STAGE:
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

if LOCAL:
    PUBLISH_MESSSAGES = False # Do not send messages to sns in local environment
else:
    PUBLISH_MESSSAGES = os.environ.get("PUBLISH_MESSSAGES", "true").lower() == "true" # env variables are strings, not boolean

logger.info("Importing vendor_services_settings")
try:
    from settings.vendor_services_settings import *
except:
    logger.warning("Failed to import vendor_services_settings.")
    pass


if LOCAL:
    logger.info("LOCAL environment detected. Importing local_settings.py")
    try:
        from settings.local_settings import *
    except:
        logger.error("Could not successfully import local_settings.py. This is necessary if you are running locally. This file should be in version control.")
        raise


ITF_API = os.environ.get('ITF_API_HOST', "http://127.0.0.1:8000/api")
ITF_API_KEY = os.environ.get('ITF_API_KEY', "ABC123")
