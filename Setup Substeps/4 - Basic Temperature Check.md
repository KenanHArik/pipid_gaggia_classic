# Basic Check of the RTD Temperature Sensor

The following code is included to test a basic sample of driving the display. The display used is a PiOLED I2C 0.91inch OLED Display Module, for Raspberry Pi 1/ Pi2/ Pi3/ Pi Zero. Its resolution is 128x32, and is driven by the I2C and compatible with the SSD1306 driver. The one I purchased was a generic one, but a specific Adafruit version can be found [here](https://github.com/adafruit/Adafruit_Python_SSD1306)

The library that was chosen to drive the display was [luma](https://luma-oled.readthedocs.io/en/latest/). I found its code to be clean and organized. A custom font is used here from Google Fonts, and included with the code reference to customize the size and look of the text.

If all the dependencies of the library have been installed, a quick check to make sure the display is working well is to run the code in a python console:


```python
import pigpio
import time
import math

pi = pigpio.pi()
print(f'The PiGPIO service is online: {pi.connected}')
bus = pi.spi_open(spi_channel=0, baud=500000, spi_flags=1)
# Config Notes: v_bias, auto_conversion, one_shot, three_wire,clear_faults, fifty_hz
wake_config = [1, 1, 0, 1, 0, 0]
read_config = [1, 0, 1, 1, 0, 0]
sleep_config = [0, 0, 0, 1, 0, 0]

def set_config(pi, bus, config):
    x = [str(i) for i in config]
    hexstring = hex(int(''.join(x), 2))
    pi.spi_xfer(bus, [0x80, int(hexstring, 16)])

set_config(pi, bus, sleep_config)
time.sleep(0.5)
set_config(pi, bus, wake_config)

def read_registers(pi, bus, registers):
    registers.append(0x00)
    _, d = pi.spi_xfer(bus, registers)
    binary = [format(b, "08b") for b in d[1:]]  # response is shifted 1 byte
    return binary

# read_adc_code
set_config(pi, bus, read_config)
[rtd_msb, rtd_lsb] = read_registers(pi, bus, [0x01, 0x02])
fault = bool(int(rtd_lsb[-1]))
print(f'An RTD Fault is detected: {fault}')

adc_code = (rtd_msb + rtd_lsb)[:-1]
adc_value = int(adc_code, 2)
print(f'acd_value is {adc_value}')
R_REF = 430.0  # Reference Resistor
Res0 = 100.0  # PT100
a = 0.00390830
b = -0.000000577500
Res_RTD = (adc_value * R_REF) / 32768.0  # PT100 Resistance
R = Res_RTD / Res0
temp_C = (-a + math.sqrt(a**2 - 4 * b + 4 * b * R)) / (2 * b)

print(f'The measured temperature is: {temp_C}')


# in the end:
pi.stop()
        

```

```python
import max31865
import time
ts = max31865.max31865()
ts.read_all_registers()
ts.set_config(
    v_bias=True,
    auto_conversion=False,
    one_shot=True,
    three_wire=True,
    clear_faults=False,
    fifty_hz=False
)
# ts.read_all_registers()
ts.wake()
# [rtd_msb, rtd_lsb] = ts.read_registers([0x01, 0x02])
while True:
    time.sleep(0.05)
    ts.read_temp()

```