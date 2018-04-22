import sqlite3,re
count=0
sum=0
n=1
list=[]
conn=sqlite3.connect('D:\Code\wallpaper\wallpaperdb.db')
c=conn.cursor()
c.execute('select id from localfile order by id')
res=c.fetchall()
for v in res:
    list.append(v[0])


for x in range(1,556000):
    if x not in list:
        imgurl = 'https://wallpapers.wallhaven.cc/wallpapers/full/wallhaven-' + str(x) + '.jpg'
        if count < 10000:
            fp = open('d:\\pic\\hidelist\\' + str(n) + '.txt', 'a')
            fp.write(imgurl + '\n')
            fp.close()
            count = count + 1
            sum = sum + 1
        else:
            n = n + 1
            fp = open('d:\\pic\\hidelist\\' + str(n) + '.txt', 'a')
            fp.write(imgurl + '\n')
            fp.close()
            count = 1
            sum = sum + 1

c.close()
conn.commit()
conn.close()
print(sum)