import time
from pulse import NeoPixel

led = NeoPixel()

def turn_on(light_id, color):
    #print("state=on;id=" + str(light_id) + ";color=" + str(color))
    led.turn_on(color)


def turn_off(light_id):
    #print("status=off;id=" + str(light_id))
    led.turn_off()


def blink(light_id, delay, color):
    turn_on(light_id, color)
    time.sleep(float(delay))
    turn_off(light_id)
    time.sleep(float(delay))

def pulse(delay, color):
    led.fade_off(color)
    time.sleep(float(delay))
    led.fade_in(color)
    time.sleep(float(delay))

def ledProgress(color, progress):
    print(color)
    print(progress)
    led.progress(color, progress)

def main():
    blink(1, 0.5)


if __name__ == '__main__':
    main()
