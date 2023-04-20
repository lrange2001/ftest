"""
Django settings for ftest project.

Generated by 'django-admin startproject' using Django 4.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

from pathlib import Path
import read_config
import os
from log.logserver import outputLog

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-s%4)36)&(=x238=9=3&3md445_&99-68$0d^7s4=uy)fndr#4s'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'server',
    'rest_framework',
    'rest_framework.authtoken',
    'channels',
    'corsheaders',
    'appdeploy',
    'docapp'
]

ASGI_APPLICATION = 'server.websocket.routing.application'
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_METHODS = (
 'DELETE',
 'GET',
 'OPTIONS',
 'PATCH',
 'POST',
 'PUT',
 'VIEW',
)

CORS_ALLOW_HEADERS = (
 'XMLHttpRequest',
 'X_FILENAME',
 'accept-encoding',
 'authorization',
 'content-type',
 'dnt',
 'origin',
 'user-agent',
 'x-csrftoken',
 'x-requested-with',
 'Pragma',
 'Authorization'
)

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    #'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware'
]

ROOT_URLCONF = 'ftest.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
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

WSGI_APPLICATION = 'ftest.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }
db = read_config.main('db')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': db['db_database'],
        'USER': db['db_user'],
        'PASSWORD': db['db_pass'],
        'HOST': db['db_host'],
        'PORT': db['db_port'],
    }
}
outputLog(logger_name='settings').info('加载数据库信息 服务端返回%s'%db)
# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES':(
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_PAGINATION_CLASS': 'server.other.ftestPageNumberPagination.Mypageination',  # 开启分页
    'PAGE_SIZE': 10,  # 每页显示10页
    'DEFAULT_FILTER_BACKENDS': ('django_filters.rest_framework.DjangoFilterBackend',)
}
#
# LOGGING = {
#     'version': 1,  # 保留字
#     'disable_existing_loggers': False,  # 禁用已经存在的logger实例
#     # 日志文件的格式
#     'formatters': {
#         # 详细的日志格式
#         'standard': {
#             # 'format': '[%(asctime)s][%(threadName)s:%(thread)d][task_id:%(name)s][%(filename)s:%(lineno)d]'
#             #           '[%(levelname)s][%(message)s]'
#             'format': '[%(levelname)s][%(asctime)s][%(pathname)s:%(lineno)d] %(message)s'
#         },
#         # 简单的日志格式
#         'simple': {
#             'format': '[%(levelname)s][%(asctime)s][%(filename)s:%(lineno)d]%(message)s'
#         },
#         # 定义一个特殊的日志格式
#         'collect': {
#             'format': '%(message)s'
#         }
#     },
#     # 过滤器
#     'filters': {
#         'require_debug_true': {
#             '()': 'django.utils.log.RequireDebugTrue',
#         },
#     },
#     # 处理器
#     'handlers': {
#         # 在终端打印
#         'console': {
#             'level': 'INFO',
#             # 'filters': ['require_debug_true'],  # 只有在Django debug为True时才在屏幕打印日志
#             'class': 'logging.StreamHandler',  #
#             'formatter': 'simple'
#         },
#         # 默认的
#         'default': {
#             'level': 'INFO',
#             'class': 'logging.handlers.RotatingFileHandler',  # 保存到文件，自动切
#             'filename': os.path.join('app.log'),  # 日志文件
#             'maxBytes': 1024 * 1024 * 500,  # 日志大小 500M
#             'backupCount': 3,  # 最多备份几个
#             'formatter': 'standard',
#             'encoding': 'utf-8',
#         },
#         # 专门用来记错误日志
#         'error': {
#             'level': 'ERROR',
#             'class': 'logging.handlers.RotatingFileHandler',  # 保存到文件，自动切
#             'filename': os.path.join('app_error.log'),  # 日志文件
#             'maxBytes': 1024 * 1024 * 500,  # 日志大小 50M
#             'backupCount': 5,
#             'formatter': 'standard',
#             'encoding': 'utf-8',
#         },
#         # 专门定义一个收集特定信息的日志
#         'collect': {
#             'level': 'INFO',
#             'class': 'logging.handlers.RotatingFileHandler',  # 保存到文件，自动切
#             'filename': os.path.join('app_collect.log'),
#             'maxBytes': 1024 * 1024 * 500,  # 日志大小 50M
#             'backupCount': 5,
#             'formatter': 'collect',
#             'encoding': "utf-8"
#         },
#         # celery 信息的日志
#         'celery': {
#             'level': 'INFO',
#             'class': 'logging.handlers.RotatingFileHandler',  # 保存到文件，自动切
#             'filename': os.path.join('app_celery.log'),
#             'maxBytes': 1024 * 1024 * 500,  # 日志大小 50M
#             'backupCount': 5,
#             'formatter': 'simple',
#             'encoding': "utf-8"
#         },
#     },
#     'loggers': {
#         # 默认的logger应用如下配置
#         '': {
#             'handlers': ['default', 'console', 'error'],  # 上线之后可以把'console'移除
#             'level': 'DEBUG',
#             'propagate': True,  # 向不向更高级别的logger传递
#         },
#         # 名为 'collect'的logger还单独处理
#         'collect': {
#             'handlers': ['console', 'collect'],
#             'level': 'INFO',
#         },
#         # 名为 'celery' 的logger还单独处理
#         'celery': {
#             'handlers': ['celery'],
#             'level': 'INFO',
#         }
#     },
# }