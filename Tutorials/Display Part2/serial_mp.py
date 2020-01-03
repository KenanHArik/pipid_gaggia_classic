"""
THIS LIBRARY FROM LUNA NEEDS TO BE MONEY PATCHED IF IT IS GOING TO BE TAILORED TO WORK WITH PIGPIO
https://github.com/rm-hull/luma.core/blob/master/luma/core/interface/serial.py


Encapsulates sending commands and data over a serial interface, whether that
is I²C, SPI or bit-banging GPIO.
"""

import errno

import luma.core.error
from luma.core import lib

__all__ = ["i2c", "spi", "bitbang", "ftdi_spi", "ftdi_i2c"]


class i2c(object):
    """
    Wrap an `I²C <https://en.wikipedia.org/wiki/I%C2%B2C>`_ (Inter-Integrated
    Circuit) interface to provide :py:func:`data` and :py:func:`command` methods.
    :param bus: A *smbus* implementation, if ``None`` is supplied (default),
        `smbus2 <https://pypi.python.org/pypi/smbus2>`_ is used.
        Typically this is overridden in tests, or if there is a specific
        reason why `pysmbus <https://pypi.python.org/pypi/pysmbus>`_ must be used
        over smbus2.
    :type bus:
    :param port: I²C port number, usually 0 or 1 (default).
    :type port: int
    :param address: I²C address, default: ``0x3C``.
    :type address: int
    :raises luma.core.error.DeviceAddressError: I2C device address is invalid.
    :raises luma.core.error.DeviceNotFoundError: I2C device could not be found.
    :raises luma.core.error.DevicePermissionError: Permission to access I2C device
        denied.
    .. note::
       1. Only one of ``bus`` OR ``port`` arguments should be supplied;
          if both are, then ``bus`` takes precedence.
       2. If ``bus`` is provided, there is an implicit expectation
          that it has already been opened.
    """

    def __init__(self, bus=None, port=1, address=0x3C):
        import smbus2
        self._cmd_mode = 0x00
        self._data_mode = 0x40

        try:
            self._addr = int(str(address), 0)
        except ValueError:
            raise luma.core.error.DeviceAddressError(
                'I2C device address invalid: {}'.format(address)
            )

        try:
            self._managed = bus is None
            self._i2c_msg_write = smbus2.i2c_msg.write if bus is None else None
            self._bus = bus or smbus2.SMBus(port)
        except (IOError, OSError) as e:
            if e.errno == errno.ENOENT:
                # FileNotFoundError
                raise luma.core.error.DeviceNotFoundError(
                    'I2C device not found: {}'.format(e.filename)
                )
            elif e.errno in [errno.EPERM, errno.EACCES]:
                # PermissionError
                raise luma.core.error.DevicePermissionError(
                    'I2C device permission denied: {}'.format(e.filename)
                )
            else:  # pragma: no cover
                raise

    def command(self, *cmd):
        """
        Sends a command or sequence of commands through to the I²C address
        - maximum allowed is 32 bytes in one go.
        :param cmd: A spread of commands.
        :type cmd: int
        :raises luma.core.error.DeviceNotFoundError: I2C device could not be found.
        """
        assert (len(cmd) <= 32)

        try:
            self._bus.write_i2c_block_data(
                self._addr, self._cmd_mode, list(cmd)
            )
        except (IOError, OSError) as e:
            if e.errno in [errno.EREMOTEIO, errno.EIO]:
                # I/O error
                raise luma.core.error.DeviceNotFoundError(
                    'I2C device not found on address: 0x{0:02X}'.format(
                        self._addr
                    )
                )
            else:  # pragma: no cover
                raise

    def data(self, data):
        """
        Sends a data byte or sequence of data bytes to the I²C address.
        If the bus is in managed mode backed by smbus2, the i2c_rdwr
        method will be used to avoid having to send in chunks.
        For SMBus devices the maximum allowed in one transaction is
        32 bytes, so if data is larger than this, it is sent in chunks.
        :param data: A data sequence.
        :type data: list, bytearray
        """

        # block size is the maximum data payload that will be tolerated.
        # The managed i2c will transfer blocks of upto 4K (using i2c_rdwr)
        # whereas we must use the default 32 byte block size when unmanaged
        if self._managed:
            block_size = 4096
            write = self._write_large_block
        else:
            block_size = 32
            write = self._write_block

        i = 0
        n = len(data)
        while i < n:
            write(list(data[i:i + block_size]))
            i += block_size

    def _write_block(self, data):
        assert len(data) <= 32
        self._bus.write_i2c_block_data(self._addr, self._data_mode, data)

    def _write_large_block(self, data):
        assert len(data) <= 4096
        self._bus.i2c_rdwr(
            self._i2c_msg_write(self._addr, [self._data_mode] + data)
        )

    def cleanup(self):
        """
        Clean up I²C resources
        """
        if self._managed:
            self._bus.close()