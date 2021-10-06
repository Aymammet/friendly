import dj_database_url

from .base import *

SECRET_KEY = os.getenv('SECRET_KEY')

DEBUG = False

ALLOWED_HOSTS = ["friendlywebapp.herokuapp.com"]

INSTALLED_APPS += [
    'cloudinary',
    'cloudinary_storage',
]
# HTTPS settings
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
CSRF_COOKIE_SAMESITE = 'Strict'
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# HSTS settings
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True   
SECURE_HSTS_PRELOAD = True

MIDDLEWARE.append('whitenoise.middleware.WhiteNoiseMiddleware')

db_from_env = dj_database_url.config(conn_max_age=600)
DATABASES['default'].update(db_from_env)

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

STATIC_ROOT = BASE_DIR / 'staticfiles'
# STATIC_ROOT = os.path.join(BASE_DIR, "static")

# Cloudinary configs
CLOUDINARY_STORAGE = {
    "CLOUD_NAME": os.getenv('CLOUD_NAME'), 
    "API_KEY" : os.getenv('API_KEY'), 
    "API_SECRET": os.getenv('API_SECRET'),
}

DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'



