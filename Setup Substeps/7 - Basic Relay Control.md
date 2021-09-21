# Basic Relay Control

**Note that pigpio only accepts BCM numbering in the code**, but physical pin is put for connection reference.

```python
import pigpio
import time

relay_pin = 18  #BCM 18, physical pin 12

pi = pigpio.pi()
pi.set_mode(relay_pin, pigpio.OUTPUT)
pi.write(relay_pin,0)
print(f'The Relay is set to {pi.read(relay_pin)}')
time.sleep(1)
pi.write(relay_pin,1)
print(f'The Relay is set to {pi.read(relay_pin)}')

# In the end
pi.stop()
```
