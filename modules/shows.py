# -*- coding: utf-8 -*-


import os

#import curses

#### 转发的显示    

def showredir(device,ip,gatewayips,remotemacs,gatewaymacs,localmacs,dnsfile,ipfile,portfile):

	cmd= "reset"  
	os.system(cmd)

	print("go-betweenX 2017.5.4  sheerfish999@163.com")
	print("\n/*************************************/\n")

	print("Basic Info ")
	print("	Local Device Name: "+device)
	print("	Local IP: "+ip)
	print("	Local Mac: "+localmacs)
	print("	Gateway IP: "+gatewayips)
	print("	Gateway Mac: "+gatewaymacs)
	print("	Remote Target Mac: "+remotemacs)

	print("")

	paths=os.getcwd()   
	#### 配置文件情况

	#
	configfile=dnsfile +".temp"

	print("DNS spoof:")

	f = open(configfile, "r") 
	for line in f:
		line=line.replace("\n","")
		print("	"+line)
	f.close()  

	#
	print("IP spoof:")

	configfile=ipfile + ".temp"

	f = open(configfile, "r") 
	for line in f:
		line=line.replace("\n","")
		print("	"+line)
	f.close()  


	#
	print("Port redirect:")

	configfile=portfile + ".temp"

	f = open(configfile, "r") 
	for line in f:
		line=line.replace("\n","")
		print("	"+line)
	f.close()  

	print("\n/*************************************/\n")

	print("Use Ctrl+c to stop....")


##  原即时操作的方法  已经弃用  受限太大
def selectredir(device,ip,gatewayips,remotemacs,gatewaymacs,localmacs,stats,stdscr,dnsfile,ipfile,portfile):

	stdscr.clear()

	stdscr.addstr(0, 0, "Basic Info ", COLORS1)
	stdscr.addstr(1, 2, "Local Device Name: "+device, COLORS1)
	stdscr.addstr(2, 2, "Local IP: "+ip, COLORS1)
	stdscr.addstr(3, 2, "Local Mac: "+localmacs, COLORS1)
	stdscr.addstr(4, 2, "Gateway IP: "+gatewayips, COLORS1)
	stdscr.addstr(5, 2, "Gateway Mac: "+gatewaymacs, COLORS1)
	stdscr.addstr(6, 2, "Remote Target Mac: "+remotemacs, COLORS1)

	stdscr.addstr(8, 0, "Please select: ", COLORS1)
	stdscr.addstr(9, 2, "1. Spoof Start.", COLORS2)
	stdscr.addstr(10, 2, "2. Spoof Nothing.", COLORS3)
	stdscr.addstr(11, 2, "9. Exit.", COLORS1)

	stdscr.addstr(13, 0, "Status:", COLORS1)
	if stats=="stop":
		stdscr.addstr(14, 2, "Spoof Nothing.", COLORS3)
	else:
		paths=os.getcwd()   
		#### 配置文件情况
	
		#
		configfile=dnsfile +".temp"

		lines=14
		stdscr.addstr(lines, 2, "DNS spoof:", COLORS2)

		f = open(configfile, "r") 
		for line in f:  
			lines=lines+1
			stdscr.addstr(lines, 4, line, COLORS2)    
		f.close()  

		#
		lines=lines+1
		stdscr.addstr(lines, 2, "IP spoof:", COLORS2)

		configfile=ipfile + ".temp"

		f = open(configfile, "r") 
		for line in f:  
			lines=lines+1
			stdscr.addstr(lines, 4, line, COLORS2)    
		f.close()  


		#
		lines=lines+1
		stdscr.addstr(lines, 2, "Port redirect:", COLORS2)

		configfile=portfile + ".temp"

		f = open(configfile, "r") 
		for line in f:  
			lines=lines+1
			stdscr.addstr(lines, 4, line, COLORS2)    
		f.close()  



	stdscr.refresh()	
	#curses.noecho()



