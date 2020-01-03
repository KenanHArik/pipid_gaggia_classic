"""Spidev library is ok, but pigpio is the library I would rather use.

Moving forward this is only for reference
"""

import spidev
import time
spi = spidev.SpiDev()
spi.open(0, 0)
spi.mode = 1
spi.cshigh = False
spi.max_speed_hz = 500000  # fastest seems to be 15600000 Hz on PiZero W
try:
    while True:
        # to_send = [0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07]
        r = spi.xfer2([0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07])
        # r = spi.readbytes(8)
        # r = spi.xfer2([0x00])
        print([bin(b) for b in r])
        # print(r)
        # print(bin(r[0]))
        # print(f'Recieved: 0x{binascii.hexlify(bytearray(r))}')
        time.sleep(1)
finally:
    spi.close()
# end

## below works for readout.
r = spi.xfer2([0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x00])
print([bin(b) for b in r[1:]])
# this also is able to write the register
r1 = spi.writebytes([0x80, 0xB2, 0x00])
print([bin(b) for b in r1])

spi.close()
# end