import time
import redis
import socket  # <--- NEW IMPORT
from flask import Flask

app = Flask(__name__)
cache = redis.Redis(host='redis', port=6379)

def get_hit_count():
    retries = 5
    while True:
        try:
            return cache.incr('hits')
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)

@app.route('/')
def hello():
    count = get_hit_count()
    # NEW: Get the container ID
    host_id = socket.gethostname()
    return 'Hello from Container: {}! I have been seen {} times.\n'.format(host_id, count)