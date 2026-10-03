import time
from .sensor import Sensor
from random import random


class EnergySensor(Sensor):
    """ Energy Monitoring sensor class, extends Sensor class implementing the required methods of the base class"""

    # Sensor Type
    SENSOR_TYPE: str = "iot.sensor.energy"

    # Kilowatt-hour unit
    KILO_WATT_HOUR_UNIT: str = "kWh"

    def __init__(self, device_id: str, initial_kwh: int = 0):
        """ Initialize the energy sensor with a devices ID and an initial energy value in kWh """
        super().__init__(device_id, EnergySensor.SENSOR_TYPE, "Acme Inc.")

        # Initialize the energy measurement (kWh)
        self.value = initial_kwh

        # Set the timestamp of the last measurement in milliseconds
        self.timestamp = int(time.time() * 1000)

        # Set Unit of Sensor Value
        self.unit = EnergySensor.KILO_WATT_HOUR_UNIT

    def update_measurement(self) -> None:
        """ Update the Kwh measurement of the sensor with a random increment """

        # The consumed energy is a cumulative counter, so it can only increase (random increment between 1 and 3 kWh)
        self.value += 2 * (random() + 0.5)

        # Set the timestamp of the last measurement in milliseconds
        self.timestamp = int(time.time() * 1000)