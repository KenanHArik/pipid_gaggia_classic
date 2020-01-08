import time


class PID(object):
    """PID Controller
    """
    def __init__(self, set_point, P=0.2, I=0.01, D=0.01):
        self.SetPoint = set_point
        self.last_time = time.time()
        self.Kp = P
        self.Ki = I
        self.Kd = D
        self.PTerm = 0.0
        self.ITerm = 0.0
        self.DTerm = 0.0
        self.last_error = 0.0
        self.current_time = None
    def update(self, current_value):
        """Calculates PID value for given reference feedback
        
        https://en.wikipedia.org/wiki/PID_controller
        """
        error = self.SetPoint - current_value
        self.current_time = time.time()
        delta_time = self.current_time - self.last_time
        delta_error = error - self.last_error
        self.PTerm = self.Kp * error
        self.ITerm += error * delta_time
        self.DTerm = 0.0
        if delta_time > 0:
            self.DTerm = delta_error / delta_time
        # Record the last time and error for next calculation
        self.last_time = self.current_time
        self.last_error = error
        return self.PTerm + (self.Ki * self.ITerm) + (self.Kd * self.DTerm)