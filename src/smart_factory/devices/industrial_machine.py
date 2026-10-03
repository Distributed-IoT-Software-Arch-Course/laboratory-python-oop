from smart_factory.devices.accelerometer_sensor import AccelerometerSensor
from smart_factory.devices.device import Device
from smart_factory.devices.energy_sensor import EnergySensor
from smart_factory.devices.switch import Switch


class IndustrialMachine(Device):
    """ Industrial Machine class, extends Device Class and add new features, attributes and methods """

    # Device Type
    DEVICE_TYPE: str = "iot.industrial.machine"

    def __init__(self, device_id: str, accelerometer_sensor_number: int = 3):
        """ Initialize the device with the devices ID, type and manufacturer """
        super().__init__(device_id, IndustrialMachine.DEVICE_TYPE, "Acme Inc.")

        # Declare and initialize the Machine Energy Monitoring Sensor (assign an Id starting from the machine Id)
        self.energy_sensor = EnergySensor(f'{self.device_id}_energy_sensor')

        # Declare and initialize the Machine Energy Monitoring Switch Actuator
        # (assign an Id starting from the machine Id)
        self.switch = Switch(f'{self.device_id}_switch')

        # Declare and initialize the list to store machine's accelerometer sensors
        self.accelerometer_sensor_list = []

        # Initialize accelerometer sensors based of the parameter passed in the constructor (default = 3)
        for sensor_index in range(accelerometer_sensor_number):
            self.accelerometer_sensor_list.append(AccelerometerSensor(f'{self.device_id}_accelerometer_{sensor_index}'))

    def update_measurements(self) -> None:
        """Update all the measurements for the sensors associated to the Machine (energy and accelerometer)"""
        # Update Energy Sensor Measurements
        self.energy_sensor.update_measurement()

        # For each accelerometer sensor update the measurements
        for acc_sensor in self.accelerometer_sensor_list:
            acc_sensor.update_measurement()

    def get_description_dict(self) -> dict:
        """Return the description of the Industrial Machine as a dictionary
        This implementation is custom with respect to the default implementation in the Device class
        since it includes the descriptions of the accelerometer sensors, the energy sensor, the switch actuator
        and the machine information. The json.dumps() of the base get_json_description() is applied only once
        on the whole dictionary, so nested devices are serialized as JSON objects and not as JSON strings"""

        # Collect the description of each accelerometer sensor
        accelerometer_description_list = []
        for acc_sensor in self.accelerometer_sensor_list:
            accelerometer_description_list.append(acc_sensor.get_description_dict())

        return {
            "machine_id": self.device_id,
            "machine_type": self.device_type,
            "machine_manufacturer": self.device_manufacturer,
            "switch": self.switch.get_description_dict(),
            "energy_sensor": self.energy_sensor.get_description_dict(),
            "accelerometer_sensor_list": accelerometer_description_list
        }

    def get_measurement_dict(self) -> dict:
        """Return the last values of each device of the Industrial Machine as a dictionary
        This implementation is custom with respect to the default implementation in the Device class
        since it includes the measurements of the accelerometer sensors, the energy sensor, the switch actuator
        and the machine id. The json.dumps() of the base get_json_measurement() is applied only once
        on the whole dictionary, so nested devices are serialized as JSON objects and not as JSON strings"""

        # Collect the last measurement of each accelerometer sensor
        accelerometer_measurement_list = []
        for acc_sensor in self.accelerometer_sensor_list:
            accelerometer_measurement_list.append(acc_sensor.get_measurement_dict())

        return {
            "machine_id": self.device_id,
            "switch": self.switch.get_measurement_dict(),
            "energy_sensor": self.energy_sensor.get_measurement_dict(),
            "accelerometer_sensor_list": accelerometer_measurement_list
        }

    def start(self) -> None:
        """ Start machine operations setting the actuator to ON and updating a sample of available sensors"""

        # Turn ON the switch
        self.switch.invoke_action(Switch.ACTION_TYPE_SWITCH, Switch.STATUS_ON)

        # Update Machine Measurements
        self.update_measurements()

    def stop(self) -> None:
        """ Stop machine operations setting the actuator to OFF and updating a sample of available sensors"""

        # Update Sensor Measurements (energy and accelerometer)
        self.update_measurements()

        # Turn OFF the switch
        self.switch.invoke_action(Switch.ACTION_TYPE_SWITCH, Switch.STATUS_OFF)
