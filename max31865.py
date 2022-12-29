import pigpio
import time


class max31865(object):
    """Class to communicate with from MAX31865 via SPI using pigpio library.
    Note: Pin number convention is BCM
	"""

    def __init__(self, channel=0, baud=500000, flags=1):
        self._pi = pigpio.pi()
        if not self._pi.connected:
            raise SystemError(
                'Cannot connect to Pigpio Daemon. Verify it is running'
            )
        self._bus = self._pi.spi_open(channel, baud, flags)
        self.sleep()  # start in sleep state
        self._sleep = True

    def read_all_registers(self):
        """Reads all register locations, and give back values
        
        """
        return self.read_registers(
            [0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07]
        )

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
        binary = [format(b, "08b") for b in d[1:]]  # response is shifted 1 byte
        return binary

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

    def set_config(
        self,
        v_bias=True,
        auto_conversion=False,
        one_shot=True,
        three_wire=True,
        clear_faults=True,
        fifty_hz=False
    ):
        args = [v_bias, auto_conversion, one_shot, three_wire, 0, 0, clear_faults, fifty_hz]
        config = [str(int(i)) for i in args]
        hexstring = hex(int(''.join(config), 2))
        print(config)
        print(hexstring)
        self.write_register(0x80, int(hexstring, 16))
        self._sleep = False if v_bias else True

    def sleep(self):
        self.set_config(
            v_bias=False,
            auto_conversion=False,
            one_shot=False,
            three_wire=True,
            clear_faults=False,
            fifty_hz=False
        )
        self._sleep = True
        print(
            'Max31865 is asleep, lower power state with no temperature readings'
        )

    def wake(self):
        self.set_config(
            v_bias=True,
            auto_conversion=True,
            one_shot=False,
            three_wire=True,
            clear_faults=False,
            fifty_hz=False
        )
        time.sleep(0.5)
        self._sleep = False
        print('Max is awake, ready for temperature readings')

    def shutdown(self):
        self._pi.stop()
        print('Closed SPI Communication to Max31865')

    def read_adc_code(self):
        if self._sleep:
            print('Wake temperature sensor before taking temperature reading')
            return None
        [rtd_msb, rtd_lsb] = self.read_registers([0x01, 0x02])
        fault = bool(int(rtd_lsb[-1]))
        if fault:
            print('RTD Fault detected...')
            return None
            # Uh oh this has not been developed, would need to dig into fault register...
        adc_code = (rtd_msb + rtd_lsb)[:-1]
        return int(adc_code, 2)

    def read_temp(self, offset=0):
        adc_code = self.read_adc_code()
        if adc_code is None:
            pass
            # handle error
        R_REF = 430.0  # Reference Resistor
        Res0 = 100.0  # PT100
        a = 0.00390830
        b = -0.000000577500
        Res_RTD = (adc_code * R_REF) / 32768.0  # PT100 Resistance
        R = Res_RTD / Res0
        temp_C = (-a + (a**2 - 4 * b + 4 * b * R)**0.5) / (2 * b)
        return temp_C + offset


# Example manual usage
# import max31865
# import time
# ts = max31865.max31865()

# ts.read_all()
# ts.set_config(
#     v_bias=True,
#     auto_conversion=False,
#     one_shot=True,
#     three_wire=True,
#     clear_faults=False,
#     fifty_hz=False
# )
# # ts.read_all_registers()
# ts.wake()
# # [rtd_msb, rtd_lsb] = ts.read_registers([0x01, 0x02])
# while True:
#     time.sleep(0.05)
#     ts.read_temp()