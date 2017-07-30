try:
    import serial  # pyserial
    import time
    import _thread
except ImportError:
    print("Some libraries are needed. Run \"pip3 install -r requirements.txt\" to install them.")
    quit()


class Uarm:
    """ Library for Uarm Swift Pro"""
    MAX_SPEED = 7000  # TODO findout max speed
    DEF_SPEED = 5000  # Default speed
    debug = False
    switch = False #  Flag for endeffector switch
    connected = False
    ack = False
    response = b'ok \r\n'

    def __init__(self, port, baudrate=115200, debug = False):
        self.debug = debug
        self.__index = 0
        self.__speed = self.DEF_SPEED
        try:
            self.ser = serial.Serial(port, baudrate, timeout=1)
        except:
            print("ERROR - Couldn't open {} port".format(port))
            quit()
        self.ser.flush()
        try:
            _thread.start_new_thread(self.serialcheckthread, ( 0.05,))
        except:
            print("Error: unable to start thread")
            quit()
        while True:
            if self.connected:
                break
            time.sleep(0.1)
        # self.waitfor('@5')  # Report event of power connection
        # time.sleep(1)
        # while self.ser.inWaiting() > 0:
        #     line = self.ser.readline()
        #     if (self.debug): print("DEBUG - ", line)
        #     if line.startswith('@5'.encode('utf-8')):
        #         print("@5")
        #     time.sleep(0.1)
        # time.sleep(1)
        print("uArm connected to {}".format(port))

        self.sendraw("M2213 V0")  # default buttons false

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

    # receive thread
    def serialcheckthread(self, delay):
        while True:
            if self.ser.inWaiting() > 0:
                self.response = self.ser.readline()
                if (self.debug): print("DEBUG - response: ", self.response)
                if self.response.startswith('@6'.encode('utf-8')):
                    self.switch = True
                if self.response.startswith('@5'.encode('utf-8')):
                    self.connected = True
                if self.response.startswith('ok'.encode('utf-8')):
                    self.ack = True
            else:
                time.sleep(delay)

    def sendraw(self, string):
        """ Send a raw GCode string """
        self.ack = False
        if type(string) != type(''):
            print("ERROR - argument {} must be a str.".format(type(string)))
            return
        string += '\n'
        self.ser.write(string.encode('utf-8'))
        if (self.debug): print("DEBUG - gcode sent: " + string, end='')
        while not self.ack:
            time.sleep(0.05)
        return True

    def move(self, x, y, z, speed=None):
        """ Move the arm to an absolute x, y, z position """
        if speed is not None:
            speed = self.speed
        self.sendraw("G0 X{} Y{} Z{} F{}".format(x, y, z, self.__speed))  # Relative displacement
        return True

    def moverel(self, x, y, z, speed=None):
        """ Move the arm to a relative x, y z position """
        if speed is not None:
            speed = self.speed
        self.sendraw("G2204 X{} Y{} Z{} F{}".format(x, y, z, self.__speed))  # Relative displacement
        return True

    def pause(self, seconds):
        milisec = int(seconds) * 1000
        # self.sendraw("G2004 P{}".format(milisec))  # Pause
        if (self.debug): print("DEBUG - pause {} seconds".format(seconds))
        time.sleep(seconds)
        return True

    def mode(self, mode):
        if mode != 0 and mode != 3:
            mode = 0
        self.sendraw("M2400 S{}".format(mode))  # Set mode 0 Normal 3 Universal holder
        return True

    def pumpswitch(self, dir):
        self.switch = False
        while not self.switch:
            self.moverel(0, 0, -1, speed=1500)
        #  self.sendraw('G2203') # Stop moving
        self.pump(dir)

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

    def wrist(self, angle):
        self.sendraw("G2202 N3 V{}".format(angle))
        return True

    # def waitfor(self, string):
    #     delay = 0.05
    #     for i in range(int(60/delay)):  # wait for 10 seconds
    #         if self.response.startswith(string.encode('utf-8')):
    #         #if self.response[0:2] == b'ok':
    #             break
    #         time.sleep(delay)
    #     else:
    #         print ("ERROR - No aknoledge receive from arm")
    #         self.close()
    #         quit()
    #     self.response=b'' # clear response

    def close(self):
        """ Close serial connexion and release the arm"""
        self.ser.close()  # close port

    # Private Methods ==================================================================

    def check_reachable(self, x, y, z):
        # TODO check if reachable
        return True
