# Basic Button

This is to get a button input working via GPIO sensing using PiGPIO

**Note that pigpio only accepts BCM numbering in the code**, but physical pin is put for connection reference.

```python
import pigpio
import time

button_in = 7  #BCM 7, physical pin 26

pi = pigpio.pi()
pi.set_mode(button_in, pigpio.INPUT)
pi.set_pull_up_down(button_in, pigpio.PUD_UP)

try:
    while True:
        print(pi.read(button_in)) # This will be 1 when released, 0 when pressed due to wiring to ground and pull up setting. 
        time.sleep(0.05)
except Exception as e:
    print(e)
finally:
    pi.stop()
```
