import requests,lxml,json,socket,re,time
from bs4 import BeautifulSoup
#get url of error page
count=0
sum=0
n=209
# x = int(input("Start Page:"))
# y = int(input("Stop Page:"))
starttime=time.ctime()
print (starttime)

def download(imgurl,picname):
    pic = requests.get(imgurl, timeout=600)
    string = 'd:\\pic\\' + picname
    fp = open(string, 'wb')
    fp.write(pic.content)
    fp.close()

fpe = open('d:\\ErrorPage-log.txt', 'r')
lines=fpe.readlines()
fpe.close()

for p in lines:
    print('Page:'+p)
    try:
        r1=requests.get(url='https://alpha.wallhaven.cc/search?q=&search_image=&sorting=date_added&order=asc&page='+p).text
        #total next start page:12217
        soup=BeautifulSoup(r1,'lxml')
        i=soup.find_all('figure')
        for x in i:
            imgurl='https://wallpapers.wallhaven.cc/wallpapers/full/wallhaven-'+x.get('data-wallpaper-id')+'.jpg'
            print(imgurl)
            if count < 10000:
                fp = open('d:\\pic\\list\\' + str(n) + '.txt', 'a')
                fp.write(imgurl + '\n')
                fp.close()
                count = count + 1
                sum = sum + 1
            else:
                n = n+1
                fp = open('d:\\pic\\list\\' + str(n) + '.txt', 'a')
                fp.write(imgurl + '\n')
                fp.close()
                count = 1
                sum = sum + 1
    except:
        fp = open('d:\\ErrorPage-log2.txt', 'a')
        print('Error Page:'+p)
        fp.write(p)
        fp.close()
        continue
print(sum)
print(starttime)
print(time.ctime())


