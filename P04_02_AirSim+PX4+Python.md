Ubuntu : PX4 && Window : Airsim, Python
---


## 1. 파이썬 에어심 라이브러리 빌드
```bash
pip install msgpack-rpc-python==0.4.1
pip install msgpack-python==0.5.6
pip install airsim

sudo apt install geographiclib-tools
sudo geographiclib-get-geoids egm96-5
```
--> 잘 안되면 gpt 형한테 물어보기

## 2. 위치, 속도, 각도 기초 제어

```bash
import time
import airsim

# 번갈아가면서 시동 성공, 실패의 문제는 PX4 쪽 문제(Arming denied) 인 것 같지만, 어쨌든 나중에 해결할 수 있음 해보기
# moveToPositionAsync는 앞(북쪽)이 x고, NED 좌표계 사용-->동쪽 x, 북쪽 y, 위쪽 z로 변경함.
# 명령 사이 사이 딜레이를 넣어야 명령 중복 에러 방지
# 되도록 moveToPositionAsync 명령어에 .join 쓰지 말기


client = airsim.MultirotorClient()
client.confirmConnection()

vehicle_name = "Drone1"
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


# 1. yaw를 초기 상태로 고정
client.moveToPositionAsync(y, x, -z, 5)
track(10)
client.moveToPositionAsync(0, 0, -z, 5)
track(10)

# 2. yaw를 특정 방향으로 고정
client.moveToPositionAsync(
    y, x, -z, 5,
    yaw_mode=airsim.YawMode(is_rate=False, yaw_or_rate=30),
    vehicle_name=vehicle_name
)
time.sleep(10.0)
client.moveToPositionAsync(
    0, 0, -z, 5,
    yaw_mode=airsim.YawMode(is_rate=False, yaw_or_rate=30),
    vehicle_name=vehicle_name
)
time.sleep(10.0)

# 3. yaw 일정 각속도
client.moveToPositionAsync(
    y, x, -z, 5,
    drivetrain=airsim.DrivetrainType.MaxDegreeOfFreedom,
    yaw_mode=airsim.YawMode(is_rate=True, yaw_or_rate=50),  # 초당 10도 회전
    vehicle_name=vehicle_name
)
time.sleep(10.0)
client.moveToPositionAsync(
    0, 0, -z, 5,
    drivetrain=airsim.DrivetrainType.MaxDegreeOfFreedom,
    yaw_mode=airsim.YawMode(is_rate=True, yaw_or_rate=50),  # 초당 10도 회전
    vehicle_name=vehicle_name
)
time.sleep(10.0)


# 착륙 및 정리
client.landAsync(vehicle_name=vehicle_name).join()
client.armDisarm(False, vehicle_name=vehicle_name)
client.enableApiControl(False, vehicle_name=vehicle_name)
```

## 3. 이미지 처리

```bash
import airsim
import numpy as np
import cv2
import time

client = airsim.MultirotorClient()
client.confirmConnection()

while True:
    '''
    airsim.ImageType.Scene : 일반적 RGB 이미지
    airsim.ImageType.DepthPlanar : 직교 투영 깊이 # 깊이 (m)로 출력,
    airsim.ImageType.DepthPerspective : 원근 투영 깊이 # 깊이 (m)로 출력
    airsim.ImageType.DepthVis : 깊이 이미지
    airsim.ImageType.Segmentation : 객체 세그멘테이션 이미지
    airsim.ImageType.SurfaceNormals : 표면 법선 # 객체의 방향 분석 이미지
    airsim.ImageType.Infrared : 적외선 이미지
    airsim.ImageType.DisparityNormalized : 스테레오 disparity (상이성) 이미지
    airsim.ImageType.OpticalFlow : 광류 이미지
    '''

    '''
        camera_name "0" : 앞
        camera_name "1" : 앞
        camera_name "2" : 앞
        camera_name "3" : 아래
        camera_name "4" : 후방
        '''

    responses = client.simGetImages([
        airsim.ImageRequest("0", airsim.ImageType.DepthVis, False, True),
        airsim.ImageRequest("0", airsim.ImageType.Segmentation, False, True),
        airsim.ImageRequest("0", airsim.ImageType.DisparityNormalized, False, True),
        airsim.ImageRequest("0", airsim.ImageType.OpticalFlow, False, True),
        airsim.ImageRequest("0", airsim.ImageType.DepthPlanar, True),  # Float, in meters
    ])

    # 1. responses[0]
    img1_1d = np.frombuffer(responses[0].image_data_uint8, dtype=np.uint8)
    img1 = cv2.imdecode(img1_1d, cv2.IMREAD_COLOR)

    # 2. responses[1]
    img2_1d = np.frombuffer(responses[1].image_data_uint8, dtype=np.uint8)
    img2 = cv2.imdecode(img2_1d, cv2.IMREAD_COLOR)

    # 3. responses[2]
    img3_1d = np.frombuffer(responses[2].image_data_uint8, dtype=np.uint8)
    img3 = cv2.imdecode(img3_1d, cv2.IMREAD_COLOR)

    # 4. responses[3]
    img4_1d = np.frombuffer(responses[3].image_data_uint8, dtype=np.uint8)
    img4 = cv2.imdecode(img4_1d, cv2.IMREAD_COLOR)

    # 5. responses[4]
    depth_img = np.array(responses[4].image_data_float, dtype=np.float32)
    depth_img = depth_img.reshape(responses[4].height, responses[4].width)
    center_x = responses[2].width // 2
    center_y = responses[2].height // 2
    center_depth = depth_img[center_y, center_x]
    print(f"[중심 ({center_x},{center_y})] 깊이: {center_depth:.2f}m | 평균: {np.mean(depth_img):.2f}m")


    # 창 띄우기
    cv2.imshow("Image1", img1)
    cv2.imshow("Image2", img2)
    cv2.imshow("Image3", img3)
    cv2.imshow("Image4", img4)


    # 종료 조건
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


cv2.destroyAllWindows()
```

## 4. 멀티 드론 (터미널)

추측 : 파이썬에서는 TCP 포트 4560만 지원해서 멀티 드론이 안된다.

setting.json을 다음과 같이 설정 (ip 설정은 다르게 해야함)
```bash
{
  "SettingsVersion": 1.2,
  "SimMode": "Multirotor",
  "ClockType": "SteppableClock",
  "OriginGeopoint": {
    "Latitude": 47.641468,
    "Longitude": -122.140165,
    "Altitude": 0
  },

  "Vehicles": {
    "Drone1": {
      "VehicleType": "PX4Multirotor",
      "X": 4,
      "Y": 0,
      "Z": -2,
      "Yaw": -180,
      "UseSerial": false,
      "Lockstep": true,
      "UseTcp": true,
      "QgcHostIp": "",
      "TcpPort": 4560,
      "ControlIp": "192.168.10.13",
      "LocalHostIp": "0.0.0.0",
      "Sensors": {
        "barometer": {
          "SensorType": 1,
          "Enabled": true,
          "PressureFactorSigma": 0.0001825
        }
      }
    },

    "Drone2": {
      "VehicleType": "PX4Multirotor",
      "X": 8,
      "Y": 0,
      "Z": -2,
      "UseSerial": false,
      "Lockstep": true,
      "UseTcp": true,
      "UseUdp": true,
      "QgcHostIp": "",
      "TcpPort": 4561,
      "ControlIp": "192.168.10.13",
      "LocalHostIp": "0.0.0.0",
      "Sensors": {
        "barometer": {
          "SensorType": 1,
          "Enabled": true,
          "PressureFactorSigma": 0.0001825
        }
      }

    }

  }
}

```

2개의 터미널 창을 열고, 각각 아래와 같이 입력
```
cd PX4-Autopilot
PX4_SIM_MODEL=none_iris ./build/px4_sitl_default/bin/px4 -i 0
mavlink stop-all
mavlink start -u 14580 -r 4000000 -m onboard -o 14540 -t 127.0.0.1
# PX4_SIM_MODEL=none_iris ./build/px4_sitl_default/bin/px4 -i 0 ./ROMFS/px4fmu_common -s etc/init.d-posix/rcS -d "mavlink stop-all; mavlink start -u 14580 -r 4000000 -m onboard -o 14540 -t 127.0.0.1"



cd PX4-Autopilot
PX4_SIM_MODEL=none_iris ./build/px4_sitl_default/bin/px4 -i 1
mavlink stop-all
mavlink start -u 14581 -r 4000000 -m onboard -o 14541 -t 127.0.0.1
# PX4_SIM_MODEL=none_iris ./build/px4_sitl_default/bin/px4 -i 1 ./ROMFS/px4fmu_common -s etc/init.d-posix/rcS -d "mavlink stop-all; mavlink start -u 14581 -r 4000000 -m onboard -o 14541 -t 127.0.0.1"
```
참고 사항 : -i X 는 TCP 포트 4560+X 를 연다는 뜻.

각 터미널에서 commander ~~ 로 기동 명령