import os  
import time  
  
 
source = r'D:\987654'   
target_dir = r'D:\testRAR\web'  
target = target_dir + time.strftime('%Y%m%d%H%M%S') + '.rar'  
rar_command = r'"C:\Program Files\WinRAR\WinRAR.exe" A %s %s -r' % (target,source)
#rar_command = "WinRAR A %s %s -r" % (target,source)  

if os.system(rar_command) == 0:  
    print ('Successful backup to', target)
else:  
    print ('Backup FAILED')   
