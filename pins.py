import time
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.cleanup()
GPIO.setwarnings(False)

class Pin():
  def __init__(self, pins=[], isInput=False):
    self.pins = {}
    if 'list' in str(type(pins)):
      for pin in pins:
        self.setup(pin, isInput)
    elif 'int' in str(type(pins)):
      self.setup(pins, isInput)
    print("Setup complete: {}".format(self.pins))

  def setup(self, pin=-1, isInput=False): #setup pin for output
    if isInput:
      GPIO.setup(pin, GPIO.IN)
      self.pins[pin] = GPIO.input(pin)
    else:
      GPIO.setup(pin, GPIO.OUT)
      GPIO.output(pin, GPIO.LOW)
      self.pins[pin] = False
  
  def onchange(self, callback, phase=0):
    print("Setup onchange event on pin {} (phase: {})".format(list(self.pins.keys())[0], phase))
    if phase == 1: event = GPIO.RISING
    elif phase == -1: event = GPIO.FALLING
    else: event = GPIO.BOTH
    GPIO.add_event_detect(int(list(self.pins.keys())[0]), event, callback=callback)

  def remove(self, pin):
    self.pins[pin] = False
    self.l(pin)

  def h(self, pins=[]): # set pin to high
    pins = self.pins if len(pins) <= 0 else pins
    for pin in pins:
      self.pins[pin] = True
      GPIO.output(pin, GPIO.HIGH)
  
  def l(self, pins=[]): # set pin to low
    pins = self.pins if len(pins) <= 0 else pins
    for pin in pins:
      self.pins[pin] = False
      GPIO.output(pin, GPIO.LOW)

  def toggle(self, pins=[]):
    pins = self.pins if len(pins) <= 0 else pins
    state = []
    for pin in pins:
      self.pins[pin] = not self.pins[pin]
      GPIO.output(pin, GPIO.HIGH if self.pins[pin] else GPIO.LOW)
      state.append(self.pins[pin])
    return state

  def read(self, pins=[]):
    pins = self.pins if len(pins) <= 0 else pins
    result = []
    for pin in pins:
      self.pins[pin] = GPIO.input(pin)
      result.append(self.pins[pin])
    return result