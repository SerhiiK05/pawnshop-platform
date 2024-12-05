from config.settings.base import *

DEBUG = os.environ.get('DJANGO_DEBUG', '') != 'False'

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.dev")


ALLOWED_HOSTS = ["127.0.0.1"]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
