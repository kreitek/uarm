#TODO check if serial is installed
import serial   # pyserial

class Uarm:
    """ Envia comandos GCode al brazo Uarm Swift Pro"""
    def __init__(self, puerto, baudrate = 57600):
        self.ser = serial.Serial(puerto, baudrate)
        self.__index = 0
        self._speed = 5000
    # getters setters
    # TODO check types and ranges
    def get_speed(self):
        """ Get the default speed """                 
        return self.__speed
    def set_speed(self, speed):
        """ Set the default speed """
        if speed < -0:
            raise ValueError("Only positive speed values")
        self.__speed = speed
        return self._speed
    def get_index(self):
        """ Get the actual index """  
        return self.__index
    def set_index(self, index):
        """ Set the actual index """          
        self.__index = index
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
            speed = self._speed
        mesage = "#{0} G0 X{1} Y{2} Z{3} F{4}\n".format(self.__index, x, y, z, speed)
        self.ser.write(mesage.encode('utf-8'))
        self.__index += 1
        #TODO esperar por respuest
        #TODO verificar respuesta
    def close(self):
        """ Cierra la conexion serie """
        self.ser.close()    # close port        



