import redis
from _datetime import datetime
import uuid
import time
import random

r = redis.Redis(host='localhost', port=6379)
r.flushdb()

user_id = random.getrandbits(32)
print("upload your illustration link: ")
png_id = str(input())
link = uuid.uuid4()
link = str(link.hex)

current_dateTime = datetime.now()

def data(r,user_id, png_id, link):
    r.hset(f'{user_id}:{png_id}', 'linkk', link)
    return None

def put_data(r, user_id, png_id, link):
    key = f'{user_id}:{png_id}'
    r.expire(key, 86400)
    print(f"Your illustration with the following link: {link} will expire in 24 hours")
    print("left seconds till expiration: ", r.ttl(key))
    time.sleep(10)
    print("your link will expire in : ", r.ttl(key), " sec.")
    return None

data(r, user_id, png_id, link)
put_data(r,user_id, png_id, link)


