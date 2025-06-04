Ubuntu(VMWare) + Pixhawk Firmware (PX4, Ardupilot)
---
VMWare는 윈도우에서 우분투를 돌리게 하는 프로그램으로, 리눅스 OS일 경우 VMWare 설치 X wow

## 1. 우분투 서버 설치
https://ubuntu.com/download/server

## 2. VMWare 설치 및 가이드
https://ubuntu.com/download/server

1) Create a New Virtual Machine 클릭
2) Browse --> 우분투 서버 설치 경로
3) 용량 선택에서 적어도 30Gb
4) split --> store
5) ubuntu-lv 설정된 용량에서 더 늘리기 (ex 13.996 --> 27.996)
6) Install OpenSSH server 는 체크
7) 위 과정 후 reboot --> failed cdrom이 뜨면 i finished installing 클릭 
8) ```service --status-all ``` 명령어로  ssh가 [-] 상태로 있는지 확인. 그럴 경우, ```bash sudo systemctl start ssh``` 로 서비스 활성화
9) ```ip addr``` 으로 inet (inet 숫자) 확인 후 기억
10) ```ssh (id이름)@(inet 숫자)``` 만약 안되면, ```ssh-keygen -R (inet 숫자)```

VMWare 종료 시, ```sudo shutdown -h now```

## 3. PX4 펌웨어 빌드
PX4 git 파일 복사
```bash 
git clone --recursive https://github.com/PX4/PX4-Autopilot.git
```
파일 열기

```bash
bash ./PX4-Autopilot/Tools/setup/ubuntu.sh
cd PX4-Autopilot
```

사용 예시 : https://docs.px4.io/main/ko/dev_setup/building_px4.html

## 4. Ardupilot 펌웨어 빌드

ArduPilot git 파일 복사
```bash 
git clone --recurse-submodules https://github.com/ArduPilot/ardupilot.git
```
파일 열기

```bash
ardupilot/Tools/environment_install/install-prereqs-ubuntu.sh -y
cd ardupilot
```