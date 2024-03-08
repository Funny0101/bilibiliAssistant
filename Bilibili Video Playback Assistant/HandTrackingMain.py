import cv2
import numpy as np
import HandTrackingMoudle as htm
import time
import autopy
import pyautogui
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

#################################################
widthOfCamera, heightOfCamera = (640, 480) # 设置显示框大小
frameReduction = 100 # 避免到达边界时无法识别到手
frameReduction_bottom = 150
smoothening = 5 # 让鼠标的移动更为顺滑
widthOfScreen, heightOfScreen = autopy.screen.size() # 获取电脑屏幕大小
#################################################

# 屏幕相关，设置大小
cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)
cap.set(3, widthOfCamera)
cap.set(4, heightOfCamera)

# 参数设置
red = (255, 0, 255)
green = (0, 255, 0)
lengthLimit = 30 # 小于这个值被判定为点击事件

# detector
detector = htm.handDetector(maxHands=1, detectionConfidence=0.7)

# 音量相关
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
volRange = volume.GetVolumeRange()
minVol = volRange[0]  # 最小音量
maxVol = volRange[1]
maxHandLength = 250  # 自定义手能张开的最大长度
minHandLength = 50
topBar = 150  # 音量框的默认属性
bottomBar = 400
leftBar = 50
rightBar = 85
volBar = 400  # 防止报错
volPercentage = 0


class Operation:
    def __init__(self):
        self.mouseMove = False # 鼠标移动
        self.mouseLeftClick = False # 鼠标左键单击
        self.screenShot = False # 截图
        self.scrollUp = False # 鼠标滚轮上滑
        self.scrollDown = False # 鼠标滚轮下滑
        self.volumeControl = False # 音量控制

    # 重置所有属性，避免造成干扰
    def reset(self):
        self.__init__()

    # 判断当前期待执行指令
    def operationSelect(self, fingersUp):
        # 所有手指张开——截图
        # 食指张开——鼠标移动
        # 食指和大拇指张开——音量控制
        # 食指和中指并拢——鼠标左键
        # 除大拇指以外张开——滚轮下滑
        # 只有大拇指张开——滚轮上滑
        if all(x > 0 for x in fingersUp):
            self.screenShot = True
        elif not fingersUp[0] and fingersUp[1] and not fingersUp[2] and not fingersUp[3] and not fingersUp[4]:
            self.mouseMove = True
        elif fingersUp[0] and fingersUp[1] and not fingersUp[2] and not fingersUp[3] and not fingersUp[4]:
            self.volumeControl = True
        elif not fingersUp[0] and fingersUp[1] and fingersUp[2] and not fingersUp[3] and not fingersUp[4]:
            self.mouseLeftClick = True
        elif not fingersUp[0] and fingersUp[1] and fingersUp[2] and fingersUp[3] and fingersUp[4]:
            self.scrollDown = True
        elif fingersUp[0] and not fingersUp[1] and not fingersUp[2] and not fingersUp[3] and not fingersUp[4]:
            self.scrollUp = True

def handTrack(stop_event):
    # 获取上一步鼠标位置以及当前鼠标位置
    # 使操作顺滑
    preLocX, preLocY = 0, 0
    currentLocX, currentLocY = 0, 0

    while not stop_event.is_set():
        # 从屏幕流中截取有效信息
        ret, img = cap.read()
        # 找到手部信息
        img = detector.findHands(img)
        # 找到手部坐标
        handLMList = detector.findPosition(img)
        # 在屏幕中央画一个矩形框，表示手指移动的实际有效范围
        cv2.rectangle(img, (frameReduction, frameReduction),
                      (widthOfCamera - frameReduction, heightOfCamera - frameReduction), red, 2)

        # 操作对象实例
        operation = Operation()


        # 是否检测到手指
        if handLMList:
            # 哪些手指是张开的
            fingersUp = detector.fingersUp()

            # 食指和中指坐标
            indexFinger = handLMList[8][1:]
            middleFinger = handLMList[12][1:]

            # 根据手势判断应进行何种操作
            operation.operationSelect(fingersUp)

            # 食指尖和大拇指尖
            x1, y1 = handLMList[4][1], handLMList[4][2]
            x2, y2 = handLMList[8][1], handLMList[8][2]

            # 二者之间画圆的坐标,距离
            cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
            length = math.hypot(x2 - x1, y2 - y1)

            # 截屏
            if operation.screenShot:
                screenshot = pyautogui.screenshot()
                screenshot.save('screenshot.png')
                time.sleep(0.3)  # 为了防止一下子触发太多次截图操作
                print("截屏成功！")


            # 滚轮操作
            if operation.scrollDown:
                pyautogui.scroll(-20)  # 向下滚动20个单位；

            if operation.scrollUp:
                pyautogui.scroll(20)  # 向上滚动20个单位；


            # 鼠标移动
            if operation.mouseMove:
                # 计算出鼠标应该移动到的位置
                x = np.interp(indexFinger[0], (frameReduction, widthOfCamera - frameReduction), (0, widthOfScreen))
                y = np.interp(indexFinger[1], (frameReduction, heightOfCamera - frameReduction_bottom), (0, heightOfScreen))
                currentLocX = preLocX + (x - preLocX) / smoothening
                currentLocY = preLocY + (y - preLocY) / smoothening

                # 将鼠标移动到对应位置
                autopy.mouse.move(widthOfScreen - currentLocX, currentLocY)
                cv2.circle(img, (indexFinger[0], indexFinger[1]), 10, red, cv2.FILLED)
                preLocX, preLocY = currentLocX, currentLocY


            # 等待左键单击
            if operation.mouseLeftClick:
                length, img, lineInf0 = detector.findDistance(img, 8, 12)

                # 如果大拇指和食指之间的距离低于阈值，则单击鼠标左键
                if length < lengthLimit:
                    cv2.circle(img, (lineInf0[0], lineInf0[1]), 15, green, cv2.FILLED)
                    autopy.mouse.click()
                    time.sleep(0.4) # 为了防止一下子触发太多次单击左键操作


            if operation.volumeControl:
                # 画圆，连线
                cv2.circle(img, (x1, y1), 10, green, cv2.FILLED)
                cv2.circle(img, (x2, y2), 10, green, cv2.FILLED)
                cv2.line(img, (x1, y1), (x2, y2), green, 3)
                cv2.circle(img, (cx, cy), 10, green, cv2.FILLED)

                # 根据食指和拇指之间的距离控制音量
                vol = np.interp(length, [minHandLength, maxHandLength], [minVol, maxVol])
                volBar = np.interp(length, [minHandLength, maxHandLength], [bottomBar, topBar])
                volPercentage = np.interp(length, [minHandLength, maxHandLength], [0, 100])
                volume.SetMasterVolumeLevel(vol, None)

                # 在图片上一个条形框和音量百分比
                cv2.rectangle(img, (leftBar, topBar), (rightBar, bottomBar), red, 2)
                cv2.rectangle(img, (leftBar, int(volBar)), (rightBar, bottomBar), red, cv2.FILLED)
                cv2.putText(img, f'{int(volPercentage)}%', (leftBar - 10, bottomBar + 50),
                            cv2.FONT_HERSHEY_COMPLEX, 1,(255, 0, 0),3)


        # 重置操作
        operation.reset()

        # 将图片在屏幕上显示
        #cv2.imshow("Img", img)

    # 释放摄像头，销毁窗口
    cap.release()
    cv2.destroyAllWindows()

# if __name__ == '__main__':
#     handTrack()