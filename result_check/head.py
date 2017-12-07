# -*- coding: cp936 -*-
__author__ = 'zzf'

import re
import datetime

hyphens_regex = re.compile(r'-{2,}')
space_regex = re.compile(r'\s{2,}')

#根据规定的头尾字符串从字符串中返回子串，包括换行符
def getText(head,tail,str):
	regex=head+r'[\s\S]+?'+tail
	result=re.search(regex,str,re.M|re.I)
	if result:
		return result.group()
	else:
		return 'No result'

#用于从字符串str中找出形如‘indexID’(如是index ID形式则要加个空格）格式的序列，返回ID的数字序列
def getIDs(index,str):
	regex=index+r'[0-9]+'
	regex_num=re.compile(r'[0-9]+$',re.M|re.I)
	p=re.compile(regex)
	array=p.findall(str)
	num_arr=[]
	for i in range(0,len(array)):
		num_arr.append(regex_num.search(array[i]).group())
	return num_arr

#从字符串str中返回keySeparatorValue\s中对应的Value字符串，无需理会空格
def getValue(key,separator,str):
	mykey=key.replace('(','').replace(')','')
	mystr=str.replace('\t','').replace('(','').replace(')','')
	regex=mykey+r'\s*'+separator+r'.+$'
	result=re.search(regex,mystr,re.M|re.I)
	if result:
		return result.group().split(separator)[1].strip()
	else:
		return 'No result'

#打印字符串列表列表
def printList(list):
	for element in list:
		print element

#用于比较 字段名 值 平均值 最大值 形式的数据，可以是不同单位
def compare(table_line ,result, head):
	value_list = space_regex.split(table_line)
	#print value_list
	current_value = convert_unit(value_list[1])
	average_value = convert_unit(value_list[2])
	max_value = convert_unit(value_list[3])
	#print str(current_value)+' '+str(average_value)+' '+str(max_value)
	if (current_value > max_value):
		result.append('!!!' + head + value_list[0] + u'is higher than  maximun average value')

#用于将value统一换算成k单位，暂时支持K、M、G,默认格式为1k，两边中间无空格
def convert_unit(value):
	num = re.search(r'(\d|\.)+', value, re.I).group()
	if value.endswith('K') or value.endswith('k'):
		result = float(num)*1000
	elif value.endswith('M') or value.endswith('m'):
		result = float(num)*1000000
	elif value.endswith('G') or value.endswith('g'):
		result = float(num)*1000000000
	else:
		result = float(num)
	return result