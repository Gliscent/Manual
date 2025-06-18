from airsim import MultirotorClient
import time

client = MultirotorClient()
client.confirmConnection()

vehicle_name = "Drone2"
client.enableApiControl(True, vehicle_name)
client.armDisarm(True, vehicle_name)
client.takeoffAsync(vehicle_name=vehicle_name).join()
time.sleep(1)
client.landAsync(vehicle_name=vehicle_name).join()
time.sleep(1)
client.armDisarm(False, vehicle_name)
client.enableApiControl(False, vehicle_name)
