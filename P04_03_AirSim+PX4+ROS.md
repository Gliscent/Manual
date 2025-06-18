Airsim + ROS noetic
---

이 메뉴얼을 진행하기 전에 사전 지식이 필요함.
에어심을 다루는 데에 2가지 방식이 있음.
(1) airsim 패키지 노드 사용. 아래 3, 4, 5번이 이와 관련된 항목
(2) mavlink 프로토콜 노드 사용. 6번이 이와 관련된 항목

airsim 패키지 노드를 사용 안해도 되지만, 나중에 이미지 처리까지 목표로 한다면 따라하고, 
이 메뉴얼을 만들 때는 목차에 따라 순차적으로 진행했기 때문에 유동적으로 메뉴얼 따라하기.

## 1. ROS 설치 & Catkin 설치
```bash
sudo apt-get install gcc-8 g++-8

# 저장소 등록
sudo sh -c 'echo "deb http://packages.ros.org/ros/ubuntu $(lsb_release -sc) main" > /etc/apt/sources.list.d/ros-latest.list'
sudo apt install curl gnupg -y
curl -s https://raw.githubusercontent.com/ros/rosdistro/master/ros.asc | sudo apt-key add -
sudo apt update

# ROS noetic짱 설치
sudo apt install ros-noetic-desktop-full

# Catkin 설치
pip install "git+https://github.com/catkin/catkin_tools.git#egg=catkin_tools"

echo "source /opt/ros/noetic/setup.bash" >> ~/.bashrc
source ~/.bashrc

```

## 2. Catkin 환경 빌드
```bash

# ROS 관련
sudo apt install python3-rosdep python3-rosinstall python3-rosinstall-generator python3-wstool build-essential
sudo rosdep init
rosdep update

# 혹시 모를 초기화
cd
rm -rf ~/.catkin_tools
rm -rf ~/build ~/devel ~/logs ~/install

# Catkin 워크스페이스 관련
mkdir -p ~/catkin_ws/src
cd ~/catkin_ws
catkin init

# 의존성 설치
cd ~/catkin_ws
wstool init ~/catkin_ws/src
rosinstall_generator --upstream mavros | tee /tmp/mavros.rosinstall
rosinstall_generator mavlink | tee -a /tmp/mavros.rosinstall
wstool merge -t src /tmp/mavros.rosinstall
wstool update -t src
rosdep install --from-paths src --ignore-src --rosdistro `echo $ROS_DISTRO` -y
catkin build

echo "source ~/catkin_ws/devel/setup.bash" >> ~/.bashrc
source ~/.bashrc
```


## 3. 에어심 빌드 (선택)
```bash
git clone https://github.com/Microsoft/AirSim.git;
cd AirSim;
./setup.sh;
./build.sh;

```

## 4. Airsim ROS 패키지 빌드 (선택)
```bash
cd 
rm -rf .catkin_tools
rm -rf ~/build ~/devel ~/logs
cd ~/AirSim/ros
catkin init
catkin config --source-space src
catkin build
```

## 5. VMware 설정 (선택)
#### 1. 왼쪽 상단에 Player > Manage > Virtual Machine Settings > Network Adapter > Bridged 선택
#### 2. 재부팅
#### 3. 브릿지 노드 실행 (airsim 드론의 정보를 가져옴)
#### 4. IP 주소 변경
##### 1) 에어심 쪽 setting.json 에서 IP 변경 (내 컴퓨터 기준 -> "ControlIp": "192.168.10.13", "LocalHostIp": "192.168.10.5")
##### 2) ~/.bashrc 에서 export PX4_SIM_HOST_ADDR IP 변경
####  5. airsim topic 확인 ```rostopic list```

## 6. Mavlink 프로토콜 UDP 노드

혹시 PX4 펌웨어를 아직 안 다운 받았으면 메뉴얼 P01 참고.

아래 나올 내용은 airsim 패키지가 아니라 mavlink 통신 노드로 접근.

윈도우 쪽 airsim 정보를 가져오지 않고, 직접 PX4에서 정보를 종합.

그래서 mavlink 통신을 할 때 보낼 주소를 UDP 127.0.0.1로 로컬화.

아래 진행하기 전에 인스턴스 확인 (-i X 에서 X숫자가 tcp 포트와 일치하는지 체크)

### 터미널1
```
cd PX4-Autopilot
PX4_SIM_MODEL=none_iris ./build/px4_sitl_default/bin/px4 -i 0 ./ROMFS/px4fmu_common -s etc/init.d-posix/rcS -d "mavlink stop-all; mavlink start -u 14580 -r 4000000 -m onboard -o 14540 -t 127.0.0.1"
```

### 터미널2
```
cd PX4-Autopilot
PX4_SIM_MODEL=none_iris ./build/px4_sitl_default/bin/px4 -i 1 ./ROMFS/px4fmu_common -s etc/init.d-posix/rcS -d "mavlink stop-all; mavlink start -u 14581 -r 4000000 -m onboard -o 14541 -t 127.0.0.1"
```

### 터미널3
편의상 .launch 파일을 만들어야 함.
혹시 잘 진행이 안된다면 ```mavlink status``` 로 UDP 포트 번호 보기

launch 파일은 가장 편한 위치에 생성.
```
nano multi_mavros.launch
```

```bash
<launch>
  <group ns="drone1">
    <node pkg="mavros" type="mavros_node" name="mavros1" output="screen">
      <param name="fcu_url" value="udp://127.0.0.1:14540@127.0.0.1:14580" />
      <param name="tgt_system" value="1"/>
      <param name="system_id" value="1"/>
    </node>
  </group>

  <group ns="drone2">
    <node pkg="mavros" type="mavros_node" name="mavros2" output="screen">
      <param name="fcu_url" value="udp://127.0.0.1:14541@127.0.0.1:14581" />
      <param name="tgt_system" value="2"/>
      <param name="system_id" value="2"/>
    </node>
  </group>
</launch>
```

```
roslaunch multi_mavros.launch
```

### 나머지 터미널

원하는 명령어 예시

```
rostopic list
```

```
rostopic echo /drone1/mavros1/local_position/pose
```

```
rostopic echo /drone2/mavros2/local_position/pose
```

```
# 이륙 모드 on (기본 고드 바꾸려면 PX4에서 변경)
rosservice call /drone1/mavros1/set_mode "base_mode: 0
custom_mode: 'AUTO.TAKEOFF'"

# 시동->이륙
rosservice call /drone1/mavros1/cmd/arming "value: true"

# 착륙
rosservice call /drone1/mavros1/set_mode "base_mode: 0 
custom_mode: 'AUTO.LAND'"
```