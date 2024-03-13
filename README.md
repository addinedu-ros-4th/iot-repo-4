# 📮스마트 우편함 - IoT Project📮


<img src="https://img.shields.io/badge/C++-00599C?style=flat-square&logo=C%2B%2B&logoColor=white"/> <img src="https://img.shields.io/badge/GitHub-181717?style=flat-square&logo=GitHub&logoColor=white"/> <img src="https://img.shields.io/badge/MySQL-4479A1?style=flat-square&logo=MySQL&logoColor=white"/> <img src="https://img.shields.io/badge/PYTHON-87CEFA?style=flat-square&logo=PYTHON&logoColor=white"/> <img src="https://img.shields.io/badge/ARDUINO-48D1CC?style=flat-square&logo=ARDUINO&logoColor=white"/> <img src="https://img.shields.io/badge/QT-00FF00?style=flat-square&logo=QT&logoColor=white"/> <img src="https://img.shields.io/badge/MQTT-9400D3?style=flat-square&logo=MQTT&logoColor=WHITE"> ![image](https://github.com/addinedu-ros-4th/iot-repo-4/assets/155615876/f9704f71-1971-4a97-be41-fa106425b112) ![image](https://github.com/addinedu-ros-4th/iot-repo-4/assets/155615876/e36fe4a3-2312-4af1-aeed-120dbfe09a2d) ![image](https://github.com/addinedu-ros-4th/iot-repo-4/assets/155615876/7d745aa3-d6b2-4fdc-a75f-8db120558782) ![image](https://github.com/addinedu-ros-4th/iot-repo-4/assets/155615876/7520970f-77ea-4ce5-835d-b3a11dfc4ef6)




---


#  1 프로젝트 소개
### 프로젝트 목표
    1. Arduino와 pyqt를 모두 사용할 수 있는 스마트 우편함 시스템을 설계
    2. MQTT를 통한 WIFI 통신
    3. 센서들을 통한 실시간 데이터로 데이터베이스 구축
    
### 1.2 프로젝트 팀 소개

[김영환](https://github.com/earnest99) - 리더 / Python / PYQT / HW 

[김진홍](https://github.com/sna145815) - PYQT / Database 

[곽준](https://github.com/junroun) - Arduino / MQTT

[유겸희](https://gist.github.com/kyemhee) - Arduino / HW

---
# 2 Hardware
1. Arduino Uno & WIFI ESP8266 Module
2. Servo Motor
3. I2C LCD 1602 Display board
4. JM101-fingerprint sensor
5. Ultrasonic Ranging Module HR -SR04 Sensor
6. Battery
   
![image](https://github.com/addinedu-ros-4th/iot-repo-4/assets/155615876/59a3e5db-1591-42d7-9f50-cfc0303d01ce)![image](https://github.com/addinedu-ros-4th/iot-repo-4/assets/155615876/6e66dd19-c054-402e-96e1-e2cddca32b4d)
![image](https://github.com/addinedu-ros-4th/iot-repo-4/assets/155615876/b3354dce-4425-4f25-b88a-53bb1fe1b6bf)
![image](https://github.com/addinedu-ros-4th/iot-repo-4/assets/155615876/2a040fd5-2f19-4aba-9e3f-39507d894bee)
![image](https://github.com/addinedu-ros-4th/iot-repo-4/assets/155615876/a64e189c-5e20-4ca9-bcf8-a1022bad5301)
![image (4)](https://github.com/addinedu-ros-4th/iot-repo-4/assets/155615876/dfed3590-8e16-493d-89e2-b0496eebb186)

---
# 3 Software
1. Arduino
   
![image](https://github.com/addinedu-ros-4th/iot-repo-4/assets/155615876/a745961a-6f5d-49ab-8d65-a62d86592951)
---
2. Pyqt

![image](https://github.com/addinedu-ros-4th/iot-repo-4/assets/155615876/20e87a1b-cd4d-4718-9a08-12feeb699f60)
---
3. MQTT
   
![image](https://github.com/addinedu-ros-4th/iot-repo-4/assets/155615876/26d33bd5-e4b1-424c-aae4-0d29815c0802)

---
# 4. 프로젝트 설명
### 4.1 기능 리스트
![Screenshot from 2024-03-12 13-21-33](https://github.com/addinedu-ros-4th/iot-repo-4/assets/155615876/4adbd0ff-f13a-4ab0-ad05-bc0650e82bdd)

### 4.2 시스템 흐름 / Flow Chart
HW 시스템 흐름도

![Screenshot from 2024-03-12 13-12-46](https://github.com/addinedu-ros-4th/iot-repo-4/assets/155615876/03159c3d-1e8f-4c63-b9d4-65a017e2e240)
---
PYQT 시스템 흐름도
<img src = "https://github.com/addinedu-ros-4th/iot-repo-4/assets/155615876/062036ea-7bc8-484d-9f56-745b282f93df" width="100%" height="75%">


### 4.3 MQTT 프로토콜
![Screenshot from 2024-03-12 13-19-41](https://github.com/addinedu-ros-4th/iot-repo-4/assets/155615876/e5614861-72b5-4b50-b746-80fd1d5050af)

### 4.4 Database 구성
<img src = "https://github.com/addinedu-ros-4th/iot-repo-4/assets/155615876/e6767b36-fc04-4eab-8dca-79a47809a37d" width="25%" height="25%"> <img src = "https://github.com/addinedu-ros-4th/iot-repo-4/assets/155615876/18426162-b3d3-46a8-bafb-41550980bd2f" width="25%" height="25%"> <img src = "https://github.com/addinedu-ros-4th/iot-repo-4/assets/155615876/60d50f4a-9a8f-4900-8ced-aed5d0cc872b" width="25%" height="25%">

---
# 5 디자인
### 5.1 Design
![Screenshot from 2024-03-12 16-58-59](https://github.com/addinedu-ros-4th/iot-repo-4/assets/155615876/1114178e-1f74-4299-93d0-a301f4850296)

### 5.2 Model
<img src = "https://github.com/addinedu-ros-4th/iot-repo-4/assets/155615876/c5c8bf69-bd16-493f-abb4-c0cdff55df74" width="50%" height="50%">

---
# 6 시연영상
[![IMAGE ALT TEXT HERE](https://img.youtube.com/vi/i6gyzcIRdr0/0.jpg)](https://www.youtube.com/watch?v=i6gyzcIRdr0)

# MQTT 설치
    $ sudo apt-get install mosquitto
    $ sudo apt install mosquitto-clients

