from IOT_Espresso import IOT_Espresso
import pigpio
import time


def main(time_delay=0.5):
    """[summary]
    """
    # spin up webserver
    machine = IOT_Espresso()
    pi = pigpio.pi()
    if not pi.connected:
        exit()
    try:
        # main control loop
        while True:
            machine.get_state()
            if brew == True:
                # wake up machine
                # check temp
                # update display
                while brew:
                    # check temp
                    # adjust machine heater
                    # update display
                    # update webserver
                    # 
                    pass
            machine.get_state()
            if brew == True:
                # wake up machine
                # check temp
                # update display
                while brew:
                    # check temp
                    # adjust machine heater
                    # update display
                    # update webserver
                    # 
                    pass
        time.sleep(time_delay)


        except KeyboardInterrupt:
            pass
        finally:
            # this is in case of failure
            # turn heater off
            machine.sleep()
            pi.stop()




if __name__ == "__main__":
    main()
