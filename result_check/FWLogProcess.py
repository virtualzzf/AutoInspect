# -*- coding: cp936 -*-

__author__ = 'zzf'

from head import *

import re
import datetime

def checkFWLog(str_content):
	#读取配置文件
	profile_file=open('E:/AutoInspect/result_check/profile.txt')
	profile_content=profile_file.read()
	SRX_cpu_idle_threshold=int(getValue('SRX_cpu_idle_threshold','=',profile_content))
	SRX_cpu_utilization_threshold=int(getValue('SRX_cpu_utilization_threshold','=',profile_content))
	SRX_memory_utilization_threshold=int(getValue('SRX_memory_utilization_threshold','=',profile_content))
	SRX_session_ratio_threshold=int(getValue('SRX_session_ratio_threshold','=',profile_content))
	profile_file.close()

	#机箱告警部分
	chassis_alarms_result=[]
	#print u"------机箱告警情况------"
	chassis_alarms_info=getText('show chassis alarms \| no-more $',r'({.+:nod|.+@.+>)',str_content)
	for i in getIDs('node',chassis_alarms_info):
		node_info= getText('node'+i,r'^\n',chassis_alarms_info)
		status_info=hyphens_regex.split(node_info.replace('\n','').replace(':',''))
		node_status={status_info[0]:status_info[1]}
		if cmp(node_status[status_info[0]], 'No alarms currently active') != 0:
			chassis_alarms_result.append('!!!node' + i + ':'+status_info[1])
	#if len(chassis_alarms_result) == 0:
		#chassis_alarms_result.append(u'机箱无告警')
	printList(chassis_alarms_result)
	#print node_status

	#软件告警部分
	system_alarms_result=[]
	#print u"------软件告警情况------"
	system_alarms_info= getText('show system alarms \| no-more $',r'({.+:nod|.+@.+>)',str_content)
	for i in getIDs('node',system_alarms_info):
		node_info= getText('node'+i,'^\n',system_alarms_info)
		status_info=hyphens_regex.split(node_info.replace('\n','').replace(':',''))
		node_status={status_info[0]:status_info[1]}
		if cmp(status_info[1], 'No alarms currently active') != 0:
			system_alarms_result.append('!!!node' + i + ':'+status_info[1])
	#if len(system_alarms_result) == 0:
		#system_alarms_result.append(u'软件无告警')
	printList(system_alarms_result)
	#	print node_status

	#系统时间
	time_result=[]
	#print u"------系统时间情况------"
	system_uptime_info = getText('show system uptime \| no-more $',r'({.+:nod|.+@.+>)',str_content)
	for i in getIDs('node',system_uptime_info):
		node_info=getText('node'+i,r'^\n',system_uptime_info)
		time_current_str=getValue('Current time',': ',node_info)
		time_booted_str=getValue('System booted',': ',node_info)
		time_current=datetime.datetime.strptime(time_current_str.split(' ')[0]+' '+time_current_str.split(' ')[1], '%Y-%m-%d %H:%M:%S')
		time_booted=datetime.datetime.strptime(time_booted_str.split(' ')[0]+' '+time_booted_str.split(' ')[1], '%Y-%m-%d %H:%M:%S')
		time_run=int((time_current-time_booted).days)
		if time_run < 7:
			time_result.append('!!!node'+i+u'restarted in 1 week')
	#if len(time_result) == 0:
		#time_result.append(u'系统一周内没有重启过')
	printList(time_result)

	#路由引擎
	routing_engine_result=[]
	#print u"------路由引擎情况------"
	routing_engine_info= getText('show chassis routing-engine \| no-more $',r'({.+:nod|.+@.+>)',str_content)
	for i in getIDs('node',routing_engine_info):
		node_info=getText('node'+i,r'^\n',routing_engine_info)
		#这里没有使用getValue因为分隔符不是固定的符号，而是无规律格式的空格
		memory_utilization=re.search(r'Memory utilization.*',node_info,re.M|re.I).group()
		cpu_idle=re.search(r'Idle.*',node_info,re.M|re.I).group()
		dic_routing_engine={space_regex.split(memory_utilization)[0]:space_regex.split(memory_utilization)[1], space_regex.split(cpu_idle)[0]:space_regex.split(cpu_idle)[1]}
		if int(dic_routing_engine['Idle'].replace(' percent','')) < SRX_cpu_idle_threshold:
			routing_engine_result.append('!!!node'+i+u' CPU idle is too low '+dic_routing_engine['Idle'])
		if int(dic_routing_engine['Memory utilization'].replace(' percent', '')) > SRX_memory_utilization_threshold:
			routing_engine_result.append('!!!node' + i + u' memory utilization is too high: '+dic_routing_engine['Memory utilization'])
	#if len(routing_engine_result) == 0:
		#routing_engine_result.append(u'路由引擎正常')
	printList(routing_engine_result)
	#	print dic_routing_engine

	#集群状态
	cluster_status_result=[]
	#print u"------集群状态------"
	cluster_status_info= getText('show chassis cluster status \| no-more $',r'({.+:nod|.+@.+>)',str_content)
	#group_num=cluster_status_info.count('Redundancy group:')
	index=[]
	for i in getIDs('Redundancy group: ',cluster_status_info):
		Redundancy_info=getText('Redundancy group: '+i,r'^\n',cluster_status_info)
		for j in getIDs('node',Redundancy_info):
			node_info=space_regex.split(getText('node'+j,r'\n',Redundancy_info))
			if len(node_info) == 7:
			 	key=node_info[0]
				value=node_info[5]
				dic_node_status={key:value}
				if cmp(dic_node_status[key], 'None') != 0:
					cluster_status_result.append('!!!group' + i + ' node' + j + u' state is abnormal:'+value)
	#if len(cluster_status_result) == 0:
		#cluster_status_result.append(u'集群状态正常')
	printList(cluster_status_result)
	#	   print dic_node_status

	#板卡运行状态
	pic_status_result=[]
	#print u"------板卡运行状态------"
	pic_status = getText('show chassis fpc pic-status \| no-more $',r'({.+:nod|.+@.+>)',str_content)
	for i in getIDs('node',pic_status):
		node_info_regex=r'node'+i+r'[\s\S]*?^\n'
		node_info= re.search(node_info_regex,pic_status,re.M|re.I).group()
		for j in getIDs('Slot ',node_info):
			slot_info_regex=r'Slot '+j+r'[\s\S]+?(Slot|^\n)'
			slot_info=re.search(slot_info_regex,node_info,re.M|re.I).group()
			slot_info_list=slot_info.split('\n')
			pic_num=slot_info.count('PIC ')
			#slot信息和pic信息
			dic_slot=[]
			for k in range(0,pic_num+1):
				pic_temp=space_regex.split(slot_info_list[k].strip())
				dic_slot.append({'name':pic_temp[0], 'status':pic_temp[1]})
			if (cmp(dic_slot[0]['status'], 'Online') != 0) or (cmp(dic_slot[1]['status'], 'Online') != 0):
				print dic_slot[0]['status'] + dic_slot[1]['status']
				pic_status_result.append('!!!node' + i +' '+ dic_slot[0]['name'] + u'state is abnormal')
	#if len(pic_status_result) == 0:
		#pic_status_result.append(u'板卡运行状态正常')
	printList(pic_status_result)

	#电源模块
	env_pem_result=[]
	#print u"------电源模块------"
	env_pem = getText('show chassis environment pem \| no-more $',r'({.+:nod|.+@.+>)',str_content)
	for i in getIDs('node',env_pem):
	#	print 'node'+i+':'
		node_info=getText('node'+i+':',r'^\n',env_pem)
		for j in getIDs('PEM ',node_info):
			pem_info=getText('PEM '+j+' status:',r'(PEM |^\n)',node_info).replace(':','')
			pem_info_list=re.split('\n|\s{2,}',pem_info)
			dic_pem={pem_info_list[0]:pem_info_list[3]}
	#		print dic_pem
			if (cmp(dic_pem[pem_info_list[0]], 'Online') != 0):
				env_pem_result.append('!!!node' + i + ' ' + pem_info_list[0] + u'state is abnormal')
	#if len(env_pem_result) == 0:
		#env_pem_result.append(u'电源模块正常')
	printList(env_pem_result)

	#60s CPU 利用率
	#print u'------60秒CPU利用率------'
	spu_60s_result=[]
	spu_info = getText('show security monitoring performance spu \| no-more $',r'({.+:nod|.+@.+>)',str_content)
	for i in getIDs('node',spu_info):
		node_info=getText('node'+i,r'^\n',spu_info)
		for j in getIDs('fpc  ',node_info):
			fpc_info=getText('fpc  '+j,r'(fpc  |^\n)',node_info)
			array=[]
			sum_value=0
			average_value=0
			for k in range(0,60):
				#此处的正则表达式比较特别，不好直接用现成方法
				regex_second=r'\D'+str(k)+':'+r'\s{2,}\d+'
				p=re.compile(regex_second)
				time_info=p.search(fpc_info).group().replace('\n','').replace(' ','')
				key=time_info.split(':')[0]
				value=time_info.split(':')[1]
				array.append({key:value})
				sum_value += int(value)
			average_value=sum_value/60
			if average_value > SRX_cpu_utilization_threshold:
				spu_60s_result.append('!!!node '+i+' FPC '+j+u' average CPU utilization is too high in 60s: '+ str(average_value))
	#if len(spu_60s_result) == 0:
		#spu_60s_result.append(u'60s CPU使用率正常')
	printList(spu_60s_result)

	#会话连接数
	session_result=[]
	#print u'------安全监控情况------'
	session_info = getText('show security monitoring \| no-more $',r'({.+:nod|.+@.+>)',str_content)
	for i in getIDs('node',session_info):
		node_info=getText('node'+i , r'^\n' , session_info)
		table_info=getText(r'^\s*\d+',r'^\n',node_info)
		table_list=table_info.split('\n')
		#多两个空行
		for j in range(0,len(table_list)-2):
			line=space_regex.split(re.sub(r'^\s+','',table_list[j]))
			dic_line={}
			dic_line['FPC'] = line[0]
			dic_line['PIC'] = line[1]
			dic_line['CPU'] = line[2]
			dic_line['MEM'] = line[3]
			dic_line['flow session current'] = line[4]
			dic_line['flow session maximun'] = line[5]
			dic_line['cp session current'] = line[6]
			dic_line['cp session maximun'] = line[7]
			if int(dic_line['flow session current']) == 0 and int(dic_line['flow session maximun']) == 0:
				dic_line['flow session ratio'] = 0
			else:
				dic_line['flow session ratio'] = int(dic_line['flow session current'])/int(dic_line['flow session maximun'])*100
			if int(dic_line['cp session current']) == 0 and int(dic_line['cp session maximun']) == 0:
				dic_line['cp session ratio'] = 0
			else:
				dic_line['cp session ratio'] = int(dic_line['cp session current'])/int(dic_line['cp session maximun'])*100
			if int(dic_line['CPU']) > SRX_cpu_utilization_threshold:
				session_result.append('!!!node '+i+' FPC '+dic_line['FPC']+' PIC '+dic_line['PIC']+u' CPU utilization is too high: '+dic_line['CPU'])
			if int(dic_line['MEM']) > SRX_memory_utilization_threshold:
				session_result.append('!!!node '+i+' FPC '+dic_line['FPC']+' PIC'+dic_line['PIC']+u' memory utilization is too high: '+dic_line['MEM'])
			if dic_line['flow session ratio'] > SRX_session_ratio_threshold:
				session_result.append('!!!node '+i+' FPC '+dic_line['FPC']+' PIC'+dic_line['PIC']+u' Flow session is too high: '+dic_line['flow session ratio'])
	#if len(session_result) == 0:
		#session_result.append(u'安全监控正常')
	printList(session_result)
	
	if len(chassis_alarms_result)==0 and len(system_alarms_result)==0 and len(time_result)==0 and len(routing_engine_result)==0 and len(cluster_status_result)==0 and len(pic_status_result) == 0 and len(env_pem_result) == 0 and len(spu_60s_result)==0 and len(session_result)==0:
		print "ALL IS WELL"