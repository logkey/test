import requests,lxml,json,socket,re,time
from bs4 import BeautifulSoup
#get url of each page
count=0
sum=0
n=209
x = int(input("Start Page:"))
y = int(input("Stop Page:"))
starttime=time.ctime()
print (starttime)

def download(imgurl,picname):
    pic = requests.get(imgurl, timeout=600)
    string = 'd:\\pic\\' + picname
    fp = open(string, 'wb')
    fp.write(pic.content)
    fp.close()

for p in range(x, y+1):
    print('Page:'+str(p))
    try:
        r1=requests.get(url='https://alpha.wallhaven.cc/search?q=&search_image=&sorting=date_added&order=asc&page='+str(p)).text
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
        fp = open('d:\\ErrorPage-log.txt', 'a')
        print('Error Page:'+str(p))
        fp.write(str(p)+'\n')
        fp.close()
        continue
print(sum)
print(starttime)
print(time.ctime())


