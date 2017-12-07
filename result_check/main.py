# -*- coding: cp936 -*-

__author__ = 'zzf'

from head import *
from FWLogProcess import checkFWLog
from SWLogProcess import checkSWLog
from F5LogProcess import checkF5Log

equipment_file=open('E:/AutoInspect/equipmentInfo.txt')
equipmentInfos = equipment_file.readlines()
for equipmentInfo in equipmentInfos:
	ip, usernam, password, equipment_type = equipmentInfo.split()
	log_info = open(r'E:/AutoInspect/' + ip + r'.txt').read()
	print '\n'+ u"checking " + ip + '......'
	if cmp(equipment_type, "FW") == 0:
		checkFWLog(log_info)
	elif cmp(equipment_type, "SW") == 0:
		checkSWLog(log_info)
	elif cmp(equipment_type, "F5") == 0:
		checkF5Log(log_info)
