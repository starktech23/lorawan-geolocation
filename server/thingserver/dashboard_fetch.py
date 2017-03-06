"""
    ThingServer
    Use unofficial Things Connected dashboard API to get new packets
"""

from redis import StrictRedis
from redis.exceptions import ConnectionError

import time
import requests

import settings as s

def login(s):
    r = s.post('https://dashboard.thingsconnected.net/api/login', json={'email': s.LOGIN_EMAIL, 'password': s.LOGIN_PASSWORD})
    
    if r.status_code != 200:
        print "Unable to login."
    else:
        print "Logged in."

    return

def loop(s,r):

    r = s.get('https://dashboard.thingsconnected.net/api/devices/%s/messages/' % s.DEVICE)
    if r.status_code != 200:
        login(s)

    else:
        r.publish('dashboard_messages', r.text)

    time.sleep(s.FREQUENCY)


if __name__ == '__main__':
    s = requests.Session()
    
    r = StrictRedis(host=s.REDIS_HOST, port=s.REDIS_PORT)
    try:
        if self.r.ping():
            print "Redis connected."
    except ConnectionError:
        "Error: Redis server not available."
    
    login(s)
    
    while True:
        loop(s,r)