#TODO check if serial is installed
import serial   # pyserial

class Uarm:

    """ Envia comandos GCode al brazo Uarm Swift Pro"""
    def __init__(self, puerto, baudrate = 57600):
        self.ser = serial.Serial(puerto, baudrate)
        self.__index = 0
        self.__speed = 5000

    # getters setters
    # TODO check types and ranges
    @property
    def speed(self):
        """ Get the default speed """
        return self.__speed

    @speed.setter
    def speed(self, value):
        """ Set the default speed """
        if value <= 0:
            raise ValueError("Only positive non zero speed values")
        self.__speed = value
        return self.__speed

    @property
    def index(self):
        """ Get the actual index """
        return self.__index

    # ===================
    def send(self, string):
        """ Manda cadena en crudo """
        if type(string) != type(str()):
            print("DEBUG: variable " + str(type(string)) + ". Se requiere str.")
            return
        self.ser.write(string.encode('utf-8'))
        #self.ser.write(b'blablabla\n')

    def move(self, x, y, z, speed = None):
        """ Mueve el brazo a una posicion absoluta """
        #protocol example "#25 G0 X180 Y0 Z150 F5000"
        #TODO comprobar float y otros tipos
        #TODO comprobar si el punto es alcanzable
        if speed == None:
            speed = self.__speed
        message = "#{0} G0 X{1} Y{2} Z{3} F{4}\n".format(self.__index, x, y, z, speed)
        self.ser.write(message.encode('utf-8'))
        self.__index += 1
        #TODO esperar por respuest
        #TODO verificar respuesta

    def close(self):
        """ Cierra la conexion serie """
        self.ser.close()    # close port
