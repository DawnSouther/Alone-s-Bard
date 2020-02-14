#!/usr/bin/python
# -*- coding: UTF-8 -*-

from PyQt5.QtWidgets import *
from PyQt5 import QtCore
from PyQt5.QtCore import QStringListModel
import pywintypes
import win32api
import win32gui,win32con,time
import midi
from constant import PITCH_KEY_MAP, GlobalBean
from widget.MidiList import MidiList
from thread.MidiPlay import MidiPlay
import common.Util as Util

class Body(QWidget):
    pid = 0
    def __init__(self, hwnd):
        super().__init__()
        self.pid = GlobalBean.hwnd
        self.topFlag = True
        self.restorePos = None
        self.restoreSize = None
        self.startMovePos = None
        self.init()

    def init(self):
        self.grid = QGridLayout()
        self.grid.setSpacing(3)
        # midi列表
        self.midiList = MidiList()
        # 标题
        self.title = self.generateTitle()
        # 控制器按钮
        self.control = self.generateControl();

        self.grid.addLayout(self.title,0,1)
        self.grid.addWidget(self.midiList.midiList,1,1)
        self.grid.addLayout(self.control,2,1)

        self.setLayout(self.grid)
        self.resize(600, 300)
        self.setFixedSize(600, 300)
        self.move(0, 0)
        self.setWindowTitle('MIDI自动演奏工具')
        # self.setWindowFlags(QtCore.Qt.Widget) #取消置顶
        print(self.windowFlags())
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.FramelessWindowHint) #置顶
        self.show()
    
    # 生成标题控件
    def generateTitle(self):
        titleBox = QHBoxLayout()
        titleBox.addWidget(QLabel('MIDI列表'))
        titleBox.addStretch(1)
        top = QPushButton('置顶');
        top.setCheckable(True)
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        top.clicked[bool].connect(lambda : self.changeTop(top))
        titleBox.addWidget(top)
        flush = QPushButton('刷新');
        flush.clicked.connect(self.midiList.flushMidiList)
        titleBox.addWidget(flush)
        mined = QPushButton('最小化')
        mined.clicked.connect(self.ShowMininizedWindow)
        titleBox.addWidget(mined)
        closed = QPushButton('关闭')
        closed.clicked.connect(self.CloseWindow)
        titleBox.addWidget(closed)
        return titleBox
    
    #关闭窗口
    def CloseWindow(self):
        self.close()

    #最小化窗口
    def ShowMininizedWindow(self, min):
        self.showMinimized()

    # 生成控制器按钮
    def generateControl(self):
        controlBox = QHBoxLayout()
        player = QPushButton('演奏')
        player.clicked.connect(self.clickKey)
        controlBox.addWidget(player)
        stoper = QPushButton('停止')
        stoper.clicked.connect(self.stopPlay)
        controlBox.addWidget(stoper)
        controlBox.addStretch(1)
        return controlBox

    # 生成进度条
    def generateProcessBar(self):
        self.processsBar = QProgressBar(self)

    # 向窗口发送按键
    def clickKey(self):
        print(self.pid)
        # print(key)
        # 只需要获取一次窗口，防止抖动
        win32gui.SetForegroundWindow (self.pid)
        time.sleep(0.3)
        self.play(self.pid)
    
    # 停止演奏
    def stopPlay(self):
        Util.stopMidiThread()
    
    def changeTop(self, top):
        if top.isChecked():
            # 置顶
            self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.FramelessWindowHint) 
        else:
            # 取消置顶
            self.setWindowFlags(QtCore.Qt.Widget | QtCore.Qt.FramelessWindowHint) 
        self.show()

    def play(self, hwnd):
        if GlobalBean.currentThread == None:
            Util.newMidiThread(MidiPlay())
        else:
            Util.stopMidiThread()
            Util.newMidiThread(MidiPlay())

    def getRestoreInfo(self):
        return self.restorePos, self.restoreSize

    def mousePressEvent(self, QMouseEvent):
        self.isPressed = True
        self.startMovePos = QMouseEvent.globalPos()
        print(self.startMovePos)

    def mouseMoveEvent(self, QMouseEvent):
        if self.isPressed:
            movePoint = QMouseEvent.globalPos() - self.startMovePos
            widgetPos = self.pos()
            self.startMovePos = QMouseEvent.globalPos()
            self.move(widgetPos.x() + movePoint.x(), widgetPos.y() + movePoint.y())

    def mouseReleaseEvent(self, QMouseEvent):
        self.isPressed = False