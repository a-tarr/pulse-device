import requests
import json
import lights
import time
import threading
from neopixel import Color

url = 'https://iot-hackathon-api.azurewebsites.net/api/config'
config = None
global oldTime
oldTime = time.time()
newTime = None

shouldUpdate = False

def read_config():
    try:
        print('Calling API')
        response = requests.get(url)
        result = json.loads(response.text)
        # write to a local config file
        with open('/home/pi/pulse/iot.dash.device/config.json', 'w') as f:
            json.dumps(result, f)
        return result
    except requests.exceptions.RequestException as e:
        print('API request failed, grabbing from local config file')
        with open('/home/pi/pulse/iot.dash.device/config.json', 'r') as f:
            result = json.loads(f)
        return result

def poll_config():
    global shouldUpdate
    global config
    while True:
        print('Polling config')
        newConfig = read_config()
        #print(newConfig == config)
        if newConfig == config:
            shouldUpdate = False
        else:
            config = newConfig
            shouldUpdate = True
        time.sleep(5)

def display_status(status, color, delay, alert, rgb, brightness, progress = 0):
    if status == 0:
        if alert == 'toggle':
            lights.turn_on(1, Color(rgb[0], rgb[1], rgb[2]))
        elif alert == 'pulse':
            lights.pulse(delay, Color(rgb[0], rgb[1], rgb[2]))
        elif alert == 'blink':
            lights.blink(1, 1, Color(rgb[0], rgb[1], rgb[2]))
        elif alert == 'progress':
            lights.ledProgress(Color(rgb[0], rgb[1], rgb[2]), progress)
        else:
            # if an incorrect mode is passed through, simply turn the light on
            lights.turn_on(1, Color(rgb[0], rgb[1], rgb[2]))
 
def led_loop():
    while True:
        global shouldUpdate
        global config

        print(shouldUpdate)
        if shouldUpdate == True:
            color = config['color']
            alert = config['alert']
            delay = config['delay']
            rgb = (int(config['red']), int(config['green']), int(config['blue']))
            print(rgb)
            brightness = 255
            progress = 8
            if config['brightness'] != None:
	        brightness = config['brightness']
            if config['progress'] != None:  	    
		progress = config['progress']	        
        display_status(float(config['status']), color, delay, alert, rgb, brightness, progress)

def main():
    global config
    global shouldUpdate
    
    config = read_config()

    # set inital shouldUpdate for first request
    shouldUpdate = True
    
    ledThread = threading.Thread(name='ledThread', target=led_loop)
    pollThread = threading.Thread(name='pollThread', target=poll_config)
    
    ledThread.daemon = True
    pollThread.daemon = True
    ledThread.start()
    pollThread.start()

    # sleep main thread while child threas run
    while True:
        time.sleep(1)

if __name__ == '__main__':
    main()
