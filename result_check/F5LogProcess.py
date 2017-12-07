# -*- coding: cp936 -*-

__author__ = 'zzf'

from head import *

import re

def checkF5Log(log_content):
    profile_file=open('E:/AutoInspect/result_check/profile.txt')
    profile_content=profile_file.read()
    F5_CPU_usage_threshold=int(getValue('F5_CPU_usage_threshold','=',profile_content))
    F5_memory_used_threshold=int(getValue('F5_memory_used_threshold','=',profile_content))
    profile_file.close()

    #连接情况
    connection_result=[]
    #print u"------连接情况------"
    connection_info = getText('# show sys performance connection$','.+@.+(tmos)',log_content)
    connections_line = getText(r'^Connections', '\n',connection_info).replace('\n','')
    client_connections_line = getText(r'^Client Connections', '\n',connection_info).replace('\n','')
    server_Connections_line = getText(r'^Server Connections', '\n',connection_info).replace('\n','')
    compare(connections_line ,connection_result, '')
    compare(client_connections_line ,connection_result, '')
    compare(server_Connections_line ,connection_result, '')
    #if len(connection_result) == 0:
        #connection_result.append(u'连接情况正常')
    printList(connection_result)

    #系统情况
    system_result=[]
    #print u"------系统情况------"
    system_info = getText('# show sys performance system$','.+@.+(tmos)',log_content)
    utilization_line = getText(r'^Utilization', '\n',system_info).replace('\n','')
    tmm_memory_line = getText(r'^TMM Memory Used', '\n',system_info).replace('\n','')
    other_memory_line = getText(r'^Other Memory Used', '\n',system_info).replace('\n','')
    compare(utilization_line ,system_result, '')
    compare(tmm_memory_line ,system_result, '')
    compare(other_memory_line ,system_result, '')
    #if len(system_result) == 0:
        #system_result.append(u'系统情况正常')
    printList(system_result)

    #吞吐量
    throughput_bits_result=[]
    #print u"------吞吐量情况------"
    throughput_info = getText('# show sys performance throughput$','.+@.+(tmos)',log_content)
    throughput_bits_info= getText(r'^Throughput\(bits\)\(bits\/sec\)', r'^\s+',throughput_info)
    service_bits_line = getText(r'^Service', '\n',throughput_bits_info).replace('\n','')
    in_bits_line = getText(r'^In', '\n',throughput_bits_info).replace('\n','')
    out_bits_line = getText(r'^Out', '\n',throughput_bits_info).replace('\n','')
    if cmp(service_bits_line, "No result") != 0:
        compare(service_bits_line ,throughput_bits_result, 'Throughput(bits/sec) ')
    compare(in_bits_line ,throughput_bits_result, 'Throughput(bits/sec) ')
    compare(out_bits_line ,throughput_bits_result, 'Throughput(bits/sec) ')
    #if len(throughput_bits_result) == 0:
        #throughput_bits_result.append(u'吞吐量(bits/sec)情况正常')
    printList(throughput_bits_result)

    throughput_packet_result=[]
    throughput_packets_info = getText(r'^Throughput\(packets\)\(pkts\/sec\)', r'^\s+',throughput_info)
    service_packets_line = getText(r'^Service', '\n',throughput_packets_info).replace('\n','')
    in_packets_line = getText(r'^In', '\n',throughput_packets_info).replace('\n','')
    out_packets_line = getText(r'^Out', '\n',throughput_packets_info).replace('\n','')
    if cmp(service_packets_line, "No result") != 0:
        compare(service_packets_line ,throughput_packet_result, 'Throughput(pkts/sec) ')
    compare(in_packets_line ,throughput_packet_result, 'Throughput(pkts/sec) ')
    compare(out_packets_line ,throughput_packet_result, 'Throughput(pkts/sec) ')
    #if len(throughput_packet_result) == 0:
        #throughput_packet_result.append(u'吞吐量(pkts/sec)情况正常')
    printList(throughput_packet_result)

    if len(connection_result) == 0 and len(system_result)==0 and len(throughput_bits_result) == 0 and len(throughput_packet_result)==0:
        print "ALL IS WELL"