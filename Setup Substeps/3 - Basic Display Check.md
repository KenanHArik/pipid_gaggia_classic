# Basic Check of the Display

The following code is included to test a basic sample of driving the display. The display used is a PiOLED I2C 0.91inch OLED Display Module, for Raspberry Pi 1/ Pi2/ Pi3/ Pi Zero. Its resolution is 128x32, and is driven by the I2C and compatible with the SSD1306 driver. The one I purchased was a generic one, but a specific Adafruit version can be found [here](https://github.com/adafruit/Adafruit_Python_SSD1306)

The library that was chosen to drive the display was [luma](https://luma-oled.readthedocs.io/en/latest/). I found its code to be clean and organized. A custom font is used here from Google Fonts, and included with the code reference to customize the size and look of the text.

If all the dependencies of the library have been installed, a quick check to make sure the display is working well is to run the code in a python console:

`source pipid/bin/activate` to start the python environment

```python
import os
from PIL import ImageFont
from luma.core.render import canvas
from luma.oled.device import ssd1306
from luma.core.interface.serial import i2c

serial = i2c(port=1, address=0x3C)
device = ssd1306(serial, width=128, height=32)

font_file = os.path.abspath("/home/pi/espresso/Mukta-Medium.ttf") # location must match where font file is
Font = ImageFont.truetype(font_file, 14)

with canvas(device) as draw:
    set_temp = 999
    current_temp = 999
    l1 = f"Set Temp: {str(set_temp)} °C"
    l2 = f"Current Temp: {str(current_temp)} °C"
    draw.text((0, 0), l1, font=Font, fill="white")
    draw.text((0, 13), l2, font=Font, fill="white")

# these can be run one at a time to understand their impact.
device.hide()
device.show()
device.clear()
```
