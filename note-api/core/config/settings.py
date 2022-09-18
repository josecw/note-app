from ctypes import cast
from email.policy import default
from decouple import config

db_host = config('DB_HOST')
db_user = config('DB_USER')
db_pass = config('DB_PASSWORD')
db_name = config('DB_NAME')
db_socket_timeout = config('DB_SOCKET_TIMEOUT', cast=int, default=2000)
db_connect_timeout = config('DB_CONNECT_TIMEOUT', cast=int, default=2000)

jwt_secret = config('JWT_SECRET')
jwt_algo = config('JWT_ALGO')
jwt_expiry = config('JWT_EXPIRY', cast=int, default=600)