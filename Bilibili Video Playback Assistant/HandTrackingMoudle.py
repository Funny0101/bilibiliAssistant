import cv2
import mediapipe as mp
import math
import time

# 参数设置
fpsColor = (100, 100, 100)
fpsPosition = (0, 0)
connectionColor = (255, 0, 0)
handLMColor = (0, 0, 255)

# 颜色相关
circleColor = (255, 0, 255)
rectangleColor = (255, 0, 0)


class handDetector:
    def __init__(self, mode=False, maxHands=2, modComplexity=1, detectionConfidence=0.5, trackConfidence=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.modComplexity = modComplexity
        self.detectionConfidece = detectionConfidence
        self.trackConfidence = trackConfidence

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, self.modComplexity,
                                        self.detectionConfidece, self.trackConfidence)
        self.mpDraw = mp.solutions.drawing_utils
        self.tipIds = [4, 8, 12, 16, 20]

    def findHands(self, img, draw=True):
        # 将bgr转换为rgb
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        # 处理图片，提取信息
        self.results = self.hands.process(imgRGB)
        # 找到手部坐标
        multiHandLMs = self.results.multi_hand_landmarks
        # 如果找到手
        if multiHandLMs:
            for handLMs in multiHandLMs:
                if draw:
                    # 是否需要在屏幕上画图
                    handConStyle = self.mpDraw.DrawingSpec(color=connectionColor, thickness=3)  # 点与点之间的连接
                    handLMStyle = self.mpDraw.DrawingSpec(color=handLMColor, thickness=4)  # 点的颜色和大小
                    self.mpDraw.draw_landmarks(img, handLMs, self.mpHands.HAND_CONNECTIONS, handConStyle, handLMStyle)
        return img

    def findPosition(self, img, handNumber=0, draw=True):
        self.multiHandLMList = []
        xList = []
        yList = []
        box = []

        # 如果屏幕中存在手
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNumber]
            height, width = img.shape[:2]

            # 将手部信息放进列表中
            for id, lm in enumerate(myHand.landmark):
                xList.append(int(width * lm.x))
                yList.append(int(height * lm.y))
                self.multiHandLMList.append([id, xList[id], yList[id]])

            # 矩形框坐标
            xMin, xMax = min(xList), max(xList)
            yMin, yMax = min(yList), max(yList)
            box += list((xMin, yMin, xMax, yMax))
            if draw:
                # 是否将手用矩形框圈出来
                cv2.rectangle(img, (xMin - 20, yMin - 20), (xMax + 20, yMax + 20), rectangleColor, 2)
        return self.multiHandLMList+box

    def findDistance(self, img, point1, point2, draw=True, r=10, thickness=3):
        x1, y1 = self.multiHandLMList[point1][1:]
        x2, y2 = self.multiHandLMList[point2][1:]
        # 取两个点的中点
        circlePosition = ((x1 + x2) // 2, (y1 + y2) // 2)
        if draw:
            # 画圆，连线
            cv2.circle(img, (x1, y1), r, circleColor, cv2.FILLED)
            cv2.circle(img, (x2, y2), r, circleColor, cv2.FILLED)
            cv2.line(img, (x1, y1), (x2, y2), circleColor, thickness)
            cv2.circle(img, circlePosition, r, circleColor, cv2.FILLED)
        # 计算距离
        length = math.hypot(x2 - x1, y2 - y1)
        return length, img, [x1, y1, x2, y2, circlePosition]

    def fingersUp(self):
        fingers = []
        # 大拇指的检测单独判断
        # 大拇指的活动更倾向于用横向坐标x表示
        if self.multiHandLMList[self.tipIds[0]][1] > self.multiHandLMList[self.tipIds[0] - 1][1] + 10:
            fingers.append(1)
        else:
            fingers.append(0)
        # 其余四个数值，用y判断
        for id in range(1, 5):
            if self.multiHandLMList[self.tipIds[id]][2] < self.multiHandLMList[self.tipIds[id] - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)
        return fingers