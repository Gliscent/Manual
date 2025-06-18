Ubuntu + ROS2 (Galactic)
---
Ubuntu 20.04에서만 가능함. 아래 명령어들은 드론과 관련이 있음.

## 1. ROS2 galactic 설치

```bash
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
```

## 2. .bashrc 아랫줄에 내용 추가
우선 ```nano ~/.bashrc``` 로 진입. 그 안에 아래 내용 작성

```bash
alias nb="nano ~/.bashrc"
alias sb="source ~/.bashrc; echo "Bashrc is reloaded""
alias galactic="echo "ROS2 Galatic is activated"; ros_domain; source /opt/ros/galactic/setup.bash"
alias ros_domain="export ROS_DOMAIN_ID=216"
alias rs="echo "ros2_study is activated"; galactic; source ~/ros2_study/install/local_setup.bash"
alias cb="colcon build
source ~/ros2_study/install/setup.bash
source /opt/ros/galactic/setup.bash
```

## 3. colcon 설치

```bash
sudo apt update && sudo apt install -y
python3-pip
python3-pytest-cov
ros-dev-tools

python3 -m pip install -U
flake8-blind-except
flake8-builtins
flake8-class-newline
flake8-comprehensions
flake8-deprecated
flake8-docstrings
flake8-import-order
flake8-quotes
pytest-repeat
pytest-rerunfailures
pytest
setuptools

sudo apt install python3-colcon-common-extensions
```

패키지 선택 후 컴파일 가능
```bash
colcon build --packages-select apf_package
```

## 4. 드론 관련 환경 빌드

```bash
mkdir -p ~/ros2_study
sudo apt install tree
sudo apt install ros-galactic-turtlesim
sudo apt-get update sudo apt-get upgrade
sudo apt-get install python3-pip
sudo apt-get install python3-dev
pip install --upgrade pip
sudo pip install future
sudo apt-get install screen wxgtk libxml libxlts
sudo pip install pyserial
sudo pip install dronekit
sudo pip install MAVProxy
sudo apt-get update
source ~/.bashrc
sb
git clone "https://github.com/(깃허브사용자이름)/src.git"
```

그 후, 원하는 파일 위치에 가고 colcon build
```bash
cb
```

## 번외 내용
### 1. 와이파이 연결
```bash
sudo nano /etc/netplan/50-cloud-init.yaml
```
이후, ssid, pw 수정.
```bash
sudo reboot
ifconfig wlan0
```
위의 과정으로도 와이파이가 안잡히면 랜선 연결.

### 2. ssh 활성화 (내용이 부정확)
우분투 쪽에서 입력
```bash
sudo ssh-keygen -t rsa -f /ect/ssh/ssh_host_rsa_key -N ''
```
연결하는 쪽에서 입력
```bash
ssh-keygen -R 192.168.0.X
```

### 라즈베리 파이에서 gui 설치
```bash
sudo apt-get update
sudo apt-get upgrade
sudo apt-get install ubuntu-desktop
```