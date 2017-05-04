# go-betweenX
用于在不访问目标服务器的情况下,  对目标服务器对外的请求流量进行转发(同网段),   包括外部域名\本网段的某个IP , 转发到本地某个端口, 以便进行所需的动态接口打桩测试

1)  只适用于同网段 (本地对应的网卡和对应目标在同一个网段)  , 对安装360的PC(启动网络保护)和安卓机测试无效,   虚拟机似乎必须是同一个server下

2)  安装   arpoison   ,  dnsspoof    :  yum install dsniff 


参数格式:  python tocheat.py


config.py   基本配置文件 

(注意以下文件名可配)

dns 转发配置文件  (转发到本地, 支持#注释):  		dnspoof.config(dnsfile)		格式:  每行一个域名  www.abc.com			效果: 对指定域名的请求转发到本地

ip  转发配置文件 (同网段转发到本地, 支持#注释):  	ipspoof.config(ipfile)			格式:  每行一个IP 192.168.1.200				效果: 对同网段指定IP的请求转发到本地

本地端口转发配置文件 (本地两个端口之间, 支持#注释):	portredirect.config(portfile)		格式:  每行一个转发 80 48000				效果: 对到本地80地址的请求,转发到本地48000
