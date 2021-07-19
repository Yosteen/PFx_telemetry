from pyVim import connect
from pyVmomi import vim
import os
os.system('clear')

vc = '192.168.41.5'
vcUname = 'administrator@vsphere.local'
vcPassword = 'Rtp@1234'
svmUname = 'vxflex'
svmPassword = 'VMwar3!!'


si = connect.SmartConnectNoSSL(host=vc,user=vcUname,pwd=vcPassword)
content = si.RetrieveContent()
print (content)






'''
si = connect.SmartConnectNoSSL(host=vc,user=vcUname,pwd=vcPassword)
content = si.RetrieveContent()
vm_view = content.viewManager.CreateContainerView(content.rootFolder,[vim.VirtualMachine],True)
sio_ips = [ vm_view.view[vm].summary.guest.ipAddress for vm in range (len(vm_view.view)) if "cale" in vm_view.view[vm].summary.config.name]
vm_view.Destroy()
mtus = []
for ip in sio_ips:
    
    try:
        u = svmUname
        p = svmPassword
        command = os.popen(f"sshpass -p {svmPassword}  ssh {svmUname}@{ip} '/sbin/ip a | grep mtu | grep eth '")
        output = command.read()
        ipa = output.split()
        mtu = [ip, ipa[14],ipa[17],ipa[27],ipa[30]]
    except IndexError:
        mtu = [ip,"Wrong Credentials",'N/A','N/A','N/A','N/A','N/A']
    mtus.append(mtu)
for i in mtus: print (i)

'''



'''
hosts = ['green-cc1esx-01.green.cnp.local','green-cc1esx-02.green.cnp.local']
vmkIpPrefix = "| awk '{print$1" + "\",\"" + "$2" + "\",\"" + "}'"
vipPrefix = "| awk '{print$4}'"
vmkIpCmd = f'esxcli network ip interface ipv4 get {vmkIpPrefix}'
vipIPsCmd = f'more /etc/vmware/esx.conf | grep IoctlMdmIPStr {vipPrefix}'
hostsVmkIPsDic={}
for host in hosts: 
    outputRaw = os.popen (f'sshpass -p Rtp@1234 ssh -l root {host} {vmkIpCmd}')
    outputRead = outputRaw.read()
    outputArr = outputRead.split(',')
    vmkIpDic={}
    for index,value in enumerate (outputArr,0):
        if 'vmk' in value: 
            DicKey = str(outputArr[index]).strip()
            DicValue = str(outputArr[index+1])
            vmkIpDic.update({DicKey:DicValue})
    #for k,v in vmkIpDic.items(): print (k,v)
    hostsVmkIPsDic.update({host:vmkIpDic})
    sioVipOutputRaw = os.popen (f'sshpass -p Rtp@1234 ssh -l root {host} {vipIPsCmd}')
    sioVipOutput = sioVipOutputRaw.read()
    sioVipOutputArr = sioVipOutput.split("=")
    sioVips = (sioVipOutputArr[1])[0:-2]
    sioVipsArr = sioVips.split(",")
    print (sioVipsArr)
'''

'''
for k,v in hostsVmkIPsDic.items(): 
    print (k,v)
    print ('####')
print (hostsVmkIPsDic['green-cc1esx-01.green.cnp.local'])

'''