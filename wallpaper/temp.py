import sqlite3,re,os


def GetFileList(dir, fileList):
    newDir = dir
    if os.path.isfile(dir):
        fileList.append(dir)
    elif os.path.isdir(dir):
        for s in os.listdir(dir):
            newDir = os.path.join(dir, s)
            GetFileList(newDir, fileList)
    return fileList

list = GetFileList('D:\\ALL', [])
conn=sqlite3.connect('D:\Code\wallpaper\wallpaperdb.db')
c=conn.cursor()
c.execute('delete from localfile')
for e in list:
    #print (e)
    filename=re.search('wallhaven-.*',e).group()
    id=re.search('(?<=-).*\d',e).group()
    url='https://wallpapers.wallhaven.cc/wallpapers/full/'+filename
    c.execute('insert into localfile (id,filename,filetype,url) values (?,?,?,?)',(id,filename,e.split('.')[-1],url))

c.close()
conn.commit()
conn.close()
