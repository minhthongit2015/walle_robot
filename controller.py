from pins import Pin

class Switch():
  """
  Base class for Module like Switch with on/off method
  """

  def __init__(self, pins):
    self.pin = Pin(pins)

  def on(self):
    self.pin.h()

  def off(self):
    self.pin.l()

  def toggle(self):
    return self.pin.toggle()[0]

class Lazer(Switch):
  def __init__(self, pin):
    Switch.__init__(self, pin)