import random
from datetime import datetime
import binascii
import uuid

def gen_id():
    """
    Generate random ID using random number and Epoch time
    """
    id = int(str(random.randint(1000,9999))+str(datetime.utcnow().strftime('%s')))

    return id



def gen_jwt_secret():

    secret = binascii.hexlify(uuid.uuid4().bytes).decode('utf-8')

    return secret