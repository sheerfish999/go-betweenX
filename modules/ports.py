# -*- coding: utf-8 -*-

import os



#### 本地端口转发

def portdirect(portfile,delall=0):    # delall=1 代表只是按照列表清空转发


	####  处理配置文件
	paths=os.getcwd() 
	configfile=portfile + ".temp"
	cmd="touch " + configfile
	os.system(cmd)

	f = open(paths  + "/" + portfile)            
	file_object = open(paths  + "/" + configfile, 'w')

	for line in f:  
		if line[0:1]!="#":       #非注释
			file_object.write(line)

	f.close()
	file_object.close()	


	### 逐行进行执行

	file_object = open(paths  + "/" + configfile)
	for ports in file_object:

		theport=ports.split(" ")
		port1=theport[0]
		port2=theport[1]
		
		port2=port2.replace("\n","")
		
		#先删除, 避免历史错误累积
		delportdirect(port1,port2)

		if delall==0:   ## 不是清空操作
			cmd= "iptables -t nat -A PREROUTING -p tcp --dport " + str(port1) +" -j REDIRECT --to-ports "+ str(port2)
			os.system(cmd) 

	file_object.close()	


##### 删除 iptables 映射

def delportdirect(port1,port2):

	cmd="iptables -t nat -L  PREROUTING -n | grep -n 'Chain PREROUTING'  | awk -F ':' '{print $1}'  |head -n 1"
	output =os.popen(cmd)  
	line1 = output.read()
	#print(cmd)
	#print(line1)

	cmd="iptables -t nat -L PREROUTING -n | grep -n 'tcp dpt:"+str(port1)+" redir ports "+str(port2)+"' |  awk -F ':' '{print $1}' |head -n 1"
	output =os.popen(cmd)  
	line2 = output.read() 
	#print(cmd)
	#print(line2)

	if line2!="":
		line=int(line2)-int(line1)-1
		cmd="iptables -t nat -D PREROUTING " +str(line)
		os.system(cmd) 






