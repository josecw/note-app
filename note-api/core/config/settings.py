from ctypes import cast
from email.policy import default
from decouple import config

# App
HOST = config('HOST', default='0.0.0.0')
PORT = config('PORT', cast=int, default=8000)
DEBUG_MODE = config('DEBUG_MODE', cast=bool, default=False)
LOG_LEVEL = config('LOG_LEVEL', default='INFO')

# MongoDB
DB_HOST = config('DB_HOST')
DB_USER = config('DB_USER')
DB_PASS = config('DB_PASSWORD')
DB_NAME = config('DB_NAME')
DB_TIMEOUT = config('DB_TIMEOUT', cast=int, default=2000)


JWT_SECRET = config('JWT_SECRET')
JWT_ALGO = config('JWT_ALGO')
JWT_EXPIRY = config('JWT_EXPIRY', cast=int, default=600)

REDIS_HOST = config('REDIS_HOST')
REDIS_PASS = config('REDIS_PASSWORD')
REDIS_PORT = config('REDIS_PORT')