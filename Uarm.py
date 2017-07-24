try:
    import serial # pyserial
except ImportError:
    print("Some libraries are needed. run \"pip3 install -r requirements.txt\" to install them.")
    quit()

class Uarm:
    """ Library for Uarm Swift Pro"""
    MAX_SPEED = 7000 # Maximum speed allow by the arm
    DEF_SPEED = 5000 # Default speed

    def __init__(self, port, baudrate = 115200):
        self.ser = serial.Serial(port, baudrate)
        self.__index = 0
        self.speed = self.DEF_SPEED

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
            self.__speed = self.DEF_SPEED
        else:
            self.__speed = _value

    @property
    def index(self):
        """ Get the actual index """
        return self.__index

    # ===================
    def send(self, string):
        """ Send raw GCode string """
        if type(string) != type(str()):
            print("ERROR: variable " + str(type(string)) + " must be a str.")
            return
        self.ser.write(string.encode('utf-8'))
        #self.ser.write(b'blablabla\n')

    def move(self, x, y, z, speed = None):
        """ Move the arm to an absolute position """
        #protocol example "#25 G0 X180 Y0 Z150 F5000"
        _x = int(x)
        _y = int(y)
        _z = int(z)
        if (not self.check_reachable(_x, _y, _z)):
            print("ERROR - the point {0}, {1}, {2} is not reachable".format(_x, _y, _z))
            return False
        self.__index += 1
        if speed == None:
            speed = self.speed
        message = "#{0} G0 X{1} Y{2} Z{3} F{4}\n".format(self.__index, x, y, z, speed)
        self.ser.write(message.encode('utf-8'))
        #TODO wait for response
        #TODO check response
        return True

    def check_reachable(self, x, y, z):
        # TODO check if reachable
        return True

    def close(self):
        """ Close serial connexion """
        self.ser.close()    # close port
