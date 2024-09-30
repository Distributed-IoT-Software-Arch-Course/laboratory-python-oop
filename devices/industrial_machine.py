from devices.accelerometer_sensor import AccelerometerSensor
from devices.device import Device
from devices.energy_sensor import EnergySensor
from devices.switch import Switch


class IndustrialMachine(Device):
    """ Industrial Machine class, extends Device Class and add new features, attributes and methods """

    # Device Type
    DEVICE_TYPE = "iot.industrial.machine"

    def __init__(self, device_id: str, accelerometer_sensor_number: int = 3):
        """ Initialize the device with the devices ID, type and manufacturer """
        super().__init__(device_id, IndustrialMachine.DEVICE_TYPE, "Acme Inc.")

        # Declare and initialize the Machine Energy Monitoring Sensor (assign an Id starting from the machine Id)
        self.energy_sensor = EnergySensor(f'{self.device_id}_energy_sensor')

        # Declare and initialize the Machine Energy Monitoring Switch Actuator (assign an Id starting from the machine Id)
        self.switch = Switch(f'{self.device_id}_switch')

        # Declare and initialize the list to store machine's accelerometer sensors
        self.accelerometer_sensor_list = []

        # Initialize accelerometer sensors based of the parameter passed in the constructor (default = 3)
        for sensor_index in range(accelerometer_sensor_number):
            self.accelerometer_sensor_list.append(AccelerometerSensor(f'{self.device_id}_switch_{sensor_index}'))

    def update_measurements(self):
        """Update all the measurements for the sensors associated to the Machine (energy and accelerometer)"""
        # Update Energy Sensor Measurements
        self.energy_sensor.update_measurement()

        # For each accelerometer sensor update the measurements
        for acc_sensor in self.accelerometer_sensor_list:
            acc_sensor.update_measurement()

    def get_json_description(self):
        """Return the list of last values for each device of the Industrial Machine
        This implementation is custom with respect to the default implementation in the Device class
        since it includes the list of accelerometer sensors, energy sensor, actuators and the machine information"""

        accelerometer_description_list = []

        # For each accelerometer sensor update the device descriptions and measurements
        for acc_sensor in self.accelerometer_sensor_list:
            accelerometer_description_list.append(acc_sensor.get_json_description())

        return {
            "machine_id": self.device_id,
            "machine_type": self.device_type,
            "machine_manufacturer": self.device_manufacturer,
            "switch_id": self.switch.get_json_description(),
            "energy_sensor_id": self.energy_sensor.get_json_description(),
            "accelerometer_sensor_id_list": accelerometer_description_list
        }

    def get_json_measurement(self):
        """Return the list of last values for each device of the Industrial Machine
        This implementation is custom with respect to the default implementation in base class
        since it includes the measurements of accelerometer sensors, energy sensor, actuators and the machine information"""

        accelerometer_description_list = []

        # For each accelerometer sensor update the device descriptions and measurements
        for acc_sensor in self.accelerometer_sensor_list:
            accelerometer_description_list.append(acc_sensor.get_json_measurement())

        return {
            "machine_id": self.device_id,
            "switch": self.switch.get_json_measurement(),
            "energy_sensor": self.energy_sensor.get_json_measurement(),
            "accelerometer_sensor_list": accelerometer_description_list
        }

    def start(self):
        """ Start machine operations setting the actuator to ON and updating a sample of available sensors"""

        # Turn ON the switch
        self.switch.invoke_action(Switch.ACTION_TYPE_SWITCH, Switch.STATUS_ON)

        # Update Machine Measurements
        self.update_measurements()


    def stop(self):
        """ Stop machine operations setting the actuator to OFF and updating a sample of available sensors"""

        # Update Sensor Measurements (energy and accelerometer)
        self.update_measurements()

        # Turn OFF the switch
        self.switch.invoke_action(Switch.ACTION_TYPE_SWITCH, Switch.STATUS_OFF)
