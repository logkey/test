#!/usr/bin/env python
#coding=UTF-8
import os,sys,time,pycurl

ourl="https://www.baidu.com"
c=pycurl.Curl()
c.setopt(pycurl.URL,ourl)
c.setopt(pycurl.CONNECTTIMEOUT,5)
c.setopt(pycurl.TIMEOUT,5)
c.setopt(pycurl.NOPROGRESS,1)
c.setopt(pycurl.FORBID_REUSE,1)
c.setopt(pycurl.MAXREDIRS,1)
c.setopt(pycurl.DNS_CACHE_TIMEOUT,30)

indexfile=open(os.path.dirname(os.path.realpath(__file__))+"/content.txt",
c.setopt(pycurl.WRITEHEADER,indexfile)
c.setopt()
