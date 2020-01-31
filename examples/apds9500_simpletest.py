import time
import board
import busio
import adafruit_apds9500
from adafruit_apds9500 import Gesture

i2c = busio.I2C(board.SCL, board.SDA)

ap = adafruit_apds9500.APDS9500(i2c)
while True:
    gesture_reading = ap.gesture
    for gesture in gesture_reading:
      print(Gesture.string[gesture], "Gesture Detected");
    time.sleep(.1)
