import paho.mqtt.client as mqtt
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import uic
from qt_material import apply_stylesheet
import mysql.connector
from datetime import datetime
from PyQt5.QtCore import QTimer,QObject, pyqtSignal
from_class = uic.loadUiType("sub2.ui")[0]

class Signal(QObject):
    timer_start_signal = pyqtSignal()
    timer_stop_signal = pyqtSignal()
    show_mail_signal = pyqtSignal()
    
class WindowClass(QMainWindow, from_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.text.setStyleSheet('color:navy;background:white')
        self.p_count.setText("0")
        # 사용자 정보
        self.auth = {
            'username': "jun",
            'password': "gg5860ktm"
        }
        # MySQL 연결 설정
        self.connection = mysql.connector.connect(
                host="34.64.119.253",
                user="root",
                password="qwer1234",
                database="Project"
            )

        # DB 연결
        self.connect_to_mysql()
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
        
        # 타이머 설정
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.timer_timeout)
        # 타이머 상태를 나타내는 변수
        self.timer_active = False

        # 시그널 객체 생성
        self.signal = Signal()
        self.signal.timer_start_signal.connect(self.timer_start)
        self.signal.timer_stop_signal.connect(self.timer_stop)
        self.signal.show_mail_signal.connect(self.show_mail_message)

    def timer_start(self):
        self.timer_count = 0
        self.timer.start(1000)

    def timer_stop(self):
        self.timer.stop()

    def timer_timeout(self):
        # 타이머가 만료될 때마다 실행되는 함수
        self.timer_count += 1
        #print(self.timer_count)
        if self.timer_count >= self.timer_count %60 == 0:  # 타이머 값이 60초가 지나면
            self.signal.show_mail_signal.emit()

    def show_mail_message(self):
        current_text = self.text.text()
        current_time = datetime.now()
        formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
        text = current_text + '\n' + formatted_time + '\t' + '우편물 찾아가세요!'
        self.text.setText(text)
        
    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print("Connected to the broker")
            # 구독할 토픽을 설정
            client.subscribe("post/door")
            client.subscribe("post/open")
            client.subscribe("post/sensor")
            client.subscribe("post/doorstate")
        else:
            print(f"Connection failed with result code {rc}")

    def on_message(self, client, userdata, msg):
        # 받은 메시지 처리
        print(f"Received message on topic {msg.topic}: {msg.payload.decode()}")
        if msg.topic == 'post/door':
            if msg.payload.decode() == 'door is open.':
                content = 'OPEN'
                self.signal.timer_stop_signal.emit()
                self.timer_active = False
            else:
                content = 'CLOSE'
            self.insert_log(content)
        elif msg.topic == 'post/open':
            content = 'OPEN'
            self.insert_log(content)
        elif msg.topic == 'post/sensor':
            content = 'INPUT'
            self.insert_log(content)
            if self.timer_active == False:
                self.signal.timer_start_signal.emit()
                self.timer_active = True
            
        self.addText(msg)

    
            
    def insert_log(self,content):
        query = "INSERT INTO LOG_TABLE (EVENT_TIME, CONTENT) VALUES (%s, %s)"
        cur = self.connection.cursor()
        cur.execute(query, (datetime.now(), content))
        self.connection.commit()
        
    def addText(self, msg):
        input_text = msg.payload.decode()
        current_time = datetime.now()
        formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
        if msg.topic == 'post/sensor':
            self.p_count.setText(input_text)
            current_text = self.text.text()
            text = current_text+'\n'+formatted_time + '\t' + '우편물 도착 !!'
            self.text.setText(text)
        elif msg.topic == 'post/door':
            self.p_state.setText(input_text)
            if (msg.payload.decode() == "door is close."):
                self.clearText()
            else:
                current_text = self.text.text()
                text = current_text+'\n'+formatted_time + '\t' + '문열림 !!'
                self.text.setText(text)
        elif msg.topic == 'post/doorstate':
            current_text = self.text.text()
            text = current_text+'\n'+formatted_time + '\t' + input_text
            self.text.setText(text)



    def clearText(self):
        self.text.clear()
        self.p_count.setText("0")
        
    def connect_to_mysql(self):
        try:
            if self.connection.is_connected():
                print("MySQL에 연결되었습니다.")
                # 여기에 추가적인 작업 수행

                #self.connection.close()  # 연결 종료

        except mysql.connector.Error as error:
            print("MySQL 연결 오류:", error)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    myWindows = WindowClass()
    
    apply_stylesheet(app, theme='dark_medical.xml')

    myWindows.show()
    
    sys.exit(app.exec_())
