# sudo pigpiod
# sudo killall pigpiod
# ps aux | grep pigpiod

import pigpio

pi = pigpio.pi()

if not pi.connected:
    print("Pi not connected")
    # exit(0)

channel = 0
baud = 500000
flags = 1  # SPI mode 1 is necessary

h = pi.spi_open(channel, baud, flags)


def read_registers(h, registers):
    """Reads list of register locations, and give back values
    
    Args:
        h (int): pi.spi_open identifier return handle
        register (list): register location(s) to read from. i.e. [0x00, 0x01]
    
    Returns:
        (bytearray) : containing register values
    """
    registers.append(0x00)
    _, d = pi.spi_xfer(h, registers)
    return d[1:]


def write_register(h, register, data):
    """Writes data to register location
    
    Args:
        h (int): pi.spi_open identifier return handle
        register (hex): register location to write to. i.e. 0x80
        data (hex): byte data to write to register. i.e. 0xB2
    
    Returns:
        None
    """
    pi.spi_xfer(h, [register, data])


rx_data = read_registers(h, [0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07])

# for b in rx_data:
print(bin(b) for b in rx_data)

# data = '11111111'
# d = hex(int(data, 2))

write_register(h, 0x80, 0x00)

rx_data = read_registers(h, [0x00])
for b in rx_data:
    print(bin(b))

pi.stop()
