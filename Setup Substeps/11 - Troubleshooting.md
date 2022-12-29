## RTD fault

If there is ever any fault in the system with the MAX31865, the temperature reading will not work.

Instead, the return will be `RTD fault detected`

This fault is something that needs to be cleared, as the code is written to not clear any faults should they occur.

The script below should be run to just allow clearing of faults on the temp sensor (note: clear_faults=True)

```python
import max31865
import time
ts = max31865.max31865()
ts.set_config(
    v_bias=True,
    auto_conversion=False,
    one_shot=True,
    three_wire=True,
    clear_faults=True,
    fifty_hz=False
)
ts.wake()
while True:
    time.sleep(0.05)
    ts.read_temp(offset=2.0)
    
```

After the faults have been cleared from the register, and assuming no other issue, the temperature reading should return to normal.

To make it easy, a script of `temp_sense.py` is included to do just that.

## Shutting down the service

If there are any issues running the service, the status can be checked with the following

`systemctl status pi_espresso.service`

if ever the service needs to be started or stopped, it can be done with the following:

`systemctl stop pi_espresso.service`
`systemctl start pi_espresso.service`
