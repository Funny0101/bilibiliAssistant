# BiliBili Video Playback Assistant

- 2152598 郑皓予

- 2151136 朱开来

- 2153174 陈华机

****

### Content

[TOC]

****

### Brief Introduction

Our BiliBili Video Playback Assistant is an innovative video playback assistive system that combines speech recognition and gesture recognition technologies. 

It aims to provide a seamless and convenient experience for users to interact with Bilibili videos without the need for traditional mouse and keyboard inputs.

****

### File Architecture

```
└─Video Assistant
    │  pre_final.pptx
    │  README.md
    │  Report.pdf
    │  
    ├─Bilibili Video Playback Assistant
    │  │  HandTrackingMain.py
    │  │  HandTrackingMoudle.py
    │  │  main.py
    │  │  recording.wav
    │  │  
    │  ├─image
    │  │          
    │  └─sound
    │          
    └─ExecutableFile
        │  recording.wav
        │  VideoAssistant.exe
        │  
        ├─image
        │      
        └─sound
```

****

### Development Environment

**Operating System**: windows

**Programming Language**: Python3.8(In fact, this project is compatible with Python versions 3.6, 3.7, and 3.8. However, please make sure not to exceed version 3.8 to ensure the proper functioning of autopy.)

****

### Dependencies Install

```python
pip install PyQt5
pip install opencv-python
pip install mediapipe
pip install pycaw
pip install SpeechRecognition
pip install baidu-aip
pip install chardet
pip install pygame
pip install PyAutoGui
pip install autopy
pip install comtypes
```

****

### Run

1. Set up the environment for the project and install the required libraries using the method described in[Dependencies Install](#Dependencies Install).
2. Place all the files from the Bilibili Video Playback Assistant folder into the project folder.
3. Run main.py to launch the UI interface and experience the application.
4. Alternatively, you can simply run ExecutableFile/VideoAssistant.exe for an easier method.

****

### GUI and Operation Instructions

In the configured environment, and then you will see the home page after displaying the welcome page

![1](D:\Documents\大二下\用户交互技术\作业-期末\最终\Video Assistant\Bilibili Video Playback Assistant\image\截图\1.png)

- Say 'Open Bilibili' in Chinese to open www.bilibili.com 
- Say 'Help' in Chinese to open the help page

![2](D:\Documents\大二下\用户交互技术\作业-期末\最终\Video Assistant\Bilibili Video Playback Assistant\image\截图\2.png)

![3](D:\Documents\大二下\用户交互技术\作业-期末\最终\Video Assistant\Bilibili Video Playback Assistant\image\截图\3.png)

- Say "Open Bilibili" to open Bilibili web page and start Gesture recognition
- Only extend the index finger to control mouse movement
- Combining the index and middle fingers indicates clicking the left mouse button
- Open your index finger and thumb, and control the volume according to the size of the opening
- Open all fingers to take a screenshot
- Opening apart from the thumb indicates that the roller is sliding down
- Only when the thumb is open, it means the roller is sliding upwards
- Say 'Exit' at any time to exit the applicatio





