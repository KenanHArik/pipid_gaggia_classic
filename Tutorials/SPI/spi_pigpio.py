# sudo pigpiod
# sudo killall pigpiod
# ps aux | grep pigpiod

import pigpio


class max31865(object):
    """Class to communicate with from MAX31865 via SPI using pigpio library.
    Note: Pin numbers are BCM
	"""

    def __init__(self, channel=0, baud=500000, flags=1):
        self._pi = pigpio.pi()
        if not self._pi.connected:
            raise SystemError('Cannot connect to Pigpio Daemon. Verify it is running')
        self._bus = self._pi.spi_open(channel, baud, flags)


    def read_registers(self, registers):
        """Reads list of register locations, and give back values
        
        Args:
            h (int): pi.spi_open identifier return handle
            register (list): register location(s) to read from. i.e. [0x00, 0x01]
        
        Returns:
            (bytearray) : containing register values
        """
        registers.append(0x00)
        _, d = self._pi.spi_xfer(self._bus, registers)
        return d[1:]


    def write_register(self, register, data):
        """Writes data to register location
        
        Args:
            h (int): pi.spi_open identifier return handle
            register (hex): register location to write to. i.e. 0x80
            data (hex): byte data to write to register. i.e. 0xB2
        
        Returns:
            None
        """
        self._pi.spi_xfer(self._bus, [register, data])


    def close_SPI(self):
        """Safely closes SPI connection
        """
        self._pi.stop()
        print('Closing SPI connection to MAX31865')


    def set_config(self, v_bias=True, auto_conversion=True, one_shot=True, three_wire=True, clear_faults=True, fifty_hz=False):
        frame = bytearray()
        frame.append(int(v_bias))
        frame.append(int(auto_conversion))
        frame.append(int(three_wire))
        frame.append(0)
        frame.append(0)
        frame.append(int(clear_faults))
        frame.append(int(fifty_hz))
        self.write_register([0x80, frame])



        




# out = self.readRegisters(0, 8)
# conf_reg = out[0]
# print(f"config register byte: {conf_reg}")
# [rtd_msb, rtd_lsb] = [out[1], out[2]]
# rtd_ADC_Code = ((rtd_msb << 8) | rtd_lsb) >> 1
# temp_C = self.calcPT100Temp(rtd_ADC_Code)
# [hft_msb, hft_lsb] = [out[3], out[4]]
# hft = ((hft_msb << 8) | hft_lsb) >> 1
# print(f"high fault threshold: {hft}")
# [lft_msb, lft_lsb] = [out[5], out[6]]
# lft = ((lft_msb << 8) | lft_lsb) >> 1
# print(f"low fault threshold: {lft}")
# status = out[7]
# print(f"Status byte: {status}")
#         #
#         # 10 Mohm resistor is on breakout board to help
#         # detect cable faults
#         # bit 7: RTD High Threshold / cable fault open
#         # bit 6: RTD Low Threshold / cable fault short
#         # bit 5: REFIN- > 0.85 x VBias -> must be requested
#         # bit 4: REFIN- < 0.85 x VBias (FORCE- open) -> must be requested
#         # bit 3: RTDIN- < 0.85 x VBias (FORCE- open) -> must be requested
#         # bit 2: Overvoltage / undervoltage fault
#         # bits 1,0 don't care
#         if ((status & 0x80) == 1):
#             raise FaultError("High threshold limit (Cable fault/open)")
#         if ((status & 0x40) == 1):
#             raise FaultError("Low threshold limit (Cable fault/short)")
#         if ((status & 0x04) == 1):
#             raise FaultError("Overvoltage or Undervoltage Error")







# rx_data = read_registers(h, [0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07])

# # for b in rx_data:
# print(bin(b) for b in rx_data)

# # data = '11111111'
# # d = hex(int(data, 2))

# write_register(h, 0x80, 0x00)

# rx_data = read_registers(h, [0x00])
# for b in rx_data:
#     print(bin(b))

# pi.stop()
