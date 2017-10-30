import time
from neopixel import *

LED_COUNT      = 16      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 5       # DMA channel to use for generating signal (try 5)
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53
LED_STRIP      = ws.WS2811_STRIP_GRB   # Strip type and colour ordering
        
class NeoPixel:
        strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, 0, LED_CHANNEL, LED_STRIP)
        
        def __init__(self, brightness=255):
                self.strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, brightness, LED_CHANNEL, LED_STRIP)
                # Intialize the library (must be called once before other functions).
                self.strip.begin()

        def turn_on(self, color, brightness):        
                for i in range(self.strip.numPixels()):
                        self.strip.setBrightness(brightness)
                        self.strip.setPixelColor(i, color)
                        self.strip.show()

        def turn_off(self):
                for i in range(self.strip.numPixels()):
                        self.strip.setPixelColor(i, 0)
                        self.strip.show()

        def fade_off(self, color):
                for c in range(255, -1, -3):
                        for i in range(self.strip.numPixels()):
                                self.strip.setPixelColor(i, color)
                                self.strip.setBrightness(c)
                                self.strip.show()              

        def fade_in(self, color):
                for c in range(0, 255, 3):
                        for i in range(self.strip.numPixels()):
                                self.strip.setPixelColor(i, color)
                                self.strip.setBrightness(c)
                                self.strip.show()

	def progress(self, color, progress):
		for i in range(int(progress)):
			self.strip.setPixelColor(i, color)
			self.strip.show()
			time.sleep(0.1)         

        def spin(self, color, brightness):
                for i in range(self.strip.numPixels()):
                        self.strip.setBrightness(brightness)
                        self.strip.setPixelColor(i, color)
                        self.strip.setPixelColor(i+1, self.dimColor(color))
                        time.sleep(70/1000.0)
                        self.strip.setPixelColor(i, 0)
                        self.strip.setPixelColor(i+1, 0)
                        

        def dimColor (self, color):
                """ Color is an 32-bit int that merges the values into one """
                return (((color&0xff0000)/3)&0xff0000) + (((color&0x00ff00)/3)&0x00ff00) + (((color&0x0000ff)/3)&0x0000ff)
                        
                
              
