# Laboratory - Python Object-Oriented Programming - Industrial Use Case

This is a Laboratory is dedicated to the analysis and implementation for Python Object Oriented Programming (OOP) concepts.
The proposed modeling is associated to a Industry 4.0 Scenario with various Industrial IoT devices: 

- `Energy Monitoring Sensors` sensors to read the energy consumed by a specific machine
- `Accelerometer Sensors` to detect movements variation of a target machine
- `Switch` (ON/OFF) an actuator to start of stop a specific operating/working of a target machine

These sensors and actuators are associated to an Industrial `Machine` that has:

- _1_ x `Energy Monitoring Sensors`
- _n_ x `Accelerometer Sensors`
- _1_ x `Switch`

Each Machine exposes and implements also the following methods:

- `start()`: to start machine operations by changing the state of the associated actuator
- `stop()`: to stop machine operations by changing the state of the associated actuator
- `update_measurements()`: to update all the measurements associated to both energy monitoring and accelerometers sensors

Machine can be then associated to a `ProductionLine` in charge of handling multiple Machines at the same time and exposing 
the following methods:

- `add_industrial_machine(machine)`: Allows to add a machine to the Production Line
- `remove_industrial_machine(machine)`: Allows to remove a machine to the Production Line
- `get_machine(machine_id)`: Retrieves an existing machine from the Production Line
- `startAll()`: to start all the managed machines calling the associated `start()` method
- `stopAll()`: to stop all the managed machines calling the associated `stop()` method
- `update_measurements()`: to update all the measurements associated every machines managed by the Production Line

The Laboratory will involve designing data structure, identify classes (and creating them in Python to model these devices, 
a central system to collect and manage data.

**Note:** The scenario is simplified without any kind of communication, and everything is running within the same process. 

## Base Classes

The basic classes (taken from the OOP Playground [Link](https://github.com/Distributed-IoT-Software-Arch-Course/python-oop-playground)) are:

- `Device`: Base class for all devices defining the following attributes for all the devices such as sensors and actuators subclasses:
  - `device_id`: Id of the device
  - `device_type`: Type of the device
  - `device_manufacturer`: Manufacturer of the device
- `Sensor`: Base class for all sensors extending `Device` class and adding: 
  - Methods:
    - `update_measurement()`: update the sensor value. The default implementation throws a `NotImplementedError` exception and the subclasses must implement it. 
    - `get_json_description()`: get the description of the sensor in JSON format. The default implementation throws a `NotImplementedError` exception and the subclasses must implement it.
  - Attributes:
    - `value`: associated to the current sensor value
    - `unit`: mapping the unit associated to the physical measurement type
    - `timestamp` of the last sample in milliseconds
- `Actuator`: Base class for all actuators extending `Device` class and adding:
  - Methods:
    - `invoke_action(action_type, payload)`: method and the `get_json_description` method to get the description of the sensor in JSON format
    - `get_json_description()`: get the description of the sensor in JSON format. The default implementation throws a `NotImplementedError` exception and the subclasses must implement it.
  - Attributes:
    -  `status`: associated to the current status of the actuator
    - `timestamp` of the last action in milliseconds

### Devices Folder & Base Classes

Create a `devices` folder and a new file named `__init__.py` to handle classes as a module and properly import them in other 
folder and files within the project.

#### Device Class

In the folder `devices` create a new file named `device.py` where we are going to create the `Device` class 
with the following code:

```python
class Device:
    """ Base class for devices """

    def __init__(self, device_id, device_type, device_manufacturer):
        """ Initialize the devices with a devices ID and a devices type """
        self.device_id = device_id
        self.device_type = device_type
        self.device_manufacturer = device_manufacturer
```

#### Sensor Class

In the folder `devices` create a new file named `sensor.py` where we are going to create the `Sensor` class 
with the following code:

```python
from .device import Device


class Sensor(Device):
    """ Base class for sensors """

    def __init__(self, device_id, device_type, device_manufacturer):
        """ Initialize the sensor with a devices ID, a devices type """
        super().__init__(device_id, device_type, device_manufacturer)

        # Initialize the measurement value to None and the timestamp
        # Subclasses should override the update_measurement method to set the value
        self.value = None

        # Set the timestamp to None, subclasses should set the timestamp when updating the measurement
        self.timestamp = None

        # Set the Unit associated to sensor measurements
        self.unit = None

    def update_measurement(self):
        """ Update the measurement of the sensor, this method should be overridden by subclasses """
        raise NotImplementedError("This method should be overridden by subclasses")

    def get_json_description(self):
        """ Returns a JSON representation of the Sensor, this method should be overridden by subclasses """
        raise NotImplementedError("This method should be overridden by subclasses")
```

#### Actuator Class

In the folder `devices` create a new file named `actuator.py` where we are going to create the `Actuator` class 
with the following code:

```python
from .device import Device


class Actuator(Device):
    """ Base class for actuators """

    def __init__(self, device_id, device_type, device_manufacturer):
        """ Initialize the actuator with a devices ID and a devices type """
        super().__init__(device_id, device_type, device_manufacturer)

        # Initialize the status to None, subclasses should set the status when needed
        self.status = "off"

        # Set the timestamp to None, subclasses should set the timestamp when updating the status
        self.timestamp = None

    def invoke_action(self, action_type, payload):
        """ Invoke an action on the actuator """
        raise NotImplementedError("This method should be overridden by subclasses")

    def get_json_description(self):
        """ Returns a JSON representation of the actuator,this method should be overridden by subclasses """
        raise NotImplementedError("This method should be overridden by subclasses")
```

### Sensor Classes

#### Energy Monitoring Sensor

In the folder `devices` create a new file named `energy_sensor.py` where we are going to create the `Actuator` class 
with the following code to define the class structure and constructor method:

```python
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

    def __init__(self, device_id, initial_kwh=0):
        """ Initialize the energy sensor with a devices ID and an initial humidity level """
        super().__init__(device_id, EnergySensor.SENSOR_TYPE, "Acme Inc.")

        # Initialize the humidity measurement
        self.value = initial_kwh

        # Set the timestamp of the last measurement in milliseconds
        self.timestamp = int(time.time() * 1000)

        # Set Unit of Sensor Value
        self.unit = EnergySensor.KILO_WATT_HOUR_UNIT
```

The next step is to add the `update_measurement` method to model the generation of new energy samples:

```python
def update_measurement(self):
    """ Update the Kwh measurement of the sensor with a random increment """

    # Update the measurement with a random increment or decrement
    is_increment_decrement = random() > 0.5

    if is_increment_decrement:
        self.value += 2 * (random() + 0.5)
    else:
        self.value -= 2 * (random() + 0.5)

    # Set the timestamp of the last measurement in milliseconds
    self.line_update_timestamp = int(time.time() * 1000)
```

Final step is to define the `get_json_description` in order to define how the sensor will be described in JSON with available 
attributes and data.

```python
def get_json_description(self):
    """ Returns a JSON representation of the humidity sensor """
    result_dict = {
        "device_id": self.device_id,
        "device_type": self.device_type,
        "device_manufacturer": self.device_manufacturer,
        "value": self.value,
        "unit": self.unit,
        "timestamp": self.line_update_timestamp
    }

    return json.dumps(result_dict)
```

#### Accelerometer Sensor

In the folder `devices` create a new file named `accelerometer_sensor.py` where we are going to create the `Actuator` class 
with the following code to define the class structure and constructor method:

```python
import time
import json
from random import randint
from .sensor import Sensor


class AccelerometerSensor(Sensor):
    """ Accelerometer Sensor class, extends Sensor class implementing get_status method """

    # Sensor Type
    SENSOR_TYPE = "iot.sensor.accelerometer"

    # Sensor Value Unit
    ACCELERATION_UNIT = "Acceleration"

    def __init__(self, device_id):
        """ Initialize the temperature sensor with a devices ID and an initial temperature """
        super().__init__(device_id, AccelerometerSensor.SENSOR_TYPE, "Acme Inc.")

        # Initialize the temperature measurement
        self.value = {
            "x_axis": 0,
            "y_axis": 0,
            "z_axis": 0,
        }

        # Set the timestamp of the last measurement in milliseconds
        self.timestamp = int(time.time() * 1000)

        # Set the Temperature Sensor Unit to Celsius
        self.unit = AccelerometerSensor.ACCELERATION_UNIT
```

The main difference here is that the value is not a basic data type (e.g., int or double) but instead 
a structured dictionary containing the acceleration values on the three different axis.

The next step is to add the `update_measurement` method to model the generation of new energy samples:

```python
def update_measurement(self):
    """ Update the measurement of the sensor with a random increment """

    self.value.x_axis = randint(-400, 400)
    self.value.y_axis = randint(-400, 400)
    self.value.z_axis = randint(-400, 400)

    # Set the timestamp of the last measurement in milliseconds
    self.line_update_timestamp = int(time.time() * 1000)
```

Final step is to define the `get_json_description` in order to define how the sensor will be described in JSON with available 
attributes and data.

```python
def get_json_description(self):
    """ Returns a JSON representation of the temperature sensor """
    result_dict = {
        "device_id": self.device_id,
        "device_type": self.device_type,
        "device_manufacturer": self.device_manufacturer,
        "value": self.value,
        "unit": self.unit,
        "timestamp": self.line_update_timestamp
    }

    return json.dumps(result_dict)
```

## Data Management

The class `DataManager` has been defined to shape how data are managed in the application, to centralize the associated methods and 
_hide_ how data and information are effectively stored by the class itself.

The actual implementation has the following main capabilities:

- **Device Management**: allows to store and retrieve Devices for the Smart Home through dedicated method. The adopted data structure is a `list` of devices.
- **Measurement Management**: supports the saving and retrieval of sensor measurements and actuator variations over time.

Implemented and supported methods are:

- `add_device(device)`: Add a new device to the Data Manager
- `remove_device(device_id)`: Remove a device from the Data Manager 
- `get_device(device_id)`: Get a device by its Id from the stored devices on the Data Manager
- `store_measurement(device_id, measurement)`: Store a measurement for a device. It can be associated both a variation of a Sensor or a status change in an actuator
- `get_measurements(device_id)`: Get all measurements for a specific device
- `get_all_measurements()`: Retrieve all the stored measurements

## Smart Home

The Smart Home class is in charge of two main responsibilities: 

- **Device Management**: Exposes the capabilities to manage devices (`add`, `remove`, and `get`) hiding the fact that it is using an instance of the `DataManager` to do that.
- **Measurement Service**: Exposes stored measurements associated to both sensors and actuators hiding the fact that it is using an instance of the `DataManager` to do that.
- **Home Monitoring**: Implements a method to emulate the `monitoring` of the Smart Home that periodically check and update sensors measurements and randomly change actuators status.

## Main Application

The `main.py` file is the entry point of the application. It creates a Smart Home instance and adds some devices to it.
It also starts the monitoring of the Smart Home and prints the measurements of the devices.

```python
    # Create the smart home
my_smart_home = SmartHome(DataManager(), "SH001", 37.7749, -122.4194)

# Add devices
temp_sensor = TemperatureSensor(device_id=1)
humidity_sensor = HumiditySensor(device_id=2)
smart_light = SmartLight(device_id=3)

my_smart_home.add_device(temp_sensor)
my_smart_home.add_device(humidity_sensor)
my_smart_home.add_device(smart_light)

# Get Initial Status of all devices
print("\nInitial Status of IoT Devices:")
for device in my_smart_home.get_all_devices():
    # Check if the devices is a sensor or an actuator and print the value or the status
    if isinstance(device, Sensor):
        print(f'Sensor: {device.device_id} Value: {device.value} Timestamp: {device.line_update_timestamp}')
    elif isinstance(device, Actuator):
        print(f'Actuator: {device.device_id} Value: {device.status} Timestamp: {device.line_update_timestamp}')

# Monitor the smart home for 5 seconds
my_smart_home.monitor_home(seconds=5)

# Get all stored measurements
measurements = my_smart_home.get_all_measurements()
print("\nStored Measurements:")
for device_id, device_measurements in measurements.items():
    for measurement in device_measurements:
        print(f"Device {device_id} - Measurement: {measurement}")

# Print Json Description of all devices
print("\nJson Description of all devices:")
for device in my_smart_home.get_all_devices():
    print(device.get_json_description())
```

## File Organization & Modules

To organize your classes and files into different folders, you can follow these steps:  
Create a Directory Structure: Organize your files into directories based on their functionality. For example:  

```text
smart_home_project/
├── data
    ├── __init__.py
    ├── data_manager.py
├── devices/
│   ├── __init__.py
│   ├── actuator.py
│   ├── sensor.py
│   ├── smart_light.py
├── main.py
├── smart_home.py
└── README.md
```
The `__init__.py` file is used to mark a directory as a Python package. 
This allows you to import modules from that directory. 
Here are the main reasons why you need an `__init__.py` file:  

- **Package Initialization:** It can be used to execute initialization code for the package or set the __all__ variable to control what is imported when from package import * is used.  
- **Namespace Management:** It helps in managing the namespace of the package, ensuring that the modules within the package can be imported correctly.  
- **Compatibility:** In older versions of Python (before 3.3), the presence of __init__.py was required to recognize a directory as a package. Although it is not strictly necessary in Python 3.3 and later, it is still a good practice to include it for compatibility and clarity.

After that you have to update imports adjusting the import statements in your files to reflect the new directory structure.
For example in the `main.py` we will have an updated import for SmartLight class:

```python
from data.data_manager import DataManager
from home.smart_home import SmartHome
from devices.switch import Switch

[...]
```

If you have an import from a different class within the same directory you should use a relative import
like the following statement: 

```python
from .device import Device
```