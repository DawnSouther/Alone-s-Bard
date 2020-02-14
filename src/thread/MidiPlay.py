#!/usr/bin/python
# -*- coding: UTF-8 -*-

import threading
import time
import midi
from constant import PITCH_KEY_MAP, GlobalBean
import common.Util as Util

class MidiPlay(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
		self._running = True

	def stop(self):
		self._running = False;

	def run(self):
		while self._running:
			if GlobalBean.midiBySelected == None:
				print("未选中midi，无法演奏")
				break
			pattern = midi.read_midifile(GlobalBean.midiBySelected)
			seq = Util.resloveMidiEvent(pattern)
			tickPer = 1
			# 单位微秒
			for event in seq:
				if GlobalBean.midiPlayStatus == False:
					break
				if type(event) == midi.TimeSignatureEvent:
					tickPer = (1/4)/(1/event.denominator)*pattern.resolution
				elif type(event) == midi.SetTempoEvent:
					tickPer = (60000000 / int(event.bpm)) / tickPer
				elif type(event) == midi.NoteOnEvent:
					print(event)
					print(self._running)
					temp = PITCH_KEY_MAP.get(midi.NOTE_VALUE_MAP_FLAT[event.pitch], -1);
					print(midi.NOTE_VALUE_MAP_FLAT[event.pitch])
					if temp == -1:
						pass
					if type(temp) == list:
						Util.makeupKey(GlobalBean.hwnd, temp[0], temp[1])
					else:
						Util.simpleKey(GlobalBean.hwnd, temp)
					if event.tick != 0:
						print((tickPer * event.tick) / 1000000)
						# if ((tickPer * event.tick) / 10000 - 0.1) < 1:
						time.sleep((tickPer * event.tick) / 1000000 - 0.1 if (tickPer * event.tick) / 1000000 - 0.1 > 0 else 0.1)