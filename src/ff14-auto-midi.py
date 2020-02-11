#!/usr/bin/python
# -*- coding: UTF-8 -*-

import sys 
import constant
from body import Body
from PyQt5.QtWidgets import QApplication
import win32gui

if __name__ != "__main__":
    exit

app = QApplication(sys.argv)
windowtitle = '最终幻想XIV'
hwnd = win32gui.FindWindow(None, windowtitle)
w = Body(hwnd)

sys.exit(app.exec_())