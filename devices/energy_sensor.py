import time
import json
from .sensor import Sensor
from random import random


class EnergySensor(Sensor):
    """ Energy Monitoring sensor class, extends Sensor class implementing the required methods of the base class"""

    # Sensor Type
    SENSOR_TYPE = "iot.sensor.energy"

    # Kilo-watt per hour unit
    KILO_WATT_HOUR_UNIT = "kWh"

    def __init__(self, device_id: str, initial_kwh: int = 0):
        """ Initialize the energy sensor with a devices ID and an initial humidity level """
        super().__init__(device_id, EnergySensor.SENSOR_TYPE, "Acme Inc.")

        # Initialize the humidity measurement
        self.value = initial_kwh

        # Set the timestamp of the last measurement in milliseconds
        self.timestamp = int(time.time() * 1000)

        # Set Unit of Sensor Value
        self.unit = EnergySensor.KILO_WATT_HOUR_UNIT

    def update_measurement(self):
        """ Update the Kwh measurement of the sensor with a random increment """

        # Update the measurement with a random increment or decrement
        is_increment_decrement = random() > 0.5

        if is_increment_decrement:
            self.value += 2 * (random() + 0.5)
        else:
            self.value -= 2 * (random() + 0.5)

        # Set the timestamp of the last measurement in milliseconds
        self.timestamp = int(time.time() * 1000)