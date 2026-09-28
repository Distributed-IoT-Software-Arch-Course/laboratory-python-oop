import time
from random import randint
from .sensor import Sensor


class AccelerometerSensor(Sensor):
    """ Accelerometer Sensor class, extends Sensor class """

    # Sensor Type
    SENSOR_TYPE: str = "iot.sensor.accelerometer"

    # Sensor Value Unit
    ACCELERATION_UNIT: str = "Acceleration"

    def __init__(self, device_id: str):
        """ Initialize the temperature sensor with a devices ID and an initial temperature """
        super().__init__(device_id, AccelerometerSensor.SENSOR_TYPE, "Acme Inc.")

        # Initialize the temperature measurement
        self.value = {
            'x_axis': 0,
            'y_axis': 0,
            'z_axis': 0,
        }

        # Set the timestamp of the last measurement in milliseconds
        self.timestamp = int(time.time() * 1000)

        # Set the Temperature Sensor Unit to Celsius
        self.unit = AccelerometerSensor.ACCELERATION_UNIT

    def update_measurement(self) -> None:
        """ Update the measurement of the sensor with a random increment """

        self.value['x_axis'] = randint(-400, 400)
        self.value['y_axis'] = randint(-400, 400)
        self.value['z_axis'] = randint(-400, 400)

        # Set the timestamp of the last measurement in milliseconds
        self.timestamp = int(time.time() * 1000)
