import redis
import time
from hashlib import sha1

r = redis.Redis()
CACHE_TIME_SECONDS = 300


def timed(func):
    def time_and_call(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print("Function call to {} took {} ms".format(str(func), str(end_time - start_time)))
        return result
    return time_and_call


def read_cached(func):
    def cache_and_call(*args, **kwargs):
        key_root_ = str(args) + str(kwargs)
        m = sha1()
        m.update(key_root_.encode('utf-8'))
        key = m.hexdigest()
        print("Key is: ",key)
        result = r.get(key)
        if not result:
            result = func(*args, **kwargs)
            if CACHE_TIME_SECONDS:
                r.setex(key, CACHE_TIME_SECONDS, result)
            else:
                r.set(key, result)
        return result
    return cache_and_call


@timed
@read_cached
def faster_method(order_id):
    time.sleep(.5)
    return "Your order id is: {}".format(order_id)

@timed
def slow_method(order_id):
    time.sleep(.5)
    return "Your order id is: {}".format(order_id)



if __name__ == "__main__":
    slow_method(1234)
    slow_method(1234)
    slow_method(1234)
    slow_method(1234)
    print("First call to faster_method")
    faster_method(1234)
    faster_method(1234)
    faster_method(1234)
    faster_method(1234)
