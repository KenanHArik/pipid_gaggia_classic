"""libarary to run IOT espresso machine using raspberry pi

sudo pigpiod
if you ever need to: sudo killall pigpiod
to check on pigpio: ps aux | grep pigpiod

"""

# import dependencies
from MAX31865_Driver import max31865
import datetime
from SSD1306_Driver import ssd1306
from PID import PID


class IOT_Espresso():
    def __init__(self, brew_temp, steam_temp):
        # define default initial attributes on state of machine
        self._sleep = True
        self.brew_temp = 42
        self.steam_temp = 50
        # establish temperature sensor properties
        temp_sensor = max31865(
            channel=0, baud=500000, flags=1
        )  # sensor will start asleep
        # display config

        # set GPIO Configs / PWM
        # start in sleep mode
        self.go_to_sleep()
        self.current_temp = None

    # case of power off
    def sleep(self):
        # gpio cleanup
        self._sleep = True
        pass

    # case of power on
    def wake(self):
        # gpio cleanup
        self._sleep = True
        pass

    # get temperature
    def get_temp(self):
        pass

    def run(self, set_temp=None):
        GPIO_on = True
        # initialize PID control
        controller = PID(set_temp, P=0.2, I=0.01, D=0.01, windup_guard=0.0)
        while GPIO_on:
            self.update_temp()
            feedback = controller.update(self.current_temp)
            if feedback <= 0:
                dc = 0
            else:
                # linear scale of duty cycle from feedback
                dc = 100 * feedback / 10.0
            dc = 100 if dc > 100  # maximum duty cycle
            dc = 0 if dc < 5 # dead band
            gpio_output(heater, dc)


            


        # if mode == 'steam':
        #     t = self.steam_temp
        # else:
        #     t = self.brew_temp
        #run control loop

    # get feedback from pid on pwm
    def calculate(self):
        pass

    # get feedback from pid on pwm
    def write_data(self):
        pass

    def heater():
        pass

    def get_state():
        # this is where state of switches is understood.
        pass


# if __name__ == "__main__":

#     max =
#     tempC = max.readTemp()
#     GPIO.cleanup()

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