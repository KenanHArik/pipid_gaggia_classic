"""libarary to run IOT espresso machine using raspberry pi

sudo pigpiod
if you ever need to: sudo killall pigpiod
to check on pigpio: ps aux | grep pigpiod

"""

# import dependencies
# from MAX31865_Driver import max31865
# import datetime
from SSD1306_Driver import ssd1306
from PID import PID
import pigpio
import time
import asyncio

class espresso_ctrl():
    ''' Class for Espresso Machine Control
    '''
    _temperature = 0
    _sleep = True
    _pump_out = 32  #BCM 32, physical pin 32
    _heater_out = 18  #BCM 18, physical pin 12
    _on_switch_in = 17  #BCM 17, physical pin 11
    _steam_switch_in = 27  #BCM 27, physical pin 13
    _brew_switch_in = 22  #BCM 22, physical pin 15
    _power_on = False
    _steam_on = False
    _pump_on = False
    _p = 0.2
    _i = 0.01
    _d = 0.01
    _brew_temp = 40
    _steam_temp = 100
    sleep = _sleep
    temperature = _temperature

    def __init__(self):
        # initialize gpio
        pi = pigpio.pi()
        if not pi.connected:
            exit()
        self.init_gpio()
        # establish link to temperature sensor
        # temp_sensor = max31865(channel=0, baud=500000, flags=1)  # sensor will start asleep
        # establish link to display
        display = ssd1306(width=128, height=32, port=1, address=0x3C)  # display will start asleep
        # get the physical switch states
        self.get_state()
        # start in sleep mode
        self.go_to_sleep()

    def init_gpio(self):
        pi.set_mode(self._pump_out, pigpio.OUTPUT)
        pi.set_mode(self._heater_out, pigpio.OUTPUT)
        pi.set_mode(self._on_switch_in, pigpio.INPUT)
        pi.set_mode(self._steam_switch_in, pigpio.INPUT)
        pi.set_mode(self._brew_switch_in, pigpio.INPUT)
        pi.set_pull_up_down(self._on_switch_in, pigpio.PUD_UP)  # Set as PUD_UP
        pi.set_pull_up_down(self._steam_switch_in, pigpio.PUD_UP)
        pi.set_pull_up_down(self._brew_switch_in, pigpio.PUD_UP)
        pi.set_PWM_range(self._pump_out, 100)  # now 0 = off,  100 = full dc
        pi.set_PWM_range(self._heater_out, 100)  # now 0 = off,  100 = full dc
        pi.set_PWM_frequency(self._pump_out, 0)  # sets closest option to 0 Hz
        pi.set_PWM_frequency(self._heater_out, 0)  # sets closest option to 0 Hz
        pi.set_PWM_dutycycle(self._pump_out, 0)  # turn pump off
        pi.set_PWM_dutycycle(self._heater_out, 0)  # turn heater off
        print(f'Pump PWM Frequency is {pi.get_PWM_frequency(self._pump_out)}')
        print(f'Heater PWM Frequency is {pi.get_PWM_frequency(self._heater_out)}')

        #TODO: need to set pwm parameters here perhaps

    def get_state(self):
        # use this to set the class state to what the switch configurations are set to
        self._power_on = bool(pi.read(self._on_switch_in)
        self._steam_on = bool(pi.read(self._steam_on)
        self._pump_on = bool(pi.read(self._pump_on)

    # case of power off
    def sleep(self):
        self._sleep = True
        # turn off display
        pass

    # get temperature
    def update_temp(self):
        self._temperature = temp_sensor.read_temp()

    # case of power on -  this is a blocking function right now :(
    def control_temp(self, set_temp):
        self._sleep = False  # Let known it is running
        power_on = True  #TODO: Remove when switch implimented
        # initialize PID control
        controller = PID(set_temp, _p, _i, _d)
        try:
            while power_on:
                self.update_temp()
                feedback = controller.update(self._temperature)
                if feedback <= 0:
                    dc = 0
                else:
                    # linear scale of duty cycle from feedback
                    dc = 100 * feedback / 10.0
                dc = 100 if dc > 100  # maximum duty cycle
                dc = 0 if dc < 5 # dead band
                pi.set_PWM_dutycycle(self._heater_out, dc)
        finally:
            pi.set_PWM_dutycycle(self._heater_out, 0)
    
    # async pump task
    async def pump_on(self, dc=100):
        try:
            while True:
                if _pump_on:
                    pi.set_PWM_dutycycle(self._pump_out, dc)
                    print('pump is on')
                else:
                    pi.set_PWM_dutycycle(self._pump_out, 0)
                await asyncio.sleep(0.1)
        except:
            print('Exception with pump_on func, shutting down GPIO')
            pi.stop()
    
    def duty_cycle_limits(self, feedback):
        if feedback <= 0:
            dc = 0
        else:
            # linear scale of duty cycle from feedback
            dc = 100 * feedback / 10.0
        dc = 100 if dc > 100  # maximum duty cycle
        dc = 0 if dc < 5 # dead band
        return dc


    async def heater_control(self):
        '''Asyncronous power control task
        '''
        try:
            while True:
                if self._power_on:
                    self._sleep = False
                    set_temp = self._steam_temp if self._steam_on else self._brew_temp
                    controller = PID(set_temp, self._p, self._i, self._d)
                    self.update_temp()
                    feedback = controller.update(self._temperature)
                    dc = self.duty_cycle_limits(feedback)
                    pi.set_PWM_dutycycle(self._heater_out, dc)  # update heater output
                    await asyncio.sleep(0.01)
                else:
                    self._sleep = True
                    pi.set_PWM_dutycycle(self._heater_out, 0)
                    await asyncio.sleep(100)
        except:
            print('Exception with power_control func, shutting down GPIO')
            pi.stop()
        finally:
            pass

