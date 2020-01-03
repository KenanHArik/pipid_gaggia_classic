#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2014-18 Richard Hull and contributors
# See LICENSE.rst for details.
# PYTHON_ARGCOMPLETE_OK
"""
Use misc draw commands to create a simple image.

Ported from:
https://github.com/adafruit/Adafruit_Python_SSD1306/blob/master/examples/shapes.py
"""
import sys
import time
import datetime
from luma.core.render import canvas
from luma.oled.device import ssd1306
from luma.core.interface.serial import i2c


def main(device):
    sweep_len = 40
    range_up_down = list(range(1, sweep_len + 1)
                        ) + list(range(sweep_len, 0, -1))[1:-1]
    while True:
        for x in range_up_down:
            with canvas(device) as draw:
                power_state = 'on'
                set_temp = 40
                current_temp = 45
                l1 = f'Power {power_state}'
                l2 = f'Set Temp {str(set_temp)}'
                l3 = f'Current Temp {str(current_temp)}'
                draw.text((x, 0), l1, fill="white")
                draw.text((10, 12), l2, fill="white")
                draw.text((10, 24), l3, fill="white")


if __name__ == "__main__":
    try:
        serial = i2c(port=1, address=0x3C)
        device = ssd1306(serial, width=128, height=32)
        main(device)
    except KeyboardInterrupt:
        pass