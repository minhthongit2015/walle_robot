#!/usr/bin/python

import RPi.GPIO as GPIO
import time

def pir_detect():
  PIR = 4
  Lazer = 14
  GPIO.setwarnings(False)
  GPIO.setmode(GPIO.BCM)
  GPIO.setup(PIR, GPIO.IN)    # PIR sensor on pin 4
  GPIO.setup(Lazer, GPIO.OUT)  # Lazer on pin 14
  queue = []
  inMotion = False
  state = False
  while True:
    i = GPIO.input(4)
    queue.append(i)
    queue = noise_filter(queue[-30:])
    szQueue = ''.join(map(str,queue))
    if '111111' in szQueue[-6:]:
      if not inMotion:
        inMotion = True
        state = not state
        GPIO.output(Lazer, state)
        print("> Motion detected!")
    if '0000' in szQueue[-4:]:
      inMotion = False

    time.sleep(.2)

def noise_filter(queue):
  szQueue = ''.join(map(str,queue))
  szQueue = szQueue.replace('010', '00')
  szQueue = szQueue.replace('0110', '00')
  szQueue = szQueue.replace('01110', '00')
  szQueue = szQueue.replace('011110', '00')
  szQueue = szQueue.replace('0111110', '00')
  szQueue = szQueue.replace('101', '11')
  szQueue = szQueue.replace('1001', '11')
  return list(szQueue)

if __name__ == "__main__":
  pir_detect()