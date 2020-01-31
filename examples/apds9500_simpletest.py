import board
import apds9500
import time
i2c = board.I2C()

ap = apds9500.APDS9500(i2c)

while True:
  result = ap.gesture_result

  if result & 0x20: print("gesture result = %s"%(result & 0x0F))
  flag_1 = ap.int_flag_1

  if(flag_1 & 0x01): print("UP event detected")
  if(flag_1 & 0x02): print("DOWN event detected")
  if(flag_1 & 0x04): print("LEFT event detected")
  if(flag_1 & 0x08): print("RIGHT event detected")
  if(flag_1 & 0x10): print("FORWARD event detected")
  if(flag_1 & 0x20): print("BACKWARD event detected")
  if(flag_1 & 0x40): print("CLOCKWISE event detected")


  time.sleep(.3)
