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