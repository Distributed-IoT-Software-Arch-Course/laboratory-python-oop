from typing import Dict
from typing import Optional
from devices.switch import Switch
from data.storage_manager import StorageManager
from devices.industrial_machine import IndustrialMachine
from random import random
import json
import time

class ProductionLine:

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

    def add_industrial_machine(self, industrial_machine: IndustrialMachine):
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

    def remove_industrial_machine(self, industrial_machine_id: str):
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






