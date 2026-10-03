from .device import Device


class Sensor(Device):
    """ Base class for sensors """

    def __init__(self, device_id: str, device_type: str, device_manufacturer: str):
        """ Initialize the sensor with a devices ID, a devices type """
        super().__init__(device_id, device_type, device_manufacturer)

        # Initialize the measurement value to None and the timestamp
        # Subclasses should override the update_measurement method to set the value
        self.value = None

        # Set the timestamp to None, subclasses should set the timestamp when updating the measurement
        self.timestamp = None

        # Set the Unit associated to sensor measurements
        self.unit = None

    def update_measurement(self) -> None:
        """ Update the measurement of the sensor, this method should be overridden by subclasses """
        raise NotImplementedError("This method should be overridden by subclasses")

    def get_measurement_dict(self) -> dict:
        """ Returns a dictionary representation of the Sensor Status (e.g., the last measurement) """
        return {
            "device_id": self.device_id,
            "value": self.value,
            "unit": self.unit,
            "timestamp": self.timestamp
        }