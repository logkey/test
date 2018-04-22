
#! /usr/bin/env python
# coding=utf-8 ##

import urllib.request
import re
import sys

# 获取当前系统编码格式
#type = sys.getfilesystemencoding()
j = 0
for  i in range(0, 100, 25):
    url = 'http://movie.douban.com/top250?start='
    hash = str(i)+'&filter=&type='
    url = url + hash
    print(url)
    # 读取url内容
    content = str(urllib.request.urlopen(url).read())
    # 转换编码
#    content = content.decode("UTF-8").encode(type)
    # 读取电影名称
    match = re.findall(r'<span\s+class="title"><\/span>', content)
    print (match)
    # 读取分数
    match2 = re.findall(r'<span\s+class="rating5-t">([0-9.]+)<\/span>', content)
    print (match2)
    # 压缩到一个列表
    zipc = zip(match, match2)
    # 打开文档
    f = open('douban.txt', 'a')
    # 写入文件
    for name in zipc:
        #大于8分的电影
      #  if float(name[1])>=8:
            f.write(name[0])
            f.write(name[1])
            f.write('\n')
            j = j + 1
            print (name[0])
            print (j)            
print ('总共抓取电影数据'+ str(j) +'条').decode("UTF-8").encode(type)
print ('done')
f.close()
