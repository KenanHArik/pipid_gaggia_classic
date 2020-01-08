import sys
import time
from luma.core.render import canvas
from luma.oled.device import ssd1306
from luma.core.interface.serial import i2c


class ssd1306():
    """Class to command and create basic display, configured and relevant for an espresso machine using the ssd1306
	"""

    def __init__(self, width=128, height=32, port=1, address=0x3C):
        self._sleep = None
        serial = i2c(port=port, address=address)
        self.display = ssd1306(serial, width=width, height=height)
        self.display.clear()
        self.display.sleep()

    def sleep(self):
        self.display.hide()
        self._sleep = True

    def wake(self):
        self.display.show()
        self._sleep = False

    def clear(self):
        self.display.clear()

    def standard_display(self, power_state, set_temp, current_temp):
        with canvas(self.display) as draw:
            l1 = f'Power {power_state}'
            l2 = f'Set Temp {str(set_temp)}'
            l3 = f'Current Temp {str(current_temp)}'
            draw.text((0, 0), l1, fill="white")
            draw.text((0, 11), l2, fill="white")
            draw.text((0, 22), l3, fill="white")