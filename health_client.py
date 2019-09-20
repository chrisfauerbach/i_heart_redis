import requests
import redis
import time


r = redis.Redis()
APP_NAME = "TESTABLE_HEALTH_APP"

while True:
    healthy = r.get(APP_NAME)
    if healthy:
        resp = requests.post('http://localhost:5000/send/email')
        print("Able to make a request!", resp.text)
        time.sleep(1)
    else:
        print("Not healthy.   Waiting until it comes back.")
        time.sleep(5)
