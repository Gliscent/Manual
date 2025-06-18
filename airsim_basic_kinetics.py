import time
import airsim

# 번갈아가면서 시동 성공, 실패의 문제는 PX4 쪽 문제(Arming denied) 인 것 같지만, 어쨌든 나중에 해결할 수 있음 해보기
# moveToPositionAsync는 앞(북쪽)이 x고, NED 좌표계 사용-->동쪽 x, 북쪽 y, 위쪽 z로 변경함.
# 명령 사이 사이 딜레이를 넣어야 명령 중복 에러 방지
# 되도록 moveToPositionAsync 명령어에 .join 쓰지 말기


client = airsim.MultirotorClient()
client.confirmConnection()
print(client.listVehicles())

vehicle_name = "Drone2"
client.enableApiControl(True, vehicle_name=vehicle_name)
client.armDisarm(True)
client.takeoffAsync().join()
time.sleep(1)

def track(duration_sec=10, interval_sec=0.2):
    steps = int(duration_sec / interval_sec)
    for _ in range(steps):
        state = client.getMultirotorState(vehicle_name=vehicle_name)
        pos = state.kinematics_estimated.position
        ori = state.kinematics_estimated.orientation
        roll, pitch, yaw = airsim.to_eularian_angles(ori)  # 라디안 기준

        print(f"Position: x={pos.x_val:.2f}, y={pos.y_val:.2f}, z={pos.z_val:.2f}")
        print(f"Orientation: Roll={roll:.2f}, Pitch={pitch:.2f}, Yaw={yaw:.2f} (rad)")
        print("-" * 50)
        time.sleep(interval_sec)

x, y, z = 50, 13, 20


# # 1. yaw를 초기 상태로 고정
# client.moveToPositionAsync(y, x, -z, 5)
# track(10)
# client.moveToPositionAsync(0, 0, -z, 5)
# track(10)
#
# # 2. yaw를 특정 방향으로 고정
# client.moveToPositionAsync(
#     y, x, -z, 5,
#     yaw_mode=airsim.YawMode(is_rate=False, yaw_or_rate=30),
#     vehicle_name=vehicle_name
# )
# time.sleep(10.0)
# client.moveToPositionAsync(
#     0, 0, -z, 5,
#     yaw_mode=airsim.YawMode(is_rate=False, yaw_or_rate=30),
#     vehicle_name=vehicle_name
# )
# time.sleep(10.0)
#
# # 3. yaw 일정 각속도
# client.moveToPositionAsync(
#     y, x, -z, 5,
#     drivetrain=airsim.DrivetrainType.MaxDegreeOfFreedom,
#     yaw_mode=airsim.YawMode(is_rate=True, yaw_or_rate=50),  # 초당 10도 회전
#     vehicle_name=vehicle_name
# )
# time.sleep(10.0)
# client.moveToPositionAsync(
#     0, 0, -z, 5,
#     drivetrain=airsim.DrivetrainType.MaxDegreeOfFreedom,
#     yaw_mode=airsim.YawMode(is_rate=True, yaw_or_rate=50),  # 초당 10도 회전
#     vehicle_name=vehicle_name
# )
# time.sleep(10.0)


# 착륙 및 정리
client.landAsync(vehicle_name=vehicle_name).join()
client.armDisarm(False, vehicle_name=vehicle_name)
client.enableApiControl(False, vehicle_name=vehicle_name)
