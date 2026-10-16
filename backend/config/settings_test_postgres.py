from .settings import *  # noqa: F401,F403

DEBUG = False
SECRET_KEY = "postgres-test-secret"
ALLOWED_HOSTS = ["testserver", "localhost"]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("POSTGRES_DB", "domusos_test"),
        "USER": os.getenv("POSTGRES_USER", "domusos"),
        "PASSWORD": os.getenv("POSTGRES_PASSWORD", "domusos"),
        "HOST": os.getenv("POSTGRES_HOST", "localhost"),
        "PORT": os.getenv("POSTGRES_PORT", "5432"),
    }
}

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
    }
}

EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"
CELERY_TASK_ALWAYS_EAGER = True
CELERY_TASK_EAGER_PROPAGATES = True
USE_S3 = False
ANTIVIRUS_ENABLED = False
RATE_LIMIT_ENABLED = False
PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]
