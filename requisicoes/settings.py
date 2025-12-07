from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'sua-secret-key'
DEBUG = True

ALLOWED_HOSTS = [
    "127.0.0.1",
    "localhost",
    "192.168.100.26",  # Rede local
    ".onrender.com",   # Render (produção)
]

# -------------------------------------------------------
# APPS
# -------------------------------------------------------

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    "core",
]

# -------------------------------------------------------
# MIDDLEWARE
# -------------------------------------------------------

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",   # << OBRIGATÓRIO AQUI
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "requisicoes.urls"

# -------------------------------------------------------
# TEMPLATES
# -------------------------------------------------------

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            BASE_DIR / "core" / "templates"
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "requisicoes.wsgi.application"

# -------------------------------------------------------
# DATABASE
# -------------------------------------------------------

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# -------------------------------------------------------
# INTERNACIONALIZAÇÃO
# -------------------------------------------------------

LANGUAGE_CODE = "pt-br"
TIME_ZONE = "America/Sao_Paulo"
USE_I18N = True
USE_TZ = True

# -------------------------------------------------------
# ARQUIVOS ESTÁTICOS (STATIC)
# -------------------------------------------------------

STATIC_URL = "/static/"

# Pasta dos seus arquivos estáticos locais (logo, css do app)
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "core", "static"),
]

# Pasta onde o Django junta tudo para produção
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

# WhiteNoise — compressão e hash
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# -------------------------------------------------------
# UPLOADS (MEDIA)
# -------------------------------------------------------

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

# -------------------------------------------------------
# WEASYPRINT (PDF)
# -------------------------------------------------------

WEASYPRINT_BASEURL = BASE_DIR

# -------------------------------------------------------
# LOGIN
# -------------------------------------------------------

LOGIN_URL = "/login/"
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/login/"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
