#!/usr/bin/python
# coding: utf-8
import sys
import os
import json
import socket
from datetime import datetime, date, timedelta

try:
    from urllib import request
except:
    import urllib2 as request

try:
    reload(sys)  # 解决编码问题 py3没有
    sys.setdefaultencoding('utf8')
except:
    pass

class getData():
    def __init__(self):
        self.result = {}
    # 解析文件 /proc/{cpuninfo,meminfo}
    def parse_file(self, file, name):
        with open(file) as f:
            for line in f.readlines():
                key, value = line.split(":")
                key = key.strip()
                value = value.strip()
                if key == name:
                    return value
    def hostname(self):
        hostName = socket.gethostname()
        return hostName
    def machine_type(self):
        result = os.popen("dmesg |grep -i virtual |grep -ci hardware")
        if int(result.read()) >= 1:
            type = "physical_machine" # 物理机
        else:
            result = os.popen("dmesg |grep -i virtual |grep -ci kvm")
            if int(result.read()) >= 1:
                type = "cloud_vm" # 云主机
            else:
                type = "vm" # 虚拟机
        return type
    def os_version(self):
        with open("/etc/issue") as f:
            if f.readline().strip() == "\S":
                with open("/etc/redhat-release") as f:
                    os_version = f.readline().strip()
            else:
                os_version = f.readline().strip()
        return os_version
    # 系统启动时间
    def system_up_time(self):
        with open("/proc/uptime") as f:
            s = f.read().split(".")[0] # 启动有多少秒
        up_time = datetime.now() - timedelta(seconds=float(s)) # 当前时间减去启动秒
        return date.strftime(up_time, '%Y-%m-%d')
    def public_ip(self):
        try:
            private_ip = self.private_ip()
            ip_api_url = ['http://ip.renfei.net', 'http://ifconfig.me/ip']
            ip_list = []
            try:
                req = request.Request(url=ip_api_url[0])
                res = request.urlopen(req)
                ip = json.loads(res.read().decode())['clientIP']
            except:
                req = request.Request(url=ip_api_url[1])
                res = request.urlopen(req)
                ip = res.read().decode()
            if ip in private_ip:
                ip.append(ip)
                return ip_list
            else:
                ip_list.append('%s' %ip)
                return ip_list
        except:
            return '无公网IP'
    def private_ip(self):
        nic_prefix = ['eth', 'en', 'em'] # 常见网卡名前缀
        ip_list = []
        with open("/proc/net/dev") as f:
            for s in f.readlines():
                name = s.split(':')[0].strip()
                for p in nic_prefix:
                    if name.startswith(p):
                        result = os.popen("ip addr show %s |awk -F'[ /]' '/inet /{print $6}'" %name)
                        ip_list.append(result.read().strip())
        return ip_list
    def cpu_num(self):
        cpu = self.parse_file("/proc/cpuinfo", "cpu cores")
        return "%s核" %cpu
    def cpu_model(self):
        model = self.parse_file("/proc/cpuinfo", "model name")
        return model
    def memory(self):
        total = self.parse_file("/proc/meminfo", "MemTotal")
        total = round(float(total.split()[0]) / 1024 / 1024, 1) # 转GB单位
        return "%sG" %total
    # def disk(self):
    #     disk = []
    #     result = os.popen("lsblk -d -o name,size,rota | grep -v sr0 | grep -v NAME")
    #     for d in result.read().strip().split('\n'):
    #         d = d.split()
    #         device = d[0]
    #         size = d[1]
    #         dict_type = d[2]
    #         if int(dict_type) == 0:
    #             type = 'SSD'
    #         else:
    #             type = 'HDD'
    #         disk.append(json.dumps({"device":"/dev/%s"%device,"size":size,"type":type}))
    #     return disk
    def disk(self):
        disk = []
        result = os.popen("lsblk |awk '$6~/disk/{print $1,$4,$5}'")
        for d in result.read().strip().split('\n'):
            d = d.split()
            device = d[0]
            size = d[1]
            type = "HDD" if d[2] == 0 else "SSD"
            disk.append({'device': '/dev/%s' %device, 'size': size, 'type': type})
        return disk
    def get_all(self):
        """
        这里字段必须与API对应
        """
        self.result = {
            "hostname": self.hostname(),
            "machine_type": self.machine_type(),
            "os_version": self.os_version(),
            "public_ip": self.public_ip(),
            "private_ip": self.private_ip(),
            "cpu_num": self.cpu_num(),
            "cpu_model": self.cpu_model(),
            "memory": self.memory(),
            "disk": self.disk(),
            "put_shelves_date": self.system_up_time(),  # 上架时间默认设置系统启动时间
        }
        json_data = json.dumps(self.result)
        return json_data
if __name__ == "__main__":
    data = getData().get_all()
    print(data)