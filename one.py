import requests,json,socket,re
from bs4 import BeautifulSoup
class Getmyip:
    def getip(self):
        try:
            myip = self.visit("http://www.ip138.com/ip2city.asp")
        except:
            try:
                myip = self.visit("http://ip.chinaz.com/")
            except:
                try:
                    myip = self.visit("http://www.ip.cn/?jdfwkey=yibih2")
                except:
                    myip = "So sorry!!!"
        return myip
    def visit(self,url):
        opener = requests.get(url)
        stro = opener.text
        return re.search('\d+\.\d+\.\d+\.\d+',stro).group(0)
class temp:
    def temp(self):
        ip=Getmyip().getip()
        r=requests.get(url='http://ip.taobao.com/service/getIpInfo.php?ip=%s'%ip)
        print (str(r.status_code)+'\n******************')
        print(r.json())
        print(r.text)
    def haha():
        print('<><><><><><><><><><><><>')

if __name__=='__main__':

    r=requests.get(url='https://alpha.wallhaven.cc/search?q=&search_image=&sorting=date_added&order=asc&page='+p)

    #    for n in range(0,250,25):
    #       r=requests.get(url='https://movie.douban.com/top250?start='+str(n)+'&filter=')
    #    print(r.url)
    #    print(r.text)
    #    ttt=re.search((r'(?<=百科解释)(.*)(?=查看百科)'),r.text,re.S)
    #    print(ttt.group(0))
    #    temp.haha()
    soup=BeautifulSoup(r.content,'html.parser',from_encoding='utf-8')
    i=soup.find_all('a',class_='preview')
    for x in i:
        x=
        print(x.get('href'))
