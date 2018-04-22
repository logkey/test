import requests,lxml,json,socket,re,time
from bs4 import BeautifulSoup
#get url of each picture
count=0
sum=0
n=1
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
        #r1.add_header("User-agent", "Mozilla 5.10")
        soup=BeautifulSoup(r1,'lxml')
        i=soup.find_all('a',class_='preview')

        for r2 in i:
            r2=requests.get(url=r2.get('href')).text
            soup2=BeautifulSoup(r2,'lxml')
            i2 = soup2.find_all('img', id='wallpaper')
            for r3 in i2:
                imgurl='https:'+r3.get('src')
                print(imgurl)
                # picname=re.search(r'wallhaven-.*',imgurl,re.S).group()
                # picsize=r3.get('data-wallpaper-width')+'x'+r3.get('data-wallpaper-height')
                # picname=picname.replace('.','-'+picsize+'.')
                # download(imgurl,picname)
                if count < 999:
                    fp = open('d:\\pic\\list\\' + str(n) + '.lst', 'a')
                    fp.write(imgurl + '\n')
                    fp.close()
                    count = count + 1
                    sum = sum + 1
                else:
                    n = n+1
                    fp = open('d:\\pic\\list\\' + str(n) + '.lst', 'a')
                    fp.write(imgurl + '\n')
                    fp.close()
                    count = 1
                    sum = sum + 1
    except:
        fp = open('d:\\pic\\list\\ErrorPage-log.txt', 'a')
        print('Error Page:'+str(p))
        fp.write(str(p)+'\n')
        fp.close()
        continue
print(sum)
print(starttime)
print(time.ctime())


