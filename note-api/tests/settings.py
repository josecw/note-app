from ctypes import cast
from email.policy import default
from decouple import config 

BASE_URL = config('BASE_URL')
USER1 = config("TEST_USER_1")
USER2 = config("TEST_USER_2")
PWD = config('CORRECT_PWD')
USE_TEST_DB = config('USE_TEST_DB', cast=bool, default=True)
