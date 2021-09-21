# Basic PWM Control

This goes over how to setup PWM control using pigpio library

**Note that pigpio only accepts BCM numbering in the code**, but physical pin is put for connection reference.

```python
import pigpio
import time

heater_pin = 13  #BCM 13, physical pin 33

pi = pigpio.pi()
pi.set_mode(heater_pin, pigpio.OUTPUT)

# PWM Options

pi.set_PWM_range(heater_pin, 100)  # now 0 = off,  100 = full dc
pi.set_PWM_frequency(heater_pin, 0)  # sets closest option to 0 Hz
pi.set_PWM_dutycycle(heater_pin, 0)  # turn heater off
print(f'Heater PWM Frequency is {pi.get_PWM_frequency(heater_pin)} and dutycycle is {pi.get_PWM_dutycycle(heater_pin)}')

pi.set_PWM_dutycycle(heater_pin, 100)  # update heater output to 100%
print(f'Heater PWM dutycycle is {pi.get_PWM_dutycycle(heater_pin)}')

pi.set_PWM_dutycycle(heater_pin, 50)  # update heater output to 50%
print(f'Heater PWM dutycycle is {pi.get_PWM_dutycycle(heater_pin)}')

pi.set_PWM_dutycycle(heater_pin, 0)  # turn heater off
print(f'Heater PWM dutycycle is {pi.get_PWM_dutycycle(heater_pin)}')


# In the end
pi.stop()
```
