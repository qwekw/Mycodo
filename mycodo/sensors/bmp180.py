# coding=utf-8
from Adafruit_BMP import BMP085
import logging
import time
from .base_sensor import AbstractSensor

logger = logging.getLogger("mycodo.sensors.bmp180")


class BMP180Sensor(AbstractSensor):
    """
    A sensor support class that measures the BMP 180/085's humidity,
    temperature, and pressure, then calculates the altitude and dew point

    """

    def __init__(self, bus):
        super(BMP180Sensor, self).__init__()
        self.I2C_bus_number = bus
        self._altitude = 0.0
        self._pressure = 0
        self._temperature = 0.0

    def __repr__(self):
        """  Representation of object """
        return "<{cls}(temperature={temp})(pressure={press})" \
               "(altitude={alt})>".format(
                cls=type(self).__name__,
                alt="{0:.2f}".format(self._altitude),
                press=self._pressure,
                temp="{0:.2f}".format(self._temperature))

    def __str__(self):
        """ Return measurement information """
        return "Temperature: {temp}, Pressure: {press}, " \
               "Altitude: {alt}".format(
                alt="{0:.2f}".format(self._altitude),
                press="{0}".format(self._pressure),
                temp="{0:.2f}".format(self._temperature))

    def __iter__(self):  # must return an iterator
        """ SensorClass iterates through live measurement readings """
        return self

    def next(self):
        """ Get next measurement reading """
        if self.read():  # raised an error
            raise StopIteration  # required
        return dict(altitude=float('{0:.2f}'.format(self._altitude)),
                    pressure=int(self._pressure),
                    temperature=float('{0:.2f}'.format(self._temperature)))

    def info(self):
        conditions_measured = [
            ("Temperature", "temperature", "float", "0.00",
             self._temperature, self.temperature),
            ("Pressure", "pressure", "int", "0",
             self._pressure, self.pressure),
            ("Altitude", "altitude", "float", "0.00",
             self._altitude, self.altitude)
        ]
        return conditions_measured

    @property
    def altitude(self):
        """ BMP180/085 altitude in meters """
        if not self._altitude:  # update if needed
            self.read()
        return self._altitude

    @property
    def pressure(self):
        """ BME180/085 pressure in Pascals """
        if not self._pressure:  # update if needed
            self.read()
        return self._pressure

    @property
    def temperature(self):
        """ BMP180/085 temperature in Celsius """
        if not self._temperature:  # update if needed
            self.read()
        return self._temperature

    def get_measurement(self):
        """ Gets the measurement in units by reading the BMP180/085 """
        time.sleep(2)
        bmp = BMP085.BMP085(busnum=self.I2C_bus_number)
        return bmp.read_temperature(), bmp.read_pressure(), bmp.read_altitude()

    def read(self):
        """
        Takes a reading from the BMP180/085 and updates the self._humidity and
        self._temperature values

        :returns: None on success or 1 on error
        """
        try:
            self._temperature, self._pressure, self._altitude = self.get_measurement()
            return  # success - no errors
        except Exception as e:
            logger.exception(
                "{cls} raised an exception when taking a reading: "
                "{err}".format(cls=type(self).__name__, err=e))
        return 1
