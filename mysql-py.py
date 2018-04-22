import os
import re
import mysql.connector

try:
    conn = mysql.connector.connect(host='127.0.0.1', port='3306', user='root', \
                                   password="9527", database="movie")
    cursor=conn.cursor()
    cursor.execute('select title,originaltitle,year,filenameandpath,path from videodb')
    # 取回的是列表，列表中包含元组
    res = cursor.fetchall()
    f=open(r'D:\renamelog.txt','w',encoding='utf-8')
    for row in res:
        if  os.path.exists(row[3]):
            oldname=os.path.split(row[3])
            ff=os.path.splitext(row[3])
            newname=row[0]+"_"+row[1]+"_"+row[2]+ff[1]
            #newpath=newname+ff[1]
            #os.chdir(row[4])
            #os.listdir(row[4])
            #print (os.getcwd())
            os.rename(row[3],row[4]+"\\"+newname)
            parentpath=os.path.split(oldname[0])
            os.rename(oldname[0],parentpath[0]+"\\"+row[0]+"_"+row[1]+"_"+row[2])
            #os.chdir("D:\\")
            print (row[3],"------>",newname)
            f.writelines(row[3]+"------>"+newname+"\n")
        else:
            print (row[3]+"...........不存在！！")
            f.writelines(row[3]+"...........不存在！！\n")
            continue
    
   
except mysql.connector.Error as e:
    print ('Error : {}'.format(e))
finally:
    cursor.close
    conn.close
    f.close()

