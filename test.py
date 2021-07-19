from app.classes import Vcclass
import os
ip = '192.168.41.5'
uname = 'administrator@vsphere.local'
password = ''
svm_u = 'vxflex'
svm_p = ''

os.system('clear')
lvc = Vcclass(ip,uname,password,svm_u,svm_p)
a = lvc.mtuping() 

