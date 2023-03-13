# imports
import time
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode

keyboard = Keyboard(usb_hid.devices)

while True:
	keyboard.send(Keycode.COMMAND, Keycode.TAB)
