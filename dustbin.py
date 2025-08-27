import RPi.GPIO as GPIO
import time
from beebotte import *

bclient = BBT("ssaVKYWDarGFgNETsCAC7j5j", "aluha6YL3kWio6qAa2t4UW8B696klE2q")
status_resource = Resource(bclient,'Dust','status')
count_resource = Resource (bclient, 'Dust','counter')

GPIO.setmode(GPIO.BOARD)
GPIO_TRIGGER = 12 
GPIO_ECHO = 18
servo_data_pin = 8 
standard_frequency = 50
lid_open = 2
lid_close = 6
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)
GPIO.setup(servo_data_pin, GPIO.OUT) 
p = GPIO.PWM(servo_data_pin,standard_frequency) 
p.start(lid_close)
how_many_times = 0
try:
 while True:
  GPIO.output(GPIO_TRIGGER, True)
  time.sleep(0.00001)
  GPIO.output(GPIO_TRIGGER, False)
  StartTime = time.time()
  StopTime = time.time()

  while GPIO.input(GPIO_ECHO) == 0:
   StartTime = time.time()

  while GPIO.input(GPIO_ECHO) == 1:
   StopTime = time.time()

  TimeElapsed = StopTime - StartTime
  distance = (TimeElapsed * 34300) / 2
  if distance< 15:
   how_many_times+=1
   print ("\nDistance from the object is ==> %.0f CM" % distance)
   status_resource.write('Dust Thrown')
   count_resource.write(how_many_times)
   print ("Opening the smart dustbin")
   print "Dust thrown",how_many_times,"times"
   p.ChangeDutyCycle(lid_open) 
   time.sleep(2)
   p.ChangeDutyCycle(lid_close) 
  else:
   print ("\nDistance from the object is ==> %.0f CM" % distance)
   print ("Lid of the dustbin is covered")
   time.sleep(0.5)
except Exception:
  print("\nError while writing data to cloud")
except KeyboardInterrupt:
  print("\nThe automatic dustbin program is terminated!\n")
  p.stop()
  GPIO.cleanup()
