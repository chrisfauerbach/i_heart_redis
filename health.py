import datetime
import time

import threading

import redis
from flask import Flask, jsonify
from random import randint

OK = 'OK'

app = Flask(__name__)
app.healthy = True

r = redis.Redis()

APP_NAME = "TESTABLE_HEALTH_APP"

def update_health(status):
    if status:
        r.setex(APP_NAME, 5, status)
    else:
        print(datetime.datetime.now().__str__() + " : HEALTH HAS FAILED")
        r.delete(APP_NAME)


class ThreadingTest(object):
    def __init__(self, interval=1):
        self.interval = interval
        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True
        thread.start()

    def run(self):
        while True:
            if randint(0,100) <= 1:
                #raise Exception("Faking a database error.")
                app.healthy = False
                update_health(None)
                time.sleep(30)
            else:
                update_health('Ok')
            time.sleep(self.interval)


tr = ThreadingTest()

class InvalidUsage(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv


def do_work(): 
    if not app.healthy:
        raise Exception("Faking a database error.")
    return {"status": "ok"}

@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

@app.route('/send/email', methods=['POST'])
def get_tasks():
    try:
        return_value = do_work()
        update_health(OK) 
        return jsonify(return_value)
    except:
        update_health(None)
        raise InvalidUsage("Database connection has failed.", status_code=500)


