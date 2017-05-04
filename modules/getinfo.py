# -*- coding: utf-8 -*-

import os
import time

import codecs


#####################################  获得基础信息

### 文件处理, 获得配置文件信息

def openfiles(filename):

	paths=os.getcwd()    #绝对路径  , os.getcwd()  代替  sys.path[0]

	#string = codecs.open(paths + "/"+ filename,'r','utf-8').read()
	string = codecs.open(paths + "/"+ filename,'r').read()

	lines = len(open(filename,'rU').readlines())
	return(string,lines)


###  本地MAC

def localmac(device):

	### ifconfig 获得不稳定(和版本有关)

	cmd="ip addr show " + device +" | grep link/ether | awk '{print($2)}'"
	#print(cmd)
	output =os.popen(cmd)  
	res = output.read() 
	res=res.replace("\n","")

	#print("localmac: "+ res)

	return(res)

###　本地IP

def localip(device):

	cmd="ifconfig " + device  +" | grep -v inet6 | grep inet | awk '{print($2)}'"

	#print(cmd)
	output =os.popen(cmd)  
	res = output.read() 
	res=res.replace("addr:","")  # centos6.5
	res=res.replace("\n","")

	#print("localip: "+ res)

	return(res)

###  网关IP地址

def getgateway(device):

	cmd="route -n | grep UG | grep " +  device + " | awk '{print($2)}'"

	#print(cmd)
	output =os.popen(cmd)  
	res = output.read() 
	res=res.replace("\n","")

	#print("gatewayip: "+ res)	

	return(res)

#### 目标MAC地址

def getremotemac(ip):

	cmd="ping " + ip + " -c 2"
	#print(cmd)
	output =os.popen(cmd)  

	time.sleep(2)  ## 稍等
	cmd="arp -a -n | grep " + ip + "  | awk '{print($4)}'"
	#print(cmd)
	output =os.popen(cmd)  
	res = output.read() 
	res=res.replace("\n","")

	#print("remoteMAC: "+ res)

	return(res)

### 网关MAC地址

def getgatewaymac(device):

	ip=getgateway(device)

	res=getremotemac(ip)

	#print("gatewaymac: "+ res)	

	return(res)



###  获得本地激活的物理设备

def findStr(string, subStr, findCnt):  
	listStr = string.split(subStr,findCnt)  
	#print(listStr)  
	if len(listStr) <= findCnt:    #分割完后的字符串的长度（分割段）与要求出现的次数比较  
		return -1  
	return(len(string)-len(listStr[-1])-len(subStr))

def getipsub(ip):

	pos=findStr(ip, ".", 3)    ### 前三位  作为网段标记
	ipsub=ip[:pos]

	#print(ipsub)

	return(ipsub)

def localdevice(ip=""):   ###   ip参数是与目标ip在同一网段的网络设备, 不添则不判断

	thedevice=""

	cmd="ls -l /sys/class/net | grep -v virtual | grep '-' | awk '{print $9}'"     ### 1  非虚拟设备
	output =os.popen(cmd)  
	res = output.read() 

	devices=res.split("\n")
	#print(devices)

	for num in range(len(devices)):

		if devices[num]!="":

			#print(devices[num])
			cmd= "ifconfig " + devices[num] +" | grep RUNNING"    ###  2 为正在运行的设备
			output =os.popen(cmd)  
			res = output.read()
						
			if res!="":
				#print(devices[num])
				localips=localip(devices[num])
				
				if ip!="":     ### 3  只获取在同一个网段的设备名
					if  getipsub(ip)==getipsub(localips) and (localips is not None):
						thedevice=devices[num]
					else:
						devices[num]=""   ## 成员置空

			else:
				devices[num]=""   ## 成员置空


	return(thedevice)


