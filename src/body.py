#!/usr/bin/python
# -*- coding: UTF-8 -*-

from PyQt5.QtWidgets import *
from PyQt5 import QtCore
from PyQt5.QtCore import QStringListModel
import win32api,win32gui,win32con,time
import midi
import glob

class Body(QWidget):
    pid = 0
    def __init__(self, hwnd):
        super().__init__()
        self.pid = hwnd
        self.topFlag = True
        self.init()

    def init(self):
        self.grid = QGridLayout()
        self.grid.setSpacing(3)
        # 标题
        self.title = self.generateTitle()
        # midi列表
        self.midiList = self.generateMidiList()
        self.flushMidiLIst()
        # 控制器按钮
        self.control = self.generateControl();

        self.grid.addLayout(self.title,0,1)
        self.grid.addWidget(self.midiList,1,1)
        self.grid.addLayout(self.control,2,1)

        self.setLayout(self.grid)
        self.resize(600, 300)
        self.move(0, 0)
        self.setWindowTitle('MIDI自动演奏工具')
        # self.setWindowFlags(QtCore.Qt.Widget) #取消置顶
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint) #置顶
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
        flush.clicked.connect(lambda : self.flushMidiLIst())
        titleBox.addWidget(flush)
        titleBox.addWidget(QPushButton('最小化'))
        titleBox.addWidget(QPushButton('关闭'))
        return titleBox

    # 生成midi列表
    def generateMidiList(self):
        midiList = QListView()
        return midiList
    
    # 生成控制器按钮
    def generateControl(self):
        controlBox = QHBoxLayout()
        player = QPushButton('演奏')
        player.clicked.connect(lambda self: self.clickKey(self.pid, 81))
        controlBox.addWidget(player)
        controlBox.addWidget(QPushButton('停止'))
        controlBox.addStretch(1)
        return controlBox

    # 生成进度条
    def generateProcessBar(self):
        self.processsBar = QProgressBar(self)

    def flushMidiLIst(self):
        # TODO 换用treeview
        midiFileList = glob.glob('./midi/*.mid')
        midiFileList = midiFileList + glob.glob('./midi/*.midi')
        self.midiList.clearFocus()
        slm = QStringListModel()
        slm.setStringList(midiFileList)
        self.midiList.setModel(slm)

    #  向窗口发送按键
    def clickKey(self, hwnd, key):
        print(hwnd)
        print(key)
        # 只需要获取一次窗口，防止抖动
        win32gui.ShowWindow(hwnd,1) 
        win32gui.SetForegroundWindow (hwnd)
        time.sleep(0.3)
        play(hwnd)
    
    def changeTop(self, top):
        if top.isChecked():
            # 置顶
            self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint) 
        else:
            # 取消置顶
            self.setWindowFlags(QtCore.Qt.Widget) 
        self.show()
            
    # 发送单一按键
    def simpleKey(self, hwnd, key):
        win32gui.PostMessage(hwnd,win32con.WM_KEYDOWN,key,0)
        win32gui.PostMessage(hwnd,win32con.WM_KEYUP,key,0)
        time.sleep(0.1)
        
    # 发送组合键
    def makeupKey(self, hwnd, oneKey, twoKey):
        win32gui.PostMessage(hwnd,win32con.WM_KEYDOWN,oneKey,0)
        win32gui.PostMessage(hwnd,win32con.WM_KEYDOWN,twoKey,0)
        time.sleep(0.1)
        win32gui.PostMessage(hwnd,win32con.WM_KEYUP,twoKey,0)
        win32gui.PostMessage(hwnd,win32con.WM_KEYUP,oneKey,0)

    def play(self, hwnd):
        pattern = midi.read_midifile('midi/lemon.mid')
        tickPer = 1
        # 单位微秒
        for trace in pattern:
            for event in trace:
                if type(event) == midi.TimeSignatureEvent:
                    tickPer = (1/4)/(1/event.denominator)*pattern.resolution
                if type(event) == midi.SetTempoEvent:
                    tickPer = (60000000 / int(event.bpm)) / tickPer
                if type(event) == midi.NoteOnEvent:
                    print(event)
                    temp = PITCH_KEY_MAP.get(midi.NOTE_VALUE_MAP_FLAT[event.pitch], -1);
                    if event.velocity == 0:
                        print(midi.NOTE_VALUE_MAP_FLAT[event.pitch])
                        if temp == -1:
                            pass
                        if type(temp) == list:
                            self.makeupKey(hwnd, temp[0], temp[1])
                        else:
                            self.simpleKey(hwnd, temp)
                        if event.tick != 0:
                            print((tickPer * event.tick) / 1000000)
                            # if ((tickPer * event.tick) / 10000 - 0.1) < 1:
                            time.sleep((tickPer * event.tick) / 1000000 - 0.1)