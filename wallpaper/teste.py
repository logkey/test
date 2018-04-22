import re,requests,lxml
from bs4 import BeautifulSoup

# r2=requests.get(url='https://alpha.wallhaven.cc/wallpaper/7').text
# soup2 = BeautifulSoup(r2, 'lxml')
# i2 = soup2.find_all('img', id='wallpaper')
# for x in i2:
#      print ('wallhaven-'+x.get('data-wallpaper-id')+x.get('data-wallpaper-width')+'x'+x.get('data-wallpaper-height'))
#
# text = 'https://wallpapers.wallhaven.cc/wallpapers/full/wallhaven-550508.png'
# m = re.search(r'wallhaven-.*',text)
# print (m.group())
#
# r1 = requests.get(url='https://alpha.wallhaven.cc/search?q=&search_image=&sorting=date_added&order=asc&page=1').text
# soup = BeautifulSoup(r1, 'lxml')
# i = soup.find_all('figure')
# for x in i:
#     print (x.get('data-wallpaper-id'))
v=0
fp = open('d:\\ErrorPage-log.txt', 'r')
lines=fp.readlines()
fp.close()
for p in lines:
    print('Page:'+p)

    r1=requests.get(url='https://alpha.wallhaven.cc/search?q=&search_image=&sorting=date_added&order=asc&page='+str(p)).text
    #total next start page:12217
    soup=BeautifulSoup(r1,'lxml')
    i=soup.find_all('figure')
    for x in i:
        imgurl='https://wallpapers.wallhaven.cc/wallpapers/full/wallhaven-'+x.get('data-wallpaper-id')+'.jpg'
        print(imgurl)
    v=v+1

    #fp = open('d:\\ErrorPage-log2.txt', 'a')
    #print('Error Page:'+str(p))
    #fp.write(str(p)+'\n')
    #fp.close()

print('All Done!total:'+str(v))