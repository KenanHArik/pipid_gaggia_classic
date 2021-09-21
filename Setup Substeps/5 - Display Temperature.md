# Displaying Measured Temperature

The following code is a quick check to make sure both they display and the temperature measurement play well together. Running the code below will result in a constant refresh of the display of the current measured temperature.

This setup will be used to fine tune the thermal sensor output by measuring known temperatures (ice bath / boiling water) to check accuracy.

```python
import os
from PIL import ImageFont
from luma.core.render import canvas
from luma.oled.device import ssd1306
from luma.core.interface.serial import i2c
import max31865
import time

serial = i2c(port=1, address=0x3C)
device = ssd1306(serial, width=128, height=32)

font_file = os.path.abspath("/home/pi/pipid_gaggia_classic/Mukta-Medium.ttf")
Font = ImageFont.truetype(font_file, 20)

ts = max31865.max31865()
ts.wake()
ts.set_config(
    v_bias=True,
    auto_conversion=False,
    one_shot=True,
    three_wire=True,
    clear_faults=False,
    fifty_hz=False
)
try:
    while True:
        with canvas(device) as draw:
            current_temp = ts.read_temp()
            l = f"Temp: {current_temp:.2f} °C"
            draw.text((0, 0), l, font=Font, fill="white")
        time.sleep(0.05)
except Exception as e:
    print(e)
finally:
    # clean up on break
    device.clear()
    ts.sleep()
    pi.stop()
```
