import json


class Device:
    """ Base class for devices """

    def __init__(self, device_id: str, device_type: str, device_manufacturer: str):
        """ Initialize the devices with a devices ID and a devices type """
        self.device_id = device_id
        self.device_type = device_type
        self.device_manufacturer = device_manufacturer

    def get_measurement_dict(self) -> dict:
        """ Returns a dictionary representation of the Device Status (e.g., the last measurement).
        This method should be overridden by subclasses """
        raise NotImplementedError("This method should be overridden by subclasses")

    def get_json_measurement(self) -> str:
        """ Returns a JSON representation of the Device Status (e.g., the last measurement) """
        return json.dumps(self.get_measurement_dict())

    def get_description_dict(self) -> dict:
        """ Returns a dictionary representation of the Device Description.
        Subclasses can override it to extend the description and compose it with other devices descriptions """

        return {
            "device_id": self.device_id,
            "device_type": self.device_type,
            "device_manufacturer": self.device_manufacturer
        }

    def get_json_description(self) -> str:
        """ Returns a JSON representation of the Device Description """
        return json.dumps(self.get_description_dict())
