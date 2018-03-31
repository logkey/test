#!/usr/bin/env python
#coding=UTF-8

import psutil
from IPy import IP
import dns.resolver
#print psutil.cpu_times()
#print psutil.cpu_count()
#print psutil.disk_partitions()
#print IP('192.168.12.12').iptype()

#print IP('192.168.2.0-192.168.3.255',make_net=True)
print IP('10.10.0.0/16').strNormal(3)
domain=raw_input('url:')
a=dns.resolver.query(domain,'N')
for i in a:
    for j in i.items:
        print j.address