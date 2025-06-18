Airsim + ROS2 jazzy (ubuntu 24.04)
---
ROS랑 컨셉은 비슷하지만, 상세 설정이 많음. 우선 P03_02 하고 오기. 

## 1. PX4 설치 (P01 참고)

## 2. 의존성 설치 (정책만 살짝 무시함)
```
sudo apt update && sudo apt upgrade
sudo apt install python3-pip
sudo apt install python3-kconfiglib
pip3 install --user pyros-genmsg empy jinja2 toml numpy --break-system-packages
sudo apt install ros-jazzy-mavros ros-jazzy-mavros-extras
wget https://raw.githubusercontent.com/mavlink/mavros/master/mavros/scripts/install_geographiclib_datasets.sh
sudo bash install_geographiclib_datasets.sh
sudo apt install ros-jazzy-rmw-cyclonedds-cpp
```

## 2. 워크스페이스, 패키지 생성 (패키지 이름은 원할 대로)
```
cd ~/ros2_ws/src
ros2 pkg create --build-type ament_python mavros_pkg
cd ~/ros2_ws/src/mavros_pkg
mkdir launch
```


## 3. bashrc에 관련 내용 추가
```
source /opt/ros/jazzy/setup.bash
source ~/ros2_ws/install/setup.bash

export PX4_SIM_HOST_ADDR=192.168.10.8 (이거이거~~~~!!!!! 윈도우 컴 ip로 설정)
export RMW_IMPLEMENTATION=rmw_cyclonedds_cpp

alias nb="nano ~/.bashrc"
alias sb="source ~/.bashrc"
alias px4="cd; cd PX4-Autopilot; make px4_sitl none_iris"
alias cb="cd; cd ros2_ws; colcon build"
```

## 4. 파일 수정 (꼼꼼히 해야됨)

setup.py에 launch 등록, 내용 추가
```
cd ~/ros2_ws/src/mavros_pkg
nano setup.py
```

setup.py를 아래와 같이 수정
```
from setuptools import setup, find_packages

package_name = 'mavros_pkg'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(),
    py_modules=[],
    data_files=[
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/launch', ['launch/multi_mavros.launch.py']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='park',
    maintainer_email='your@email.com',
    description='Multi MAVROS launch file',
    license='MIT',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [],
    },
)

```
편의상 .launch.py 생성.

참고로 .launch는 ros2에 존재하지 않음.

```
cd ~/ros2_ws/src/mavros_pkg/launch
nano multi_mavros.launch.py
```

여기서 정확하지는 않지만, 경험적으로 target_system_id 가 (인스턴스 값)+1 이 되어야 하는 듯함.

그리고 드론 댓수에 따라서 system_id는 임의로 설정해도 될듯. 예시로 10대면 12부터 시작.
```
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        # MAVROS Node for drone1
        Node(
            package='mavros',
            executable='mavros_node',
            namespace='drone1',
            output='screen',
            parameters=[{
                'fcu_url': 'udp://127.0.0.1:14541@127.0.0.1:14581',
                'gcs_url': '',
                'system_id': 12,                # MAVROS의 SYS ID
                'component_id': 1,
                'target_system_id': 2,         # PX4 인스턴스 1의 SYS ID
                'target_component_id': 1,
            }],
        ),

        # MAVROS Node for drone2
        Node(
            package='mavros',
            executable='mavros_node',
            namespace='drone2',
            output='screen',
            parameters=[{
                'fcu_url': 'udp://127.0.0.1:14542@127.0.0.1:14582',
                'gcs_url': '',
                'system_id': 13,                # MAVROS의 SYS ID
                'component_id': 1,
                'target_system_id': 3,         # PX4 인스턴스 2의 SYS ID
                'target_component_id': 1,
            }],
        ),
    ])

```

패키지 진입
```
cd ~/ros2_ws/src/mavros_pkg
nano package.xml
```

패키지 내용 수정
```pakcage.xml
<?xml version="1.0"?>
<?xml-model href="http://download.ros.org/schema/package_format3.xsd" schematypens="http://www.w3.org/2001/XMLSchema"?>
<package format="3">
  <name>mavros_pkg</name>
  <version>0.0.1</version>
  <description>Multi-drone MAVROS launch package for ROS 2</description>

  <maintainer email="park@todo.todo">park</maintainer>
  <license>MIT</license>

  <buildtool_depend>ament_cmake</buildtool_depend>
  <buildtool_depend>ament_python</buildtool_depend>

  <exec_depend>rclpy</exec_depend>
  <exec_depend>mavros</exec_depend>
  <exec_depend>launch</exec_depend>
  <exec_depend>launch_ros</exec_depend>

  <test_depend>ament_copyright</test_depend>
  <test_depend>ament_flake8</test_depend>
  <test_depend>ament_pep257</test_depend>
  <test_depend>python3-pytest</test_depend>

  <export>
    <build_type>ament_python</build_type>
    <launch>
      share/launch
    </launch>
  </export>
</package>
```
사실 위에 내용들 중 대부분은 쓸모가 없을 수도 있지만, 언젠가는 도움이 될만한 설정들이 여럿 있음.

패키지 빌드
```
cd ~/ros2_ws
colcon build
source install/setup.bash
```

여기까지가 환경 설정이었고, 이제부터 실행

### Terminal1 (드론 1 UDP 연결)
```
cd PX4-Autopilot
PX4_SIM_MODEL=none_iris ./build/px4_sitl_default/bin/px4 -i 1

mavlink stop-all
mavlink start -u 14581 -r 4000000 -m onboard -o 14541 -t 127.0.0.1
```

### Terminal2 (드론 2 UDP 연결)
```
cd PX4-Autopilot
PX4_SIM_MODEL=none_iris ./build/px4_sitl_default/bin/px4 -i 2

mavlink stop-all
mavlink start -u 14582 -r 4000000 -m onboard -o 14542 -t 127.0.0.1
```

### Terminal3 (토픽 발행)
```
ros2 launch mavros_pkg multi_mavros.launch.py
```

### Terminal4 (사용 예시)

위치 받기
```
ros2 topic echo /drone2/local_position/pose
```

###  이륙 착륙

드론 1 이륙 모드 on
```
ros2 service call /drone1/set_mode mavros_msgs/srv/SetMode "{base_mode: 0, custom_mode: 'AUTO.TAKEOFF'}"
```
드론 1 시동 -> 이륙
```
ros2 service call /drone1/cmd/arming mavros_msgs/srv/CommandBool "{value: true}"
```
드론 1 착륙
```
ros2 service call /drone1/set_mode mavros_msgs/srv/SetMode "{base_mode: 0, custom_mode: 'AUTO.LAND'}"
```