#!/usr/bin/python
# -*- coding: UTF-8 -*-

from PyQt5.QtWidgets import QListWidget, QWidget
import glob
from constant import GlobalBean

class MidiList(QWidget):
	midiFile = ['./midi/*.mid', './midi/*.midi']
	def __init__(self):
		super().__init__()
		self.init()
	
	def init(self):
		self.midiList = QListWidget()
		self.midiDict = {}
		self.flushMidiList()

	def flushMidiList(self):
		midiFileList = glob.glob(MidiList.midiFile[0]) + glob.glob(MidiList.midiFile[1])
		self.midiDict.clear()
		for file in midiFileList:
			self.midiDict[file.rsplit('\\', 1)[1]] = file
		self.midiList.clear()
		self.midiList.addItems(self.midiDict.keys())
		self.midiList.itemClicked.connect(self.click)
	
	def click(self, item):
		GlobalBean.midiBySelected = self.midiDict.get(item.text(), None)
		# print(GlobalBean.midiBySelected)
