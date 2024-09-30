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

Each Machine is a Device that exposes and implements also the following methods:

- `start()`: to start machine operations by changing the state of the associated actuators and sensors
- `stop()`: to stop machine operations by changing the state of the associated actuator and sensors
- `update_measurements()`: to update all the measurements associated to both energy monitoring and accelerometers sensors
- `get_json_description()`: to get the description of the machine in JSON format
- `get_json_measurement()`: to get the description of the machine measurements in JSON format

Machine can be then associated to a `ProductionLine` in charge of handling multiple Machines at the same time and exposing 
the following methods:

- `add_industrial_machine(machine)`: Allows to add a machine to the Production Line
- `remove_industrial_machine(machine)`: Allows to remove a machine to the Production Line
- `get_machine_list()`: Retrieves the list of machines associated to the Production Line
- `get_industrial_machine(machine_id)`: Retrieves an existing machine from the Production Line
- `start()`: to start all the managed machines calling the associated `start()` method for each machine
- `stop()`: to stop all the managed machines calling the associated `stop()` method for each machine
- `get_json_description()`: to get the description of the entire Production Line in JSON format
- `get_json_measurement()`: to get the description of the entire Production Line in JSON format
- `start_monitoring(self, seconds=5)`: to start the monitoring of the Production Line for a specific amount of time

The Laboratory will involve designing data structure, identify classes (and creating them in Python to model these devices, 
a central system to collect and manage data.

**Note:** The scenario is simplified without any kind of communication, and everything is running within the same process. 

Playground Sections:

- [Base Classes](#base-classes)
- [Folders & Base Classes](#folders--base-classes)
- [Device Class](#device-class)
- [Sensors & Actuator Classes](#sensors--actuator-classes)
- [Sensors & Actuator SubClasses](#sensors--actuator-subclasses)
  - [Energy Sensor Class](#energy-sensor-class)
  - [Accelerometer Sensor Class](#accelerometer-sensor-class)
  - [Switch Class](#switch-class)
  - [Industrial Machine Class](#industrial-machine-class)
- [Storage Manager Class](#storage-manager-class)
- [Production Line Class](#production-line-class)
- [Main Application](#main-application)

## Base Classes

The basic classes (taken from the OOP Playground [Link](https://github.com/Distributed-IoT-Software-Arch-Course/python-oop-playground)) are:

- `Device`: Base class for all devices defining the following attributes for all the devices such as sensors and actuators subclasses:
  - `device_id`: Id of the device
  - `device_type`: Type of the device
  - `device_manufacturer`: Manufacturer of the device
  - The Device class defines two core method that will be inherited by every subclasses: 
    - `get_json_measurement`: Returns a JSON representation of the Status of the device (e.g., the last measurement o the last state of an actuator). This method should be implemented by subclasses.
    - `get_json_description`: Returns a JSON representation of the Device. The Device class already provide a default implementation that can be applied to every device and subclasses (e.g., Sensor and Actuator)
- `Sensor`: Base class for all sensors extending `Device` class and adding: 
  - Methods:
    - `update_measurement()`: update the sensor value. The default implementation throws a `NotImplementedError` exception and the subclasses must implement it. 
  - Attributes:
    - `value`: associated to the current sensor value
    - `unit`: mapping the unit associated to the physical measurement type
    - `timestamp` of the last sample in milliseconds
- `Actuator`: Base class for all actuators extending `Device` class and adding:
  - Methods:
    - `invoke_action(action_type, payload)`: method and the `get_json_description` method to get the description of the sensor in JSON format
  - Attributes:
    -  `status`: associated to the current status of the actuator
    - `timestamp` of the last action in milliseconds

### Folders & Base Classes

To organize your classes and files into different folders, you can follow these steps:  
Create a Directory Structure: Organize your files into directories based on their functionality. 
For example in our case we will have:  

```text
smart_factory_project/
├── data
    ├── __init__.py
    ├── storage_manager.py
├── devices/
│   ├── __init__.py
│   ├── accelerometer_sensor.py
│   ├── actuator.py
│   ├── device.py
│   ├── energy_sensor.py
│   ├── industrial_machine.py
│   ├── sensor.py
│   ├── switch.py
├── factory/
│   ├── __init__.py
│   ├── production_line.py
├── main.py
└── README.md
```

Follow the previous structure while creating the different files in the project 
presented during the next sections.

The `__init__.py` file is used to mark a directory as a Python package. 
This allows you to import modules from that directory. 
Here are the main reasons why you need an `__init__.py` file:  

- **Package Initialization:** It can be used to execute initialization code for the package or set the __all__ variable to control what is imported when from package import * is used.  
- **Namespace Management:** It helps in managing the namespace of the package, ensuring that the modules within the package can be imported correctly.  
- **Compatibility:** In older versions of Python (before 3.3), the presence of __init__.py was required to recognize a directory as a package. Although it is not strictly necessary in Python 3.3 and later, it is still a good practice to include it for compatibility and clarity.


## Device Class

The Device class has the following structure with a constructor to initialize the Device instance and two methods
related to Json description of the device and the associated last measurement.

```python
import json

class Device:
    """ Base class for devices """

    def __init__(self, device_id, device_type, device_manufacturer):
        """ Initialize the devices with a devices ID and a devices type """
        self.device_id = device_id
        self.device_type = device_type
        self.device_manufacturer = device_manufacturer

    def get_json_measurement(self) -> str:
        """ Returns a JSON representation of the Sensor Status (e.g., the last measurement) """
        raise NotImplementedError("This method should be overridden by subclasses")

    def get_json_description(self) -> str:
        """ Returns a JSON representation of the Sensor Description """

        result_dict = {
            "device_id": self.device_id,
            "device_type": self.device_type,
            "device_manufacturer": self.device_manufacturer
        }

        return json.dumps(result_dict)
```

The method `get_json_measurement()` is not implemented since depends on the characteristics of the specific subclass
like `Sensor` that returns last measurements (e.g., Temperature) or `Actuator` that instead return the last state.

On the opposite, the method `get_json_description()` provides a default implementation describing the device in 
terms of its `id`, `type`, and `manufacturer`. This implementation is usable by every subclass but of course it can 
be overridden in order to customize or extend the behaviour.

## Sensors & Actuator Classes

The main two Subclasses for Device are `Sensor` and `Actuator` with the following structure

### Sensor Class

The `Sensor` class has the responsibility to map the properties and behaviours of the Sensors in our system and application.

```python
from .device import Device
import json

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
```

Then we declare and add a new method `update_measurement` in charge of structuring how each specific sensor model
the measuring of its new values. For this reason this method is empty and should be overridden by subclasses.

```python
def update_measurement(self) -> None:
    """ Update the measurement of the sensor, this method should be overridden by subclasses """
    raise NotImplementedError("This method should be overridden by subclasses")
```

On the other hand, the implementation of the `get_json_measurement` can be integrated in the `Sensor` class and then
inherited by Sensors subclasses defining how sensor measurements are reported as JSON String.

```python
def get_json_measurement(self) -> str:
    """ Returns a JSON Measurement of the humidity sensor """
    result_dict = {
        "device_id": self.device_id,
        "value": self.value,
        "unit": self.unit,
        "timestamp": self.timestamp
    }

    return json.dumps(result_dict)
```

### Actuator Class

The `Actuator` class has the responsibility to map the properties and behaviours of the Actuator in our system and application.

```python
from .device import Device
import json


class Actuator(Device):
    """ Base class for actuators """

    def __init__(self, device_id: str, device_type: str, device_manufacturer: str):
        """ Initialize the actuator with a devices ID and a devices type """
        super().__init__(device_id, device_type, device_manufacturer)

        # Initialize the status to None, subclasses should set the status when needed
        self.status = "off"

        # Set the timestamp to None, subclasses should set the timestamp when updating the status
        self.timestamp = None
```

With the following method `invoke_action` we model the behaviour of an Actuator that can receive and action request
and execute it starting from a `type` and a `payload` containing the detail of the action (e.g., `ON` and `OFF`).
In this case since this class is generic, this method is not implemented and should be overridden by subclasses.

```python
def invoke_action(self, action_type: str, payload: str) -> None:
    """ Invoke an action on the actuator """
    raise NotImplementedError("This method should be overridden by subclasses")
```

The 

```python
def get_json_measurement(self) -> str:
    """ Returns a JSON representation of the Sensor Status (e.g., the last measurement) """
    result_dict = {
        "device_id": self.device_id,
        "status": self.status,
        "timestamp": self.timestamp
    }

    return json.dumps(result_dict)
```

## Sensors & Actuator SubClasses

Starting from the base classes, we have the following subclasses:

- `EnergySensor`: model the Energy Monitoring Sensor associated to a Machine
- `AccelerometerSensor`: model the Accelerometer Sensor associated to a Machine
- `Switch`: model the Switch Actuator associated to a Machine

### Energy Sensor Class

The energy sensor is a subclass of the `Sensor` class and it is in charge of modeling the behaviour of an energy sensor.

```python
import time
from .sensor import Sensor
from random import random


class EnergySensor(Sensor):
    """ Energy Monitoring sensor class, extends Sensor class implementing the required methods of the base class"""

    # Sensor Type
    SENSOR_TYPE: str = "iot.sensor.energy"

    # Kilo-watt per hour unit
    KILO_WATT_HOUR_UNIT: str = "kWh"

    def __init__(self, device_id: str, initial_kwh: int = 0):
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
def update_measurement(self) -> None:
    """ Update the Kwh measurement of the sensor with a random increment """

    # Update the measurement with a random increment or decrement
    is_increment_decrement = random() > 0.5

    if is_increment_decrement:
        self.value += 2 * (random() + 0.5)
    else:
        self.value -= 2 * (random() + 0.5)

    # Set the timestamp of the last measurement in milliseconds
    self.timestamp = int(time.time() * 1000)
```

### Accelerometer Sensor Class

The accelerometer sensor is a subclass of the `Sensor` class and it is in charge of modeling the behaviour of an accelerometer sensor.
The main difference here is that the value is not a basic data type (e.g., int or double) but instead a structured dictionary containing the acceleration values on the three different axis.
The class defines also static attributes to define the sensor type and the unit of the acceleration values.

```python
import time
from random import randint
from .sensor import Sensor


class AccelerometerSensor(Sensor):
    """ Accelerometer Sensor class, extends Sensor class implementing get_status method """

    # Sensor Type
    SENSOR_TYPE: str = "iot.sensor.accelerometer"

    # Sensor Value Unit
    ACCELERATION_UNIT: str = "Acceleration"

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

The next step is to add the `update_measurement` method to model the generation of new energy samples:

```python
def update_measurement(self) -> None:
    """ Update the measurement of the sensor with a random increment """

    self.value['x_axis'] = randint(-400, 400)
    self.value['y_axis'] = randint(-400, 400)
    self.value['z_axis'] = randint(-400, 400)

    # Set the timestamp of the last measurement in milliseconds
    self.timestamp = int(time.time() * 1000)
```

### Switch Class

The switch is a subclass of the `Actuator` class and it is in charge of modeling the behaviour of a switch actuator.
The class introduces also static attributes to define the possible values of the switch status and the action type.

```python
from .actuator import Actuator
import time

class Switch(Actuator):
    """ Class representing a Switch Actuator """

    # Static Class's attributes used to define action types and values
    STATUS_ON: str = "ON"
    STATUS_OFF: str = "OFF"
    ACTUATOR_TYPE: str = "iot.actuator.switch"
    ACTION_TYPE_SWITCH: str = "SWITCH"

    def __init__(self, device_id: str):
        """ Initialize the smart light with a devices ID and an initial state """
        super().__init__(device_id, Switch.ACTUATOR_TYPE, "Acme Inc.")

        # Set the initial state of the smart light to off
        self.status = Switch.STATUS_OFF

        # Set the timestamp to None, subclasses should set the timestamp when updating the status
        self.timestamp = int(time.time() * 1000)
```

Since it is an actuator, the `invoke_action` method should be implemented to model the behaviour of the switch actuator.

```python
def invoke_action(self, action_type: str, payload: str) -> None:
    """ Invoke an action on the smart light """

    # Check if action_type Type and payload are Strings
    if not isinstance(action_type, str) or not isinstance(payload, str):
        raise ValueError("Action type and payload must be strings")

    # Check the action type and payload
    if action_type.upper() == Switch.ACTION_TYPE_SWITCH and payload.upper() in [Switch.STATUS_ON, Switch.STATUS_OFF]:
        self.status = payload
    else:
        raise ValueError("Unsupported action type")
```

### Industrial Machine Class

This class is in charge of modeling the behaviour of an Industrial Machine that is composed by:

- _1_ x `Energy Monitoring Sensors`
- _n_ x `Accelerometer Sensors`
- _1_ x `Switch`

The class has the following structure:

```python
from devices.accelerometer_sensor import AccelerometerSensor
from devices.device import Device
from devices.energy_sensor import EnergySensor
from devices.switch import Switch
import json


class IndustrialMachine(Device):
    """ Industrial Machine class, extends Device Class and add new features, attributes and methods """

    # Device Type
    DEVICE_TYPE = "iot.industrial.machine"

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
            self.accelerometer_sensor_list.append(AccelerometerSensor(f'{self.device_id}_switch_{sensor_index}'))
```

The init method initializes the machine declaring and initializing the energy sensor, the switch actuator, and a list of accelerometer sensors.
The `accelerometer_sensor_number` parameter is used to define the number of accelerometer sensors associated to the machine.

The `update_measurements` method is in charge of updating the measurements of all the sensors associated to the machine.

```python
def update_measurements(self) -> None:
    """Update all the measurements for the sensors associated to the Machine (energy and accelerometer)"""
    # Update Energy Sensor Measurements
    self.energy_sensor.update_measurement()

    # For each accelerometer sensor update the measurements
    for acc_sensor in self.accelerometer_sensor_list:
        acc_sensor.update_measurement()
```

The `get_json_description` method is in charge of returning a JSON representation of the machine.
Returns a JSON representation of the Device with the addition of the description of the energy sensor, the switch actuator, and the accelerometer sensors.
It is a custom implementation that extends the default implementation of the `Device` class.

```python
def get_json_description(self) -> str:
    """Return the list of last values for each device of the Industrial Machine
    This implementation is custom with respect to the default implementation in the Device class
    since it includes the list of accelerometer sensors, energy sensor, actuators and the machine information"""

    accelerometer_description_list = []

    # For each accelerometer sensor update the device descriptions and measurements
    for acc_sensor in self.accelerometer_sensor_list:
        accelerometer_description_list.append(acc_sensor.get_json_description())

    result_dict = {
        "machine_id": self.device_id,
        "machine_type": self.device_type,
        "machine_manufacturer": self.device_manufacturer,
        "switch_id": self.switch.get_json_description(),
        "energy_sensor_id": self.energy_sensor.get_json_description(),
        "accelerometer_sensor_id_list": accelerometer_description_list
    }

    return json.dumps(result_dict)
```

On the other hand, the `get_json_measurement` method is in charge of returning a JSON representation of the machine measurements.
Also in this case it is a custom implementation that extends the default implementation of the `Device` class.

```python
def get_json_measurement(self) -> str:
    """Return the list of last values for each device of the Industrial Machine
    This implementation is custom with respect to the default implementation in base class
    since it includes the measurements of accelerometer sensors, energy sensor, actuators and the machine information"""

    accelerometer_description_list = []

    # For each accelerometer sensor update the device descriptions and measurements
    for acc_sensor in self.accelerometer_sensor_list:
        accelerometer_description_list.append(acc_sensor.get_json_measurement())

    result_dict = {
        "machine_id": self.device_id,
        "switch": self.switch.get_json_measurement(),
        "energy_sensor": self.energy_sensor.get_json_measurement(),
        "accelerometer_sensor_list": accelerometer_description_list
    }

    return json.dumps(result_dict)
```

The `start` and `stop` methods are in charge of starting and stopping the machine operations.
The implementation simulates the start and stop of the machine by changing the status of the switch actuator
and measuring the energy consumption and the acceleration values.

```python
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
```

## Storage Manager Class

The class `StorageManager` has been defined to shape how data are stored in the application, to centralize the associated methods and 
_hide_ how data and information are effectively stored by the class itself.

The actual implementation has the following main capabilities:

- **Device Description Storage**: allows to store and retrieve Devices for the Smart Home through dedicated method. The adopted data structure is a `list` of devices.
- **Device Json Measurement Storage**: supports the saving and retrieval of sensor measurements and actuator variations over time.

Implemented and supported methods are:

- `store_device_description(self, device_id, device_description)`: store a device description in the storage
- `remove_device_description(self, device_id)`: remove a device description from the storage
- `get_device_description(self, device_id)`: get a device description from the storage
- `get_all_device_descriptions(self)`: get all device descriptions from the storage
- `store_measurement(self, device_id, measurement)`: store a measurement in the storage
- `get_measurements(self, device_id)`: get all measurements for a device from the storage
- `get_all_measurements(self)`: get all measurements from the storage

The constructor initializes two dictionaries to store the device descriptions and the device measurements.

```python
class StorageManager:
    """ Class to manage the data storage of the smart home """

    def __init__(self):
        """ Initialize the data manager with an empty dictionary to store sensor data """
        self.device_description_dict = {}
        self.device_measurement_dict = {}
```

The methods to handle the device descriptions are the following:

```python
def store_device_description(self, device_id: str, device_description: str) -> None:
    """ Store a new device description """
    self.device_description_dict[device_id] = device_description

def remove_device_description(self, device_id: str) -> None:
    """ Remove a stored device description """
    if device_id in self.device_description_dict.keys():
        del self.device_measurement_dict[device_id]

def get_device_description(self, device_id: str) -> Optional[str]:
    """ Get a device description by its ID """
    if device_id in self.device_description_dict.keys():
            return self.device_description_dict[device_id]
    else:
        return None

def get_all_device_descriptions(self) -> list[str]:
    """ Return all the device Descriptions """
    return list(self.device_description_dict.values())
```

On the other hand, the methods to handle the device measurements are the following:

```python
def store_measurement(self, device_id: str, measurement: str) -> None:
    """ Store a measurement for a devices. It can be associated both a variation of a
    Sensor or a status change in an actuator """
    if device_id not in self.device_measurement_dict:
        self.device_measurement_dict[device_id] = []
    self.device_measurement_dict[device_id].append(measurement)

def get_measurements(self, device_id) -> list[str]:
    """ Get all measurements for a specific devices """
    return self.device_measurement_dict.get(device_id, [])

# Get all measurements for all devices
def get_all_measurements(self) -> list[str]:
    """ Get all measurements for all devices """
    return list(self.device_measurement_dict.values())
```

## Production Line Class

The `ProductionLine` class is in charge of managing multiple `IndustrialMachine` instances and to start and stop all the machines at the same time.
It also allows to monitor the machines for a specific amount of time. The class has the following structure:

- List of Industrial Machines
- Storage Manager
- Line Status (ON/OFF)
- Line Update Timestamp
- Latitude and Longitude
- Line Id
- Line Name

```python
from typing import Dict
from typing import Optional
from devices.switch import Switch
from data.storage_manager import StorageManager
from devices.industrial_machine import IndustrialMachine
from random import random
import json
import time


class ProductionLine:
    """ Class representing a Production Line in a Factory supporting multiple Industrial Machines """

    def __init__(self, production_line_id: str, name: str, latitude: float, longitude:float, storage_manager: StorageManager):
        """Initialize the Production line with id, name and geographic coordinates"""

        self.line_id: str = production_line_id
        self.name: str = name
        self.latitude: float = latitude
        self.longitude: float = longitude
        self.machine_dict: Dict[str, IndustrialMachine] = {}
        self.storage_manager: StorageManager = storage_manager
        self.line_status = False
        self.line_update_timestamp = int(time.time() * 1000)

        # Store the Production on the Data Manager
        self.storage_manager.store_device_description(self.line_id, self.get_json_description())
```

For the management of the machines, the class provides the following methods:

```python
def add_industrial_machine(self, industrial_machine: IndustrialMachine) -> None:
    """ Add a new machine to the production line """

    # Check if the parameter is an instance of IndustrialMachine
    if isinstance(industrial_machine, IndustrialMachine):

        # Add the machine to the dictionary
        self.machine_dict[industrial_machine.device_id] = industrial_machine

        # Update the stored Production Line Description
        self.storage_manager.store_device_description(self.line_id, self.get_json_description())

        # Add the Description of the single machine
        self.storage_manager.store_device_description(industrial_machine.device_id, industrial_machine.get_json_description())

    else:
        raise ValueError("Wrong type for industrial_machine parameter ! Expected is IndustrialMachine ...")

def remove_industrial_machine(self, industrial_machine_id: str) -> None:
    """ Remove a machine from the production line """

    # Check if the machine is in the dictionary
    if industrial_machine_id in self.machine_dict.keys():

        # Remove the machine from the dictionary
        self.machine_dict.pop(industrial_machine_id)

        # Update the stored Production Line Description (with the removed Machine Id Reference)
        self.storage_manager.store_device_description(self.line_id, self.get_json_description())

        # Remove the Description of the single machine
        self.storage_manager.remove_device_description(industrial_machine_id)

    else:
        raise ValueError(f"Machine with ID {industrial_machine_id} not found in the Production")
```

For accessing the machines and their descriptions, the class provides the following methods:

```python
def get_machine_list(self) -> list[IndustrialMachine]:
    """ Get Machine List for the Production Line"""
    return list(self.machine_dict.values())

def get_industrial_machine(self, industrial_machine_id: str) -> Optional[IndustrialMachine]:
    """ Get a machine by its ID. It uses Optional to handle the case where the machine is not found
    returning None in that case """
    if industrial_machine_id in self.machine_dict.keys():
        return self.machine_dict[industrial_machine_id]
    else:
        return None
```

To start and stop the machines, the class provides the following methods:

```python
def start(self) -> None:
    """Starting the machines associated to the production line"""
    print(f'\nStarting Production Line: {self.line_id} ...\n')

    for machine in self.machine_dict.items():
        if isinstance(machine, IndustrialMachine):
            print(f'\tStarting Machine{machine.device_id} ...')
            machine.start()

    # Update the Production Line Status
    self.line_status = True
    self.line_update_timestamp = int(time.time() * 1000)

    # Save the updated measurement in the storage manager
    self.storage_manager.store_measurement(self.line_id, self.get_json_measurement())

def stop(self) -> None:
    """Stopping the machines associated to the production line"""
    print(f'\nStopping Production Line: {self.line_id} ...\n')

    for machine in self.machine_dict.items():
        if isinstance(machine, IndustrialMachine):
            print(f'\tStopping Machine{machine.device_id} ...')
            machine.stop()

    # Update the Production Line Status
    self.line_status = False
    self.line_update_timestamp = int(time.time() * 1000)

    # Save the updated measurement in the storage manager
    self.storage_manager.store_measurement(self.line_id, self.get_json_measurement())
```

The class provides also the following methods to get the JSON description and measurements of the production line:

```python
def get_json_measurement(self) -> str:
    """Return a JSON Measurement for the Production Line."""

    result_dict = {
        "line_id": self.line_id,
        "line_status": self.line_status,
        "line_update_timestamp": self.line_update_timestamp
    }

    return json.dumps(result_dict)

def get_json_description(self) -> str:
    """Return a JSON Description for the Production Line.
    It includes the Production Line ID, Name, Latitude, Longitude and the list of machines IDs associated to the Production Line.
    It contains only the machine ids in order to avoid data replication in the storage manager.
    Individual Machine Descriptions are stored separately in the storage manager"""

    result_dict = {
        "line_id": self.line_id,
        "name": self.name,
        "latitude": self.latitude,
        "longitude": self.longitude,
        "machine_list": list(self.machine_dict.keys()),
    }

    return json.dumps(result_dict)
```

The `start_monitoring` method is in charge of monitoring the production line for a specific amount of time.
This method iterates over the list of machines and updates the measurements or triggers actions every 2 seconds.
It is a demo emulation of the monitoring process reading the sensors and randomly triggering the actuators.

```python
def start_monitoring(self, seconds=5) -> None:
    """ Monitor the smart home for a given number of seconds """

    # Iterate n times over the list of devices and update the measurements or trigger actions every 2 seconds
    for _ in range(seconds):

        # Wait for 1 seconds
        print(f"\nMonitoring Production Line: {self.line_id}")
        time.sleep(1)

        # Get the list of available machines
        for machine in self.machine_dict.values():

            print(f"Updating measurement for Machine: {machine.device_id} ...")

            # Update the measurements for the machine
            machine.update_measurements()

            # Save the updated measurement
            self.storage_manager.store_measurement(machine.device_id, machine.get_json_measurement())

            # Flip a coin and decide to switch the light on or off
            random_value = random()

            # If random value is greater than 0.5 change the state of the light
            if random_value > 0.5:

                original_status = machine.switch.status

                print(f"Changing Actuator:{machine.switch.device_id} Status for Machine: {machine.device_id} ...")

                if original_status == Switch.STATUS_ON:
                    machine.switch.invoke_action(Switch.ACTION_TYPE_SWITCH, Switch.STATUS_OFF)
                else:
                    machine.switch.invoke_action(Switch.ACTION_TYPE_SWITCH, Switch.STATUS_ON)

                new_device_status = machine.switch.status

                print(f"Actuator {machine.switch.device_id} for Machine: {machine.device_id} status changed from {original_status} to {new_device_status}")

                # Save the updated measurement
                self.storage_manager.store_measurement(machine.device_id, machine.get_json_measurement())
```

## Main Application

The `main.py` file is the entry point of the application. 
It creates the `StorageManager` instance and the `ProductionLine` instance and adds multiple `IndustrialMachine` instances to the production line.
Then it starts the production line and monitors it for a specific amount of time.
At the end, it retrieves the JSON description and measurements of the production line and saves them in the storage manager.

```python
from data.storage_manager import StorageManager
from devices.industrial_machine import IndustrialMachine
from factory.production_line import ProductionLine

# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    # Create the Data Manager to handle application information
    storage_manager = StorageManager()

    # Create Machines for Production Line 1
    industrial_machine_1 = IndustrialMachine("industrial_machine_1", accelerometer_sensor_number=3)
    industrial_machine_2 = IndustrialMachine("industrial_machine_2", accelerometer_sensor_number=3)
    industrial_machine_3 = IndustrialMachine("industrial_machine_3", accelerometer_sensor_number=3)

    # Create Production Line 1
    production_line_1 = ProductionLine("production_line_1",
                                       "TestProductionLine",
                                       44.61331038745227,
                                       10.892943550441561,
                                       storage_manager)

    # Add Machines to the production Line
    production_line_1.add_industrial_machine(industrial_machine_1)
    production_line_1.add_industrial_machine(industrial_machine_2)
    production_line_1.add_industrial_machine(industrial_machine_3)

    # Start the Production Line
    production_line_1.start()

    # Monitoring Production Line for n seconds
    production_line_1.start_monitoring(seconds=10)

    # Stop the Production Line
    production_line_1.stop()

    # Print collected measurements and variations
    devices_descriptions = storage_manager.get_all_device_descriptions()
    for device_id, device_description in devices_descriptions.items():
        print(f"Device Description - DeviceId: {device_id} - Description: {device_description}")

    # Print collected measurements and variations
    measurements = storage_manager.get_all_measurements()
    for device_id, device_measurements in measurements.items():
        for measurement in device_measurements:
            print(f"Device {device_id} - Measurement: {measurement}")
```