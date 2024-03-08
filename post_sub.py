import paho.mqtt.client as mqtt
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import uic
from qt_material import apply_stylesheet


from_class = uic.loadUiType("post_proj/sub.ui")[0]

class WindowClass(QMainWindow, from_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.text.setStyleSheet('color:navy;background:white')
        # 사용자 정보
        self.auth = {
            'username': "jun",
            'password': "gg5860ktm"
        }

        # MQTT 클라이언트 생성
        self.client = mqtt.Client()
        

        # 연결 이벤트에 대한 콜백 함수 등록
        self.client.on_connect = self.on_connect
        

        # 메시지 수신에 대한 콜백 함수 등록
        self.client.on_message = self.on_message

        # 브로커에 연결
        self.client.username_pw_set(username=self.auth['username'], password=self.auth['password'])
        self.client.connect("192.168.0.5", 1883)

        # 루프 시작 (메시지 수신 대기)
        self.client.loop_start()



    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print("Connected to the broker")
            # 구독할 토픽을 설정
            client.subscribe("post/door")
            client.subscribe("post/sensor")
        else:
            print(f"Connection failed with result code {rc}")

    def on_message(self, client, userdata, msg):
        # 받은 메시지 처리
        print(f"Received message on topic {msg.topic}: {msg.payload.decode()}")
        self.addText(msg)

    def addText(self, msg):
        input_text = msg.payload.decode()
        self.p_state.clear()
        self.p_state.setText(input_text)
        
        if msg.topic == 'post/sensor':
            self.p_count.setText(input_text)
            
        else :
            current_text = self.text.text()
            text = current_text+'\n'+input_text
            self.text.setText(text)

    def clearText(self):
        self.lineEdit.clear()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    myWindows = WindowClass()
    
    apply_stylesheet(app, theme='dark_medical.xml')

    myWindows.show()
    
    sys.exit(app.exec_())