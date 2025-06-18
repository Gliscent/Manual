Airsim + Ubuntu(VMWare) + Firmware (PX4, Ardupilot)
---

## 1. 에어심 기본 메뉴얼

https://www.youtube.com/watch?v=3qOQsIWpgtM

#### ControlIp = 리눅스 ip

#### LocalhostIp = 윈도우 ip

#### HostAddr = 윈도우 ip

## 2. 에어심 작동법

#### 1. C:\Users\user\Documents\Unreal Projects\"MyProject"

에서 .sln 비쥬얼 스튜디오 실행 후 local windows debugger + 에어심에서 "play"

#### 2. 우분투/vmware 실행 후, cmd에서

```ssh park@~~```
입력 후 (id랑 ip는 알아서 찾기), ```cd; cd PX4-Autopilot; make px4_sitl none_iris```

#### 3.

```bash
commander takeoff
commander land
```

#### ~/.bashrc
```
export PX4_SIM_HOST_ADDR=(윈도우 컴 ip)
```