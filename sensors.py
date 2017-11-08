from pins import Pin

class Sensor():
  """
  Base class for Modules like Sensor with read method
  """
  def __init__(self, pins, onchange=None):
    self.pin = Pin(pins, True)
    if onchange is not None:
      self.onchange(onchange)

  def __str__(self):
    return str(self.pin.read()[0])

  def value(self):
    return self.pin.read()[0]

  def onchange(self, callback):
    self.pin.onchange(callback)
    return 

class PIRSensor(Sensor):
  def __init__(self, pin, onchange=None):
    Sensor.__init__(self, pin, onchange)