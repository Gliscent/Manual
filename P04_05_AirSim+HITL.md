
VSPE 다운
split 선택


param set SYS_HITL 1
param set COM_ARM_WO_GPS 1
param set CBRK_USB_CHK 197848
param set EKF2_AID_MASK 1
param set COM_POSCTL_NAVL 0
param set COM_HOME_IN_AIR 1
param set NAV_RCL_ACT 0
param set EKF2_AID_MASK 1
param save


settings.json 파일
```
{
  "SettingsVersion": 1.2,
  "SimMode": "Multirotor",
  "ClockType": "SteppableClock",
  "OriginGeopoint": {
    "Latitude": 37.5585,
    "Longitude": 126.9386,
    "Altitude": 0
  },

  "Vehicles": {
    "Drone1": {
      "VehicleType": "PX4Multirotor",
      "X": 4,
      "Y": 0,
      "Z": -2,
      "Yaw": -180,
      "UseSerial": true,
      "SerialPort": "COM4",
      "BaudRate": 115200,
      "Lockstep": false,
      "PX4DebugMode": false,
      "Sensors": {
        "GpsSensor": {
          "SensorType": 3,
          "Enabled": true
        },
        "ImuSensor": {
          "SensorType": 2,
          "Enabled": true
        },
        "Barometer": {
          "SensorType": 1,
          "Enabled": true
        }
      }

    }
  }
}
}





```