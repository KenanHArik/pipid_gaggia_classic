


# import dependencies



class IOT_Espresso():
    def __init__(self):
        # define default initial attributes on state of machine
        # set default set temps
        # define hardware
        # spin up webserver
        # start in sleep mode
        pass

    # case of power off
    def go_to_sleep(self):
        pass


    # case of power on and brew temp
    def brew_mode(self):
        pass


    # case of power on and steam temp
    def steam_mode(self):
        pass


    # get temperature
    def get_temp(self):
        pass


    # main run loop
    def run(self):
        try:
            while True:
                #this is the main loop
                pass
        finally:
            # this is in case of failure
            # turn heater off


    # get feedback from pid on pwm
    def pid(self):
        pass

    def update_display(self):
        pass