"""
Django settings for sisgrs project.

Generated by 'django-admin startproject' using Django 2.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'y^a8godqs9s%2qmn2k9s2@u!r&dc)(jtj1m8vkb#9sm$0_&2$d'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'dal',
    'dal_select2',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'crispy_forms', # módulo para gerar formulários com bs4
    
    'planogrs.apps.PlanogrsConfig', # ativa este módulo
    'usuarios.apps.UsuariosConfig', # ativa este módulo
    'erros.apps.ErrosConfig',  # ativa este módulo
    'movimentarplano.apps.MovimentarplanoConfig',  # ativa este módulo
    'chamados.apps.ChamadosConfig', # ativar módulo

    'django_cleanup.apps.CleanupConfig',  # app para remover arquivos antigos
    
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'sisgrs.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [ os.path.join(BASE_DIR, 'templates') ],
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

WSGI_APPLICATION = 'sisgrs.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

# Rodar na máquina local
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Rodar no servidor
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'rafaelzottesso',
#         'USER': 'rafaelzottesso',
#         'PASSWORD': 'ifpr2019',
#         'HOST': 'pgsql.rafaelzottesso.com.br',
#         'PORT': '5432',
#     }
# }



# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'pt-br'

TIME_ZONE = 'America/Sao_Paulo'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATICFILES_DIRS = [
	os.path.join(BASE_DIR, "static"),
]

# Rodar na máquina local
STATIC_URL = '/static/'
# Rodar no servidor
# STATIC_URL = '/static/sisgrs/'
# STATIC_ROOT = '/home/rafaelzottesso/www/static/sisgrs/'


# Upload files dir
MEDIA_URL = '/uploads/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'uploads')

# Crispy Forms Config
CRISPY_TEMPLATE_PACK = 'bootstrap4'


# Nome da URL em que o usuário será redirecionado
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth
LOGIN_REDIRECT_URL = 'index-auth'
LOGIN_URL = 'login'
LOGOUT_REDIRECT_URL = 'index'

# Configurações de envio de email
# https://docs.djangoproject.com/en/2.2/topics/email/
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'sisgrs.notifica@gmail.com'
DEFAULT_FROM_EMAIL = 'sisgrs.notifica@gmail.com'
EMAIL_HOST_PASSWORD = '@IFPR2019'
EMAIL_USE_TLS = True


# Configurações da prefeitura para personalizar mensagens
PREFEITURA_NOME = "Prefeitura Municipal de Paranavaí"
PREFEITURA_CIDADE = "Paranavaí/PR"
PREFEITURA_SITE = "http://www.paranavai.pr.gov.br/"
PREFEITURA_FONE = "(44) 3421-2323"
PREFEITURA_ENDERECO = "R. Getúlio Vargas, 900 - Centro, Paranavaí - PR, 87702-000"
