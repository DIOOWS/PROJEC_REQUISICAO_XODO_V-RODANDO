from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

# ============================================================
# BASE
# ============================================================

SECRET_KEY = 'sua-secret-key'
DEBUG = False   # Render produção = SEMPRE False

ALLOWED_HOSTS = [
    "127.0.0.1",
    "localhost",
    ".onrender.com",
]

# ============================================================
# APPS
# ============================================================

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'core',
]

# ============================================================
# MIDDLEWARE
# ============================================================

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',

    # WhiteNoise DEVE vir logo depois do SecurityMiddleware
    'whitenoise.middleware.WhiteNoiseMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'requisicoes.urls'

# ============================================================
# TEMPLATE ENGINE
# ============================================================

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / "core" / "templates",
        ],
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

WSGI_APPLICATION = 'requisicoes.wsgi.application'

# ============================================================
# DATABASE
# ============================================================

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# ============================================================
# INTERNATIONALIZATION
# ============================================================

LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_TZ = True

# ============================================================
# STATIC FILES (WhiteNoise CONFIG CORRETA)
# ============================================================

STATIC_URL = "/static/"

STATICFILES_DIRS = [
    BASE_DIR / "core" / "static",
]

STATIC_ROOT = BASE_DIR / "staticfiles"

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# ============================================================
# MEDIA (uploads locais)
# ============================================================

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# ============================================================
# LOGIN
# ============================================================

LOGIN_URL = "/login/"
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/login/"

# ============================================================
# WEASYPRINT
# ============================================================

WEASYPRINT_BASEURL = BASE_DIR

# ============================================================
# SUPABASE
# ============================================================

# Carrega variáveis de ambiente do Render
SUPABASE_URL = os.environ.get(
    "SUPABASE_URL",
    "https://dwpoetiqoflhmvufalyf.supabase.co"
)

SUPABASE_KEY = os.environ.get(
    "SUPABASE_KEY",
    "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIs..."
)

SUPABASE_BUCKET = "DISPERDICIO"

# URL da logo no bucket "system" (caso queira usar no template)
LOGO_URL = os.environ.get("LOGO_URL", "")

# ============================================================
# CONTEXT PROCESSOR GLOBAL
# ============================================================

TEMPLATES[0]["OPTIONS"]["context_processors"].append(
    "core.context_processors.global_settings"
)

CSRF_TRUSTED_ORIGINS = [
    "https://projec-requisicao-xodo-v-rodando.onrender.com",
]

ALLOWED_HOSTS = [
    "127.0.0.1",
    "localhost",
    "projec-requisicao-xodo-v-rodando.onrender.com",
]
