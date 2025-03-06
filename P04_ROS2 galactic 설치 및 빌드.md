## ROS2 설치 및 빌드

#### 우분투 20.04, 파이썬 3.9 에서만 작동합니다! 중요합니다!


### 1. ROS2 galactic 설치

sudo apt update && sudo apt install locales

sudo locale-gen en_US en_US.UTF-8

sudo update-locale LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8

export LANG=en_US.UTF-8

sudo apt install software-properties-common

sudo add-apt-repository universe

sudo apt update && sudo apt install curl

sudo curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key -o /usr/share/keyrings/ros-archive-keyring.gpg

echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu $(. /etc/os-release && echo $UBUNTU_CODENAME) main" | sudo tee /etc/apt/sources.list.d/ros2.list > /dev/null

sudo apt update

sudo apt install ros-galactic-desktop

ls /etc/apt/sources.list.d/


### 2. .bashrc 아랫줄에 추가

alias nb="nano ~/.bashrc"

alias sb="source ~/.bashrc; echo \"Bashrc is reloaded\""

alias galactic="echo \"ROS2 Galatic is activated\"; ros_domain; source /opt/ros/galactic/setup.bash"

alias ros_domain="export ROS_DOMAIN_ID=216"

alias rs="echo \"ros2_study is activated\"; galactic; source ~/ros2_study/install/local_setup.bash"

alias cb="colcon build

source ~/ros2_study/install/setup.bash

source /opt/ros/galactic/setup.bash


### 3. colcon 설치

sudo apt update && sudo apt install -y \
python3-pip \
python3-pytest-cov \
ros-dev-tools
  
python3 -m pip install -U \
flake8-blind-except \
flake8-builtins \
flake8-class-newline \
flake8-comprehensions \
flake8-deprecated \
flake8-docstrings \
flake8-import-order \
flake8-quotes \
pytest-repeat \
pytest-rerunfailures \
pytest \
setuptools
  
sudo apt install python3-colcon-common-extensions


cb로 특정 패키지 컴파일 가능
colcon build --packages-select apf_package


### 4. 드론을 다루기 위한 파이썬 환경 빌드

mkdir -p ~/ros2_study

sudo apt install tree

sudo apt install ros-galactic-turtlesim


sudo apt-get update
sudo apt-get upgrade

sudo apt-get install python3-pip

sudo apt-get install python3-dev

pip install --upgrade pip

sudo pip install future

sudo apt-get install screen wxgtk libxml libxlts

sudo pip install pyserial

sudo pip install dronekit

sudo pip install MAVProxy

sudo apt-get update

위의 과정이 끝나면
cd ros2_study

source ~/.bashrc

sb

git clone "https://github.com/(깃허브사용자이름)/src.git"

cb


## 우분투를 다루면서 필요할 만한 내용


### 1. 와이파이 연결

sudo nano /etc/netplan/50-cloud-init.yaml

(와이파이 ssid, 비번 수정하고)

sudo reboot

ifconfig wlan0

위의 과정에서 와이파이가 안잡히면 랜선 연결


### 2. ssh 활성화

sudo ssh-keygen -t rsa -f /ect/ssh/ssh_host_rsa_key -N '' (이건... 잘 기억이 안난다..)

ssh-keygen -R 192.168.0.X (이건 연결하려는 컴퓨터 쪽에서)


### 3. 라즈베리 파이에서 gui 보이게 하고 싶을 때

sudo apt-get update

sudo apt-get upgrade

sudo apt-get install ubuntu-desktop
