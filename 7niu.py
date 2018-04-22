import qiniu,requests,re,sys,time,os
access_key = ''
secret_key = ''

##GET /v6/domain/list?tbl=<backetName> HTTP/1.1
##Host: api.qiniu.com  
##Content-Type: application/x-www-form-urlencoded  
##Authorization: QBox <AccessToken>


print('******wait******')
q = qiniu.Auth(access_key, secret_key)
bucket = qiniu.BucketManager(q)
bucket_dict=bucket.buckets()
rehttp=[]
dname=time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))
os.mkdir('c:\\QiniuURL-'+dname)
for x in bucket_dict[0]:
    i=0
    path='C:\\QiniuURL-'+dname+'\\'+x+'.txt'

    http=qiniu.http._get(url='http://api.qiniu.com/v6/domain/list?tbl='+x,params=None,auth=q)
    if http[0]!=[]:
        for y in range(0,len(http[0])):
            if re.search((r'.*justbehere.com.*'),http[0][y],re.S):
                rehttp=http[0][y]
                break
            rehttp=http[0][0]
    f=open(path,'w')
    marker=None   
    while x!='justbehere-live':
        _list=bucket.list(x,prefix=None, marker=marker, limit=1000, delimiter=None)
        if _list[0]!=None:
            marker=_list[0].get('marker')
            for y in _list[0].get('items'):
                key=y.get('key')    
                f.write('http://'+rehttp+'/'+key+'\n')
                i=i+1            
            if marker==None:
                break
    f.close()
    print('存储空间:<'+x+'>外链域名:<'+rehttp+'>总计:'+str(i)) 

print('******over******')
print('输入任意键退出...')
input()
sys.exit()

