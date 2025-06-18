Airsim + ROS2 jazzy (ubuntu 24.04)
---
ROS랑 똑같음. 우선 P03_02 하고 오기. 

## 1. PX4 설치 (P01 참고)

## 2. 의존성 설치 (정책만 살짝 무시함)
```
sudo apt update && sudo apt upgrade
sudo apt install python3-pip
sudo apt install python3-kconfiglib
pip3 install --user pyros-genmsg empy jinja2 toml numpy --break-system-packages
```


## 2. bashrc에 관련 내용 추가
```
export PX4_SIM_HOST_ADDR=(윈도우 컴 ip)
```

alias px4="cd; cd PX4-Autopilot; make px4_sitl none_iris"