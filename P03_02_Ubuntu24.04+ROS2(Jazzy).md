Ubuntu + ROS2 (Jazzy)
---
Ubuntu 20.04에서만 가능함. 아래 명령어들은 드론과 관련이 있음.

ROS2 적기

## 1. ROS2 설치

locale 설치
```
sudo apt update && sudo apt install locales
sudo locale-gen en_US en_US.UTF-8
sudo update-locale LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8
export LANG=en_US.UTF-8
```

저장소 할당
```
sudo apt install software-properties-common
sudo add-apt-repository universe
```

api 설정
```
sudo apt update && sudo apt install curl -y
export ROS_APT_SOURCE_VERSION=$(curl -s https://api.github.com/repos/ros-infrastructure/ros-apt-source/releases/latest | grep -F "tag_name" | awk -F\" '{print $4}')
curl -L -o /tmp/ros2-apt-source.deb "https://github.com/ros-infrastructure/ros-apt-source/releases/download/${ROS_APT_SOURCE_VERSION}/ros2-apt-source_${ROS_APT_SOURCE_VERSION}.$(. /etc/os-release && echo $VERSION_CODENAME)_all.deb"
sudo apt install /tmp/ros2-apt-source.deb
```

설치 드가자
```
sudo apt update && sudo apt install ros-dev-tools
sudo apt update && sudo apt upgrade
sudo apt install ros-jazzy-desktop
```

```
echo "source /opt/ros/jazzy/setup.bash" >> ~/.bashrc
```

## 2. colcon 설치
엄청 간단함
```
sudo apt update
sudo apt install python3-colcon-common-extensions
```

## 3. 워크 스페이스 생성
```
mkdir -p ~/ros2_ws/src
cd ~/ros2_ws
colcon build
echo "source ~/ros2_ws/install/setup.bash" >> ~/.bashrc
```

## 번외/필요 사항은 P03_01 참고