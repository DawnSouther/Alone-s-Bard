#!/usr/bin/python
# -*- coding: UTF-8 -*-

import win32api
import win32gui,win32con,time
import midi
from constant import GlobalBean


# 发送单一按键
def simpleKey(hwnd, key):
	win32gui.PostMessage(hwnd,win32con.WM_KEYDOWN,key,0)
	win32gui.PostMessage(hwnd,win32con.WM_KEYUP,key,0)
	time.sleep(0.1)
	
# 发送组合键
def makeupKey(hwnd, oneKey, twoKey):
	win32gui.PostMessage(hwnd,win32con.WM_KEYDOWN,oneKey,0)
	win32gui.PostMessage(hwnd,win32con.WM_KEYDOWN,twoKey,0)
	time.sleep(0.1)
	win32gui.PostMessage(hwnd,win32con.WM_KEYUP,twoKey,0)
	win32gui.PostMessage(hwnd,win32con.WM_KEYUP,oneKey,0)

# new新线程
def newMidiThread(midiplay):
	thread = midiplay
	thread.setDaemon(True)
	thread.start()
	GlobalBean.midiPlayStatus = True
	GlobalBean.currentThread = thread

# 停止线程
def stopMidiThread():
	GlobalBean.midiPlayStatus = False
	GlobalBean.currentThread.stop()
	while GlobalBean.currentThread.is_alive() != False:
		pass
	GlobalBean.currentThread == None

def resloveMidiEvent(pattern):
	list = [];
	for trace in pattern:
		for event in trace:
			if type(event) == midi.TimeSignatureEvent or type(event) == midi.SetTempoEvent:
				list.append(event)
			elif type(event) == midi.NoteOnEvent:
				if event.velocity != 0:
					list.append(event)
				else:
					list.append(midi.NoteOffEvent(tick=event.tick, velocity=event.velocity, pitch=event.pitch))
			elif type(event) == midi.NoteOffEvent:
				list.append(event)
	return list
					
def negativeFor(list, item):
	if type(list[len(list)-1]) == midi.NoteOnEvent and list[len(list)-1].pitch == item.pitch:
		return len(list)-1
	return -1