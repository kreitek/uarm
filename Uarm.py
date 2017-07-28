try:
    import serial  # pyserial
    import time
except ImportError:
    print("Some libraries are needed. Run \"pip3 install -r requirements.txt\" to install them.")
    quit()


class Uarm:
    """ Library for Uarm Swift Pro"""
    MAX_SPEED = 7000  # TODO findout max speed
    DEF_SPEED = 5000  # Default speed

    def __init__(self, port, baudrate=115200):
        self.__index = 0
        self.__speed = self.DEF_SPEED
        try:
            self.ser = serial.Serial(port, baudrate)
        except:
            print("ERROR - Couldn't open {} port".format(port))
            quit()
        time.sleep(1)
        while self.ser.inWaiting() > 0:
            print("DEBUG - ", self.ser.readline())
            time.sleep(0.1)
        time.sleep(1)
        print("uArm connected to {}".format(port))

    # TODO check types and ranges
    @property
    def speed(self):
        return self.__speed

    @speed.setter
    def speed(self, value):
        _value = int(value)
        if _value <= 0:
            # raise ValueError("Only positive non zero speed values")
            print("WARNING - Only positive non zero speed values")
        elif _value > self.MAX_SPEED:
            print("WARNING - value exceeds max speed ", self.MAX_SPEED)
        else:
            self.__speed = _value

    @property
    def index(self):
        """ Get the actual index """
        return self.__index

    # Public Methods ==================================================================

    def sendraw(self, string):
        """ Send a raw GCode string """
        print("DEBUG - gcode sent: " + string)
        if type(string) != type(''):
            print("ERROR: argument {} must be a str.".format(type(string)))
            return
        string += '\n'
        self.ser.write(string.encode('utf-8'))
        self._check_response()

    def move(self, x, y, z, speed=None):
        """ Move the arm to an absolute x, y, z position """
        pos = self._getcartesian(x, y, z)
        if speed is not None:
            self.speed = speed
        self.sendraw("G2204 X{} Y{} Z{} F{}".format(pos[0], pos[1], pos[2], self.__speed))  # Relative displacement
        return True

    def moverel(self, x, y, z):
        """ Move the arm to a relative x, y z position """
        pos = self._getcartesian(x, y, z)
        self.sendraw("G2204 X{} Y{} Z{} F{}".format(pos[0], pos[1], pos[2], self.__speed))  # Relative displacement
        return True

    def pause(self, seconds):
        milisec = int(seconds) * 1000
        self.sendraw("G2004 P{}".format(milisec))  # Pause
        return True

    def mode(self, mode):
        if mode != 0 and mode != 3:
            mode = 0
        self.sendraw("M2400 S{}".format(mode))  # Set mode 0 Normal 3 Universal holder
        return True

    def pump(self, active):
        if active:
            var = 1
        else:
            var = 0
        self.sendraw("M2231 V{}".format(var))  # Pump on/off
        return True

    def gripper(self, active):
        if active:
            var = 1
        else:
            var = 0
        self.sendraw("M2232 V{}".format(var))  # Gripper open/close
        return True

    def close(self):
        """ Close serial connexion and release the arm"""
        self.ser.close()  # close port

    # Private Methods ==================================================================

    @staticmethod
    def _getcartesian(x, y, z):
        try:
            response = (int(x), int(y), int(z))
        except:
            response = (0, 0, 0)
        return response

    def check_reachable(self, x, y, z):
        # TODO check if reachable
        return True

    def _check_response(self):
        response = self.ser.readline()
        print("DEBUG - response: '{}'". format(response))
        # TODO check response
        return True
