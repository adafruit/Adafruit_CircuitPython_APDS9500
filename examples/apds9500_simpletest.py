import time
import board
import busio
import adafruit_apds9500
from adafruit_apds9500 import Gesture

i2c = busio.I2C(board.SCL, board.SDA)

apds = adafruit_apds9500.APDS9500(i2c)
while True:
    gesture_reading = apds.gestures
    if len(gesture_reading) == 0:
        continue
    for gesture in gesture_reading:
        print("\t", Gesture.string[gesture], "Gesture Detected")
    print("")
    time.sleep(.1)
