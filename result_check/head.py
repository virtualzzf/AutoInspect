# -*- coding: cp936 -*-
__author__ = 'zzf'

import re
import datetime

hyphens_regex = re.compile(r'-{2,}')
space_regex = re.compile(r'\s{2,}')

#���ݹ涨��ͷβ�ַ������ַ����з����Ӵ����������з�
def getText(head,tail,str):
	regex=head+r'[\s\S]+?'+tail
	result=re.search(regex,str,re.M|re.I)
	if result:
		return result.group()
	else:
		return 'No result'

#���ڴ��ַ���str���ҳ����确indexID��(����index ID��ʽ��Ҫ�Ӹ��ո񣩸�ʽ�����У�����ID����������
def getIDs(index,str):
	regex=index+r'[0-9]+'
	regex_num=re.compile(r'[0-9]+$',re.M|re.I)
	p=re.compile(regex)
	array=p.findall(str)
	num_arr=[]
	for i in range(0,len(array)):
		num_arr.append(regex_num.search(array[i]).group())
	return num_arr

#���ַ���str�з���keySeparatorValue\s�ж�Ӧ��Value�ַ������������ո�
def getValue(key,separator,str):
	mykey=key.replace('(','').replace(')','')
	mystr=str.replace('\t','').replace('(','').replace(')','')
	regex=mykey+r'\s*'+separator+r'.+$'
	result=re.search(regex,mystr,re.M|re.I)
	if result:
		return result.group().split(separator)[1].strip()
	else:
		return 'No result'

#��ӡ�ַ����б��б�
def printList(list):
	for element in list:
		print element

#���ڱȽ� �ֶ��� ֵ ƽ��ֵ ���ֵ ��ʽ�����ݣ������ǲ�ͬ��λ
def compare(table_line ,result, head):
	value_list = space_regex.split(table_line)
	#print value_list
	current_value = convert_unit(value_list[1])
	average_value = convert_unit(value_list[2])
	max_value = convert_unit(value_list[3])
	#print str(current_value)+' '+str(average_value)+' '+str(max_value)
	if (current_value > max_value):
		result.append('!!!' + head + value_list[0] + u'is higher than  maximun average value')

#���ڽ�valueͳһ�����k��λ����ʱ֧��K��M��G,Ĭ�ϸ�ʽΪ1k�������м��޿ո�
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