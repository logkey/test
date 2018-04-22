import sqlite3,re

conn=sqlite3.connect('D:\Code\wallpaper\wallpaperdb.db')
c=conn.cursor()
#c.execute('create table wallpaper(id int primary key,filename varchar(30),filetype varchar(10),width int,height int,url varchar(200))')

fp = open('d:\\total.txt', 'r')
lines=fp.readlines()
fp.close()
c.execute('delete from wallpaper')
for line in lines:
    filename=re.search('wallhaven-.*',line).group()
    id=re.search('\d+',line).group()
    c.execute('insert into wallpaper(id,filename,filetype,url) values (?,?,?,?)',(id,filename,line.split('.')[-1],line))
c.execute('select count(*) from wallpaper')
print(c.fetchall())
c.close()
conn.commit()
conn.close()
