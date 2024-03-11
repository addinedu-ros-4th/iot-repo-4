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


connection = mysql.connector.connect(
                host="34.64.119.253",
                user="root",
                password="qwer1234",
                database="Project"
            )    
class Signal(QObject):
    timer_start_signal = pyqtSignal()
    timer_stop_signal = pyqtSignal()
    show_mail_signal = pyqtSignal()

class Logmodal(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi("log.ui",self)
        self.textBrowser.setStyleSheet('color:black;background:white')
        self.get_log()  # 로그를 가져와서 표시
        self.show()
        
    def get_log(self):
        # 데이터베이스에서 모든 레코드 가져오기
        cur = connection.cursor()
        cur.execute("SELECT * FROM LOG_TABLE")
        logs = cur.fetchall()

          #로그를 표 형식으로 포맷
        formatted_logs = ""
        for log in logs:
            # 로그 시간 정보에서 소수점 이하 정보 제거
            log_time_str = str(log[0]).split('.')[0]  # 로그 시간 정보에서 소수점 이하 정보 제거
            formatted_logs += "{:<30} {:<20}\n".format(log_time_str, log[1])

        # 로그를 텍스트 브라우저에 추가
        self.textBrowser.append(formatted_logs)
        
            
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
        self.user=""
        # MySQL 연결 설정
        

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
        self.client.connect("192.168.0.8", 1883)

        # 루프 시작 (메시지 수신 대기)
        self.client.loop_start()
        
        self.textlinecnt = 0
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
        #모달
        self.pushButton.clicked.connect(self.logmodal)
        
    def logmodal(self):
        window_2 = Logmodal()
        window_2.exec_()
        
        
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
            client.subscribe("post/sensor")
            client.subscribe("post/doorstate")
            client.subscribe("post/id")
        else:
            print(f"Connection failed with result code {rc}")

    def on_message(self, client, userdata, msg):
        # 받은 메시지 처리 
        print(f"Received message on topic {msg.topic}: {msg.payload.decode()}")
        if msg.topic == 'post/door':
            if msg.payload.decode() == 'door is open':
                content = '문열림'
                self.signal.timer_stop_signal.emit()
                self.timer_active = False
            else:
                content = '문닫힘'
        elif msg.topic == 'post/sensor':
            content = '우편물 도착'
            self.insert_mail()
            if self.timer_active == False:
                self.signal.timer_start_signal.emit()
                self.timer_active = True
        elif msg.topic == 'post/id': 
            if self.isfound() == 0:
                 return
            self.update_mailfound()
            id = msg.payload.decode()
            self.user = self.getuser(id)
            content = self.user+'님이 수거함'
        elif msg.topic == 'post/doorstate': 
            self.addText(msg)
            return
        self.insert_log(content)    
        self.addText(msg)

    def isfound(self):
        cur = connection.cursor()
        cur.execute("SELECT count(*) FROM MAIL m WHERE ISFOUND ='FALSE'")
        user = cur.fetchone()
        if user[0] == 0:
            return 0
        else:
            return 1
        
        
    def getuser(self,id):
        cur = connection.cursor()
        cur.execute("SELECT * FROM AUTH WHERE ID = %s", (id,))
        user = cur.fetchone()
        return user[1] if user else ""
    
    def update_mailfound(self):
        query = "UPDATE MAIL SET ISFOUND = 'TRUE'"
        cur = connection.cursor()
        cur.execute(query)
        connection.commit()
        
    def insert_mail(self):
        query = "INSERT INTO MAIL (EVENT_TIME, ISFOUND) VALUES (%s,%s)"
        cur = connection.cursor()
        cur.execute(query,(datetime.now(), "FALSE"))
        connection.commit()   
                 
    def insert_log(self,content):
        if content =='x':
            return
        query = "INSERT INTO LOG_TABLE (EVENT_TIME, CONTENT) VALUES (%s, %s)"
        cur = connection.cursor()
        cur.execute(query, (datetime.now(), content))
        connection.commit()
        
    def addText(self, msg):
        self.textlinecnt += 1
        if self.textlinecnt == 17:
            current_text = ''
            self.textlinecnt = 0
            self.clearText()
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
            if (msg.payload.decode() == "door is close"):
                self.p_count.setText("0")
                current_text = self.text.text()
                text = current_text+'\n'+formatted_time + '\t' + '문닫음 !!'
                self.text.setText(text)
                self.p_count.setText("0")
            else:
                current_text = self.text.text()
                text = current_text+'\n'+formatted_time + '\t' + '문열림 !!'
                self.text.setText(text)
        elif msg.topic == 'post/doorstate':
            current_text = self.text.text()
            text = current_text+'\n'+formatted_time + '\t' + input_text
            self.text.setText(text)
        elif msg.topic == 'post/id':
            current_text = self.text.text()
            text = current_text+'\n'+formatted_time + '\t' + self.user+'님이 수거함'
            self.text.setText(text)



    def clearText(self):
        self.text.clear()
        self.p_count.setText("0")
        
    def connect_to_mysql(self):
        try:
            if connection.is_connected():
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
