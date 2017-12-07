# -*- coding: cp936 -*-

__author__ = 'zzf'

from head import *
import re
def checkSWLog(log_content):
	profile_file=open('E:/AutoInspect/result_check/profile.txt')
	profile_content=profile_file.read()
	SW_CPU_usage_threshold=int(getValue('SW_CPU_usage_threshold','=',profile_content))
	SW_memory_used_threshold=int(getValue('SW_memory_used_threshold','=',profile_content))
	profile_file.close()

	#CPU使用率
	cpu_usage_result=[]
	#print u"------CPU利用率情况------"
	cpu_info_all = getText('display cpu-usage$','<.+?>', log_content)
	cpu_info_regex = r'^Chassis.+\n.+\n.+\n.+\n'
	cpu_info_list = re.findall(cpu_info_regex, cpu_info_all, re.M|re.I)
	for cpu_info_single in cpu_info_list:
		warning_5s=''
		warning_1m=''
		warning_5m=''
		chassic_regex = r'Chassis \d+'
		slot_regex = r'Slot \d+'
		cpu_regex = r'CPU 1'
		chassic_value = re.search(chassic_regex, cpu_info_single).group()
		slot_value = re.search(slot_regex, cpu_info_single).group()
		cpu_value = re.search(cpu_regex, cpu_info_single)
		value_5s = re.search(r'\d+(?=% in last 5 seconds)',cpu_info_single,re.M|re.I).group()
		value_1m = re.search(r'\d+(?=% in last 1 minute)',cpu_info_single,re.M|re.I).group()
		value_5m = re.search(r'\d+(?=% in last 5 minutes)',cpu_info_single,re.M|re.I).group()
		if int(value_5s) > SW_CPU_usage_threshold:
			warning_5s = u' CPU utilization is too high in 5s'
		if int(value_1m) > SW_CPU_usage_threshold:
			warning_1m = u' CPU utilization is too high in 1m'
		if int(value_5m) > SW_CPU_usage_threshold:
			warning_5m = u' CPU utilization is too high in 5m'
		if (len(warning_5s)+len(warning_1m)+len(warning_5m)) != 0:
			if cpu_value:
				cpu_usage_result.append(chassic_value+' '+slot_value+' CPU1'+warning_5s+warning_1m+warning_5m)
			else:
				cpu_usage_result.append(chassic_value + ' ' + slot_value + warning_5s + warning_1m + warning_5m)
	#if len(cpu_usage_result) == 0:
		#cpu_usage_result.append(u'CPU使用率情况正常')
	printList(cpu_usage_result)

	#内存使用率
	memory_used_result=[]
	#print u"------内存使用率------"
	memory_used_info=getText(r'display memory$','<.+?>', log_content)
	memory_used_value = getValue('Used Rate',':',memory_used_info).replace('%','')
	if int(memory_used_value) > SW_memory_used_threshold:
		memory_used_result.append(u'!!!memory utilization is too high:'+ memory_used_value)
	#else:
		#print u'内存使用正常'
	printList(memory_used_result)

	#启动时间
	version_result=[]
	#print u"------启动时间情况------"
	version_info=getText(r'display version$','<.+?>', log_content)
	uptime_regex=r'^.+uptime is .+'
	uptime_list = re.findall(uptime_regex, version_info,re.M|re.I)
	week_regex = r'is \d+ weeks'
	slot_regex0 = r'^.+ uptime'
	slot_regex = r'^.+:'
	#第一条格式不同，单独拿出来
	slot0 = re.search(slot_regex0, uptime_list[0], re.M|re.I).group().replace(' uptime','')
	week_num0 = re.search(week_regex, uptime_list[0], re.M|re.I)
	if not(week_num0):
		version_result.append(slot0 + u'restarted in 1 week')
	for time in uptime_list[1:]:
		slot = re.search(slot_regex, time, re.M | re.I).group()
		search_value = re.search(week_regex, time, re.M|re.I)
		if not(search_value):
			version_result.append(slot + u'restarted in 1 week')
	#if len(version_result) == 0:
		#print u'运行时间正常'
	printList(version_result)

	#设备情况
	device_result=[]
	HA_status=[]
	#print u"------设备情况------"
	device_info=getText(r'display device$','<.+?>', log_content)
	line_regex = r'\d/\d.*'
	p=re.compile(line_regex)
	line_list=p.findall(device_info)
	for line in line_list:
		p = re.compile(r'\s+')
		state_info = p.split(line)
		slot_no = state_info[0]
		brd_Type = state_info[1]
		brd_status = state_info[2]
		#该字段暂时未用
		#soft_ver = state_info[3]
		if cmp(brd_status, 'Master') == 0:
			HA_status.append('Master: Slot '+ slot_no)
		if cmp(brd_status, 'Slave') == 0:
			HA_status.append('Slave: Slot '+ slot_no)
		if cmp('Abnormal',brd_status) == 0:
			device_result. append('!!!Slot:' + slot_no + u'state is abnormal')
	#if len(device_result) == 0:
		#device_result.append(u'设备状态正常')
	printList(HA_status)
	printList(device_result)

	#环境情况
	env_result=[]
	#print u"------环境情况------"
	env_info=getText(r'display environment$','<.+?>', log_content)
	line_regex = r'\d/\d.*'
	p=re.compile(line_regex)
	line_list=p.findall(env_info)
	for line in line_list:
		p = re.compile(r'\s+')
		temp_info = p.split(line)
		slot_id = temp_info[0]
		temp=int(temp_info[3])
		lowerLimit=int(temp_info[4])
		warningLimit = int(temp_info[5])
		alarmLimit = temp_info[6]
		if temp <= lowerLimit:
			line_result = '!!!Slot '+ slot_id + u'temperature is lower than min limit: ' + str(temp)
		elif temp >= warningLimit and temp < alarmLimit:
			line_result = '!!!Slot ' + slot_id + u'temperature is higher than warning threshold: ' + str(temp)
		elif temp >= alarmLimit:
			line_result = '!!!Slot ' + slot_id + u'temperature is higher than alarm threshold: ' + str(temp)
		elif temp > lowerLimit and temp <warningLimit:
			continue
		else:
			line_result = '!!!Slot ' + slot_id + u'data error:'+ str(temp) + " "+str(lowerLimit)+" "+str(warningLimit)+" "+alarmLimit
		env_result.append(line_result)
	#if len(env_result) == 0:
		#env_result.append(u'环境情况正常')
	printList(env_result)

	#告警
	#print u"------告警信息------"
	alarm_result =[]
	alarm_info= re.search(r'(?<=display alarm\n)[\s\S]+?(?=\n^<.+?>)', log_content, re.M | re.I).group()
	if cmp(alarm_info, " No alarm information.") != 0:
		alarm_result.append(alarm_info)
	#else:
		# print u"无告警信息"
	printList(alarm_result)

	#风扇情况
	fan_state_result=[]
	#print u"------风扇情况------"
	fan_info=getText(r'display fan$','<.+?>', log_content)
	for i in getIDs('Fan-tray state on chassis ', fan_info):
		chassis_info = getText('Fan-tray state on chassis '+i,r'^\n',fan_info)
		for j in getIDs('Fan-tray  ',chassis_info):
			fan_tray_info = getText('Fan-tray  ', r'\n', chassis_info)
			state_list = space_regex.split(fan_tray_info)
			if cmp(state_list[2].replace('\n',''), 'state: Normal') != 0:
				fan_state_result.append('!!!'+state_list[0]+' '+state_list[1]+u' state is abnormal')
	#if len(fan_state_result) == 0:
		#fan_state_result.append(u'风扇状态正常')
	printList(fan_state_result)

	#同步情况
	#print u"------同步情况------"
	ntp_result=[]
	ntp_info=getText(r'display ntp-service status$','<.+?>', log_content)
	clock_status = getValue('Clock status',':',ntp_info)
	if cmp('synchronized',clock_status) != 0:
		ntp_result.append(u'!!!Sync Service is abnormal')
	#else:
		#print u'同步服务正常'
	printList(ntp_result)

	#IRF链路情况
	#print u"------IRF链路情况------"
	irf_link_result= []
	irf_link_info=getText(r'display irf link$','<.+?>', log_content)
	for i in getIDs('Member ',irf_link_info):
		member_info= getText('Member '+i,r'(Member|<.+>)',irf_link_info)
		member_info2 = getText('IRF Port', r'(Member|<.+>)', member_info)
		for j in getIDs(r' ',member_info2):
			dic_port_num={'port':j}
			list_port_status=[]
			irf_info_regex = '^ '+j+' +'+'([\s\S]+?)(?=((^ \d)|(Member)|(<.+)))'
			irf_info = re.search(irf_info_regex, member_info2, re.M|re.I).group()

			port_info = irf_info.split('\n')
			first_line = space_regex.split(port_info[0].strip())
			list_port_status.append({'interface':first_line[1],'status':first_line[2]})

			for k in range(1,len(port_info)-1):
				other_line = space_regex.split(port_info[k].strip())
				list_port_status.append({'interface': other_line[0], 'status': other_line[1]})

			for interface_status in list_port_status:
				if cmp(interface_status['status'], 'DOWN') == 0:
					irf_link_result.append('!!!Member'+ i + ' ' + 'Port' +j + ' ' + interface_status['interface'] + u'is cloded')
	#if len(irf_link_result) == 0:
		#irf_link_result.append(u'IRF链路状态正常')
	printList(irf_link_result)
	
	if len(cpu_usage_result)==0 and len(memory_used_result)==0 and len(version_result)==0 and len(device_result)==0 and len(env_result)==0 and len(alarm_result)==0 and len(fan_state_result)==0 and len(ntp_result)==0 and len(irf_link_result)==0:
		print "ALL IS WELL"