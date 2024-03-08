from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIcon,QMovie,QColor,QPixmap
import speech_recognition as sr
from aip import AipSpeech
import sys
import pygame
import time
import threading
import webbrowser
from HandTrackingMain import handTrack

# Baidu Speech API, replace with your personal key
APP_ID = '32435706'
API_KEY = 'O2ihwguwMAfethvUvlAjGZ8l'
SECRET_KEY = 'XB107UzkLy6W8Qa5x1IqLKFTgQ7b4jNw'

client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)

class SplashScreen(QtWidgets.QSplashScreen):
    def __init__(self, pixmap):
        super().__init__(pixmap)


class HelpDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("帮助对话框")
        self.setGeometry(100, 100, 400, 300)

        palette = QtGui.QPalette()
        palette.setColor(QtGui.QPalette.Background, QtGui.QColor(210, 236, 255))
        self.setPalette(palette)

        animation_data = [
            (r"image\first.gif", 0, 0, 35, 35),
            (r"image\second1.gif", 0, 265, 35, 35),
            (r"image\second2.gif", 365, 265, 35, 35)
        ]

        for animation_path, x, y, width, height in animation_data:
            movie = QMovie(animation_path)
            label_gif = QtWidgets.QLabel(self)
            label_gif.setGeometry(QtCore.QRect(x, y, width, height))
            label_gif.setScaledContents(True)
            label_gif.setMovie(movie)
            movie.start()

        self.image_label_1 = QtWidgets.QLabel(self)
        self.image_label_1.setGeometry(QtCore.QRect(332, 0, 68, 35))
        pixmap = QPixmap(r"image\bilibili_logo.png")
        self.image_label_1.setPixmap(pixmap)
        self.image_label_1.setScaledContents(True)

        self.label = QtWidgets.QLabel(self)
        self.label.setGeometry(QtCore.QRect(150, 5, 391, 31))
        font = QtGui.QFont()
        font.setFamily("幼圆")
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label.setObjectName("label")
        self.label.setText("帮助面板")

        help_text = [
            "说出“打开哔哩哔哩”以打开哔哩哔哩网页版并开始手势识别",
            "仅伸出食指来控制鼠标移动",
            "食指和中指并拢表示单击鼠标左键",
            "张开食指和大拇指，根据张开的大小控制音量",
            "将所有手指张开来截图",
            "除大拇指以外张开表示滚轮下滑",
            "只有大拇指张开代表滚轮上滑",
            "随时说出“退出”以退出应用程序"
        ]
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        for i, text in enumerate(help_text):
            help_label = QtWidgets.QLabel(self)
            help_label.setGeometry(QtCore.QRect(50, 70 + 20 * i, 350, 20))
            help_label.setFont(font)
            help_label.setText(text)

        image_data = [
            (r'image\open.png', 20, 20, 30, 70),
            (r'image\食指.png', 20, 20, 30, 90),
            (r'image\食指中指.png', 20, 20, 30, 110),
            (r'image\食指拇指.png', 20, 20, 30, 130),
            (r'image\五指.png', 20, 20, 30, 150),
            (r'image\四指.png', 20, 20, 30, 170),
            (r'image\拇指.png', 20, 20, 30, 190),
            (r'image\exit.png', 20, 20, 30, 210)
        ]

        for image_path, width, height, x, y in image_data:
            label = QtWidgets.QLabel(self)
            pixmap = QPixmap(image_path)
            label.setFixedSize(width, height)
            label.setScaledContents(True)
            label.move(x, y)
            label.setPixmap(pixmap)


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(600, 450)
        icon = QIcon(r"image\bilibili.ico")
        MainWindow.setWindowIcon(icon)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        MainWindow.setFont(font)

        palette = QtGui.QPalette()
        palette.setColor(QtGui.QPalette.Background, QColor(210, 236, 255))
        MainWindow.setPalette(palette)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # Create and set the first GIF
        self.movie1 = QMovie(r"image\first.gif")
        self.label_1_gif = QtWidgets.QLabel(self.centralwidget)
        self.label_1_gif.setGeometry(QtCore.QRect(0, 0, 70, 70))
        self.label_1_gif.setMovie(self.movie1)
        self.movie1.start()

        # Create a QLabel widget to display the image
        self.image_label_1 = QtWidgets.QLabel(self.centralwidget)
        self.image_label_1.setGeometry(QtCore.QRect(70, 0, 137, 70))
        pixmap = QPixmap(r"image\bilibili_logo.png")
        self.image_label_1.setPixmap(pixmap)
        self.image_label_1.setScaledContents(True)

        # Create a QLabel widget to display the image
        self.image_label_2 = QtWidgets.QLabel(self.centralwidget)
        self.image_label_2.setGeometry(QtCore.QRect(210, 10, 326, 65))
        pixmap = QPixmap(r"image\view_logo.png")
        self.image_label_2.setPixmap(pixmap)
        self.image_label_2.setScaledContents(True)

        # Create and set the second GIF
        self.movie2 = QMovie(r"image\second.gif")
        self.label_2_gif = QtWidgets.QLabel(self.centralwidget)
        self.label_2_gif.setGeometry(QtCore.QRect(0, 350, 240, 105))
        self.label_2_gif.setMovie(self.movie2)
        self.movie2.start()

        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(110, 90, 391, 31))
        font = QtGui.QFont()
        font.setFamily("幼圆")
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label.setObjectName("label")

        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(130, 165, 321, 20))
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")

        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(130, 235, 281, 20))
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        font.setKerning(True)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")

        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(130, 305, 281, 20))
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        font.setKerning(True)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")

        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(240, 410, 191, 16))
        font = QtGui.QFont()
        font.setFamily("黑体")
        font.setBold(False)
        font.setWeight(10)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")

        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(440,410,100,16))
        font = QtGui.QFont()
        font.setFamily("黑体")
        font.setBold(False)
        font.setWeight(10)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")

        self.label_open = QtWidgets.QLabel(self.centralwidget)
        pixmap = QPixmap(r'image\open.png')
        self.label_open.setFixedSize(pixmap.width(), pixmap.height())
        self.label_open.move(90,160)
        self.label_open.setPixmap(pixmap)

        self.label_help = QtWidgets.QLabel(self.centralwidget)
        pixmap = QPixmap(r'image\help.png')
        self.label_help.setFixedSize(pixmap.width(), pixmap.height())
        self.label_help.move(90,230)
        self.label_help.setPixmap(pixmap)

        self.label_exit = QtWidgets.QLabel(self.centralwidget)
        pixmap = QPixmap(r'image\exit.png')
        self.label_exit.setFixedSize(pixmap.width(), pixmap.height())
        self.label_exit.move(90, 300)
        self.label_exit.setPixmap(pixmap)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 600, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.help_dialog = HelpDialog(MainWindow)

        def show_help_dialog():
            self.help_dialog.exec_()

        self.help_button = QtWidgets.QPushButton(self.centralwidget)
        self.help_button.setGeometry(QtCore.QRect(0, 0, 0, 0))
        self.help_button.setText("显示帮助")
        self.help_button.clicked.connect(show_help_dialog)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Video Viewing Assistant"))
        self.label.setText(_translate("MainWindow", "欢迎来到bilibili视频观看助手"))
        self.label_2.setText(_translate("MainWindow", "说出“打开哔哩哔哩”以打开哔哩哔哩网页版"))
        self.label_3.setText(_translate("MainWindow", "说出“帮助”以打开帮助面板"))
        self.label_4.setText(_translate("MainWindow", "说出“退出”以退出应用程序"))
        self.label_5.setText(_translate("MainWindow", "制作人：朱开来，郑皓予，陈华机"))
        self.label_6.setText(_translate("MainWindow", "Version:1.0.0"))


def start_thread():
    # 让create_ftp函数在子线程中运行
    thread = threading.Thread(target=create_ftp, args=())
    # 下面是设置守护线程：如果在程序中将子线程设置为守护线程，则该子线程会在主线程结束时自动退出
    thread.setDaemon(True)
    thread.start()  # 启动线程


def create_ftp():
    while True:
        rec()
        result = listen()
        if result == 3:
            app.quit()
        elif result == 2:
            ui.help_button.click()
        elif result == 1:
            enter_bilibili()
            break
        else:
            continue


def rec(rate=16000):
    r = sr.Recognizer()
    with sr.Microphone(sample_rate=rate) as source:
        print("请说话")
        audio = r.listen(source)

    with open("recording.wav", "wb") as f:
        f.write(audio.get_wav_data())


# 使用百度语音作为STT引擎
def listen():
    with open('recording.wav', 'rb') as f:
        audio_data = f.read()

        result = client.asr(audio_data, 'wav', 16000, {
            'dev_pid': 1536
        })
        try:
            result_text = result["result"][0]
            print("你说: " + result_text)

            if "打开" in result_text:
                pygame.mixer.init()
                pygame.mixer.music.load(r"sound\bilibili.wav")
                pygame.mixer.music.play()
                time.sleep(3)
                return 1
            elif result_text == "帮助":
                pygame.mixer.init()
                pygame.mixer.music.load(r"sound\help.wav")
                pygame.mixer.music.play()
                time.sleep(3)
                return 2
            elif result_text == "退出":
                pygame.mixer.init()
                pygame.mixer.music.load(r"sound\quit.wav")
                pygame.mixer.music.play()
                time.sleep(3)
                return 3
        except:
            print("没有识别到语音")

stop_event = threading.Event()

def enter_bilibili():
    webbrowser.open("https://www.bilibili.com")
    thread1 = threading.Thread(target=bilibili_rec)
    thread2 = threading.Thread(target=handTrack, args=(stop_event,))
    thread1.setDaemon(True)
    thread2.setDaemon(True)
    thread1.start()
    thread2.start()


def bilibili_rec():
    while not stop_event.is_set():
        rec()
        with open('recording.wav', 'rb') as f:
            audio_data = f.read()
            result = client.asr(audio_data, 'wav', 16000, {
                'dev_pid': 1536
            })
        try:
            result_text = result["result"][0]
            if "动态" in result_text:
                webbrowser.open("https://t.bilibili.com")
            elif "退出" in result_text:
                stop_event.set()
                app.quit()
            else:
                continue
        except:
            pass

if __name__ == "__main__":
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    app = QtWidgets.QApplication(sys.argv)

    splash_pixmap = QtGui.QPixmap(r"image\entry_page.png")
    splash_pixmap = splash_pixmap.scaled(QtCore.QSize(600, 450))
    splash = SplashScreen(splash_pixmap)
    splash.show()
    time.sleep(2)
    splash.close()

    widget = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(widget)
    widget.show()
    start_thread()
    sys.exit(app.exec_())