#!/usr/bin/python
# -*- coding: UTF-8 -*-

PITCH_KEY_MAP = {}
PITCH_KEY_MAP['C_3'] = [17, 81]
PITCH_KEY_MAP['Db_3'] = [17, 50]
PITCH_KEY_MAP['D_3'] = [17, 87]
PITCH_KEY_MAP['Eb_3'] = [17, 51]
PITCH_KEY_MAP['E_3'] = [17, 69]
PITCH_KEY_MAP['F_3'] = [17, 82]
PITCH_KEY_MAP['Gb_3'] = [17, 53]
PITCH_KEY_MAP['G_3'] = [17, 84]
PITCH_KEY_MAP['Ab_3'] = [17, 54]
PITCH_KEY_MAP['A_3'] = [17, 89]
PITCH_KEY_MAP['Bb_3'] = [17, 55]
PITCH_KEY_MAP['B_3'] = [17, 85]

PITCH_KEY_MAP['C_4'] = 81
PITCH_KEY_MAP['Db_4'] = 50
PITCH_KEY_MAP['D_4'] = 87
PITCH_KEY_MAP['Eb_4'] = 51
PITCH_KEY_MAP['E_4'] = 69
PITCH_KEY_MAP['F_4'] = 82
PITCH_KEY_MAP['Gb_4'] = 53
PITCH_KEY_MAP['G_4'] = 84
PITCH_KEY_MAP['Ab_4'] = 54
PITCH_KEY_MAP['A_4'] =89
PITCH_KEY_MAP['Bb_4'] = 55
PITCH_KEY_MAP['B_4'] = 85

PITCH_KEY_MAP['C_5'] = [16, 81]
PITCH_KEY_MAP['Db_5'] = [16, 50]
PITCH_KEY_MAP['D_5'] = [16, 87]
PITCH_KEY_MAP['Eb_5'] = [16, 51]
PITCH_KEY_MAP['E_5'] = [16, 69]
PITCH_KEY_MAP['F_5'] = [16, 82]
PITCH_KEY_MAP['Gb_5'] = [16, 53]
PITCH_KEY_MAP['G_5'] = [16, 84]
PITCH_KEY_MAP['Ab_5'] = [16, 54]
PITCH_KEY_MAP['A_5'] = [16, 89]
PITCH_KEY_MAP['Bb_5'] = [16, 55]
PITCH_KEY_MAP['B_5'] = [16, 85]

class GlobalBean:
	hwnd = -1
	midiBySelected = None
	midiPlayStatus = False
	currentThread = None