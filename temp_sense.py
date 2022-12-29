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
