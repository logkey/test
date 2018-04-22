#coding:utf-8
import paramiko
import sys
import time
import getpass

class SSH(object):

  def __init__(self):
    self.ip=''
    self.username=''
    self.password=''
    self.client=''
    self.chan=''
    self.cmd=''
    self.try_times=5

  def connect(self):
    while True:
      try:
        self.ip=input('IP:')
        self.username = input('Username:')
        self.password = getpass.getpass('Password:')
        self.client=paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.client.connect(self.ip,22,self.username,self.password)
        self.chan=self.client.invoke_shell()   
        self.chan.settimeout(1800)
        print('连接%s成功' % self.ip)
        print(self.chan.recv(65535).decode('utf-8'))
        return
      except Exception as e:
        print(e)
        if self.try_times!=0:
          print(u'连接%s失败,请重试' %self.ip)
          self.try_times-=1
        else:
          print(u'重试5次失败，结束程序')
          exit(1)

  def send(self):
    while self.cmd!='logout':
      self.cmd=input()
      self.chan.send(self.cmd+'\n')
      time.sleep(0.5)
      print(self.chan.recv(65535).decode('utf-8'),end='')

  def close(self):
    self.chan.close()
    self.client.close()

if __name__ == '__main__':
  host=SSH()
  host.connect()
  host.send()
  host.close()
