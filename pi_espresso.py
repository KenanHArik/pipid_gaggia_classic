#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import time
import pigpio
import max31865
from PIL import ImageFont
from simple_pid import PID
from luma.core.render import canvas
from luma.oled.device import ssd1306
from luma.core.interface.serial import i2c

#######################
# Functions
#######################


def wake_machine(display, ts, pi):
    # wake display
    display.show()
    # wake temperature sensor
    ts.wake()
    # wake heater SSR
    pi.set_PWM_dutycycle(heater_pin, 0)  # turn heater to 0
    print("The machine is getting ready...")


def sleep_machine(display, ts, pi):
    # sleep display
    display.clear()
    display.hide()
    # sleep temperature sensor
    ts.sleep()
    # sleep heater SSR
    pi.set_PWM_dutycycle(heater_pin, 0)  # turn heater off
    print("The machine is sleeping...")


def update_display(set_temp, current_temp):
    with canvas(display) as draw:
        l1 = f"Temp: {current_temp:.1f}°C"
        l2 = f"Set: {set_temp:.1f}°C, at {pi.get_PWM_dutycycle(heater_pin)}%"
        draw.text((0, 0), l1, font=Font, fill="white")
        draw.text((0, 13), l2, font=Font, fill="white")


def sleep_check(wake_pin, coffee_time):
    if pi.read(wake_pin) == 0:
        return not coffee_time
    else:
        return coffee_time


def toggle_sleep_mode(gpio, level, tick):
    global coffee_time
    coffee_time = not coffee_time


def update_SSR(heater_pin, pid_calc):
    multiple = 2
    duty_cycle = multiple * round(pid_calc / multiple)
    pi.set_PWM_dutycycle(heater_pin, duty_cycle)  # turn heater off
    # print(f'Heater PWM dutycycle is {pi.get_PWM_dutycycle(heater_pin)}')


#######################
# Parameters
#######################

# global coffee_time
coffee_time = False
brew_mode = True
sleeping = True
brew_temp = 93
steam_temp = 145
offset_temp = 2.0  # offset adjustment to temp sensor

#######################
# Initialize Setup
#######################

# Initiate PID
P = 17.5
I = 0.1
D = 25.0
pid = PID(P, I, D)
pid.sample_time = 0.25
pid.output_limits = (0, 100)
pid.setpoint = brew_temp
pid.auto_mode = True

# Initiate RTD Temp Sensor and put it to sleep
ts = max31865.max31865()
ts.set_config(
    v_bias=True,
    auto_conversion=False,
    one_shot=True,
    three_wire=True,
    clear_faults=False,
    fifty_hz=False,
)

# Initiate Display
serial = i2c(port=1, address=0x3C)
display = ssd1306(serial, width=128, height=32)
font_file = os.path.abspath(
    "/home/pi/espresso/Mukta-Medium.ttf"
)  # location must match where font file is
Font = ImageFont.truetype(font_file, 14)

# Initiate the SSR, set duty cycle to 0
pi = pigpio.pi()
heater_pin = 13  # BCM 13, physical pin 33
pi.set_mode(heater_pin, pigpio.OUTPUT)
pi.set_PWM_range(heater_pin, 100)  # now 0 = off,  100 = full dc
pi.set_PWM_frequency(heater_pin, 0)  # sets closest option to 0 Hz
pi.set_PWM_dutycycle(heater_pin, 0)  # turn heater off

# Initiate the wake / sleep button
wake_pin = 7  # BCM 7, physical pin 26
pi.set_mode(wake_pin, pigpio.INPUT)
pi.set_pull_up_down(wake_pin, pigpio.PUD_UP)
pi.set_glitch_filter(wake_pin, 100)
pi.callback(wake_pin, pigpio.RISING_EDGE, toggle_sleep_mode)

# Initiate the brew / steam toggle
brew_pin = 21  # BCM 21, physical pin 40
pi.set_mode(brew_pin, pigpio.INPUT)
pi.set_pull_up_down(brew_pin, pigpio.PUD_UP)

# Sleep the machine
sleep_machine(display, ts, pi)

#######################
# Main Loop
#######################

if __name__ == "__main__":
    while True:  # Primary loop
        try:
            while coffee_time:
                if sleeping:
                    wake_machine(display, ts, pi)
                    sleeping = False
                    print("Machine is working....")
                if brew_mode == True:
                    set_temp = brew_temp
                else:
                    set_temp = steam_temp
                current_temp = ts.read_temp(offset=offset_temp)
                update_display(set_temp, current_temp)
                brew_mode = bool(pi.read(brew_pin))
                pid.setpoint = set_temp
                pid_calc = pid(current_temp)
                update_SSR(heater_pin, pid_calc)
                p, i, d = pid.components  # The separate terms are now in p, i, d
                print(f"P: {p} I: {i} D: {d}")
                time.sleep(0.1)
            else:
                if not sleeping:
                    sleep_machine(display, ts, pi)
                    sleeping = True
                print("Machine is sleeping....")
                time.sleep(2)
        except Exception as e:
            print(e)
            continue
        finally:
            if not sleeping:
                sleep_machine(display, ts, pi)
                sleeping = True
            print("Machine is sleeping....")
