#!/usr/bin/env python
#coding=UTF-8

import nmap
import json
host='192.168.233.129'
port='22'
hosts=['192.168.233.129','192.168.233.200']


def scan_host_state(hosts,port='22'):
    nm = nmap.PortScanner()
    for i in range(len(hosts)):
        nm.scan(hosts[i],port)
        if nm.has_host(hosts[i]):
            print hosts[i]+'   On'
        else:
            print hosts[i]+'   Off'

def scan_port(host,port='22'):
    nm=nmap.PortScanner()
    re=nm.scan(host,port)
    print re.get('scan')

#scan_host_state(hosts)
scan_port(host)

