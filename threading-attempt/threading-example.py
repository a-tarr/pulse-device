import logging
import threading
import time
import requests
import json

logging.basicConfig(level=logging.DEBUG,
                    format='[%(levelname)s] (%(threadName)-10s) %(message)s',
                    )

x = None
url = 'https://iot-hackathon-api.azurewebsites.net/api/config'
result = None

def worker():
    while True:
        global result
        print(result)
        time.sleep(4)


def poll_api():
    while True:
        global result
        response = requests.get(url)
        result = json.loads(response.text)
        time.sleep(5)


t = threading.Thread(name='poll_api', target=poll_api)
w = threading.Thread(name='worker', target=worker)

w.daemon = True
t.daemon = True
w.start()
t.start()

while True:
    time.sleep(1)
