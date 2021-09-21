# Basic Check of the RTD Temperature Sensor

The following code is included to test a basic sample of driving the platinum RTD temperature sensor. The sensor is amplified using the MAX31865 board module. Similar module can be found on [Adafruit](https://www.adafruit.com/product/3328)

The module amplifies the resistance measurement, and the thermal sensor is a 3 wire setup with the same threading as the existing thermal switches in the Gaggia group head. After a measurement has been taken, math is used to form a fit of the data according to RTD physics and the parameters of the board resistors.

PiGPIO library is used to drive communication to the amplifier via SPI interface.

If all the dependencies of the library have been installed, a quick check to make sure the display is working well is to run the code in a python console:

```python
import pigpio
import time
import math

pi = pigpio.pi()
print(f'The PiGPIO service is online: {pi.connected}')
bus = pi.spi_open(spi_channel=0, baud=500000, spi_flags=1)
# Config Notes: [v_bias, auto_conversion, one_shot, three_wire, 0, 0, clear_faults, fifty_hz]
wake_config = [1, 1, 0, 1, 0, 0, 0, 0]
read_config = [1, 0, 1, 1, 0, 0, 0, 0]
sleep_config = [0, 0, 0, 1, 0, 0, 0, 0]

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

Or if you want, you can continuously report values using the code below

```python
import max31865
import time
ts = max31865.max31865()
ts.set_config(
    v_bias=True,
    auto_conversion=False,
    one_shot=True,
    three_wire=True,
    clear_faults=False,
    fifty_hz=False
)
ts.wake()
while True:
    time.sleep(0.05)
    ts.read_temp()
```
