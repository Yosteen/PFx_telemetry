from app.classes import Vcclass
import os
ip = '192.168.41.5'
uname = 'administrator@vsphere.local'
password = 'Rtp@1234'
svm_u = 'vxflex'
svm_p = 'VMwar3!!'

os.system('clear')
lvc = Vcclass(ip,uname,password,svm_u,svm_p)
a = lvc.mtuping() 

