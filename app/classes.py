from pyVim import connect
from pyVmomi import vim
import os

class Vcclass:
    def __init__(self,vc,uname,password,svmuname,svmpass):
        self._vc = vc
        self._uname = uname
        self._password = password
        self._svmuname = svmuname
        self._svmpass = svmpass

    def vmks(self):
        si = connect.SmartConnectNoSSL(host=self._vc,user=self._uname,pwd=self._password)
        content = si.RetrieveContent()
        host_view = content.viewManager.CreateContainerView(content.rootFolder,[vim.HostSystem],True)
        hosts = [host for host in host_view.view]
        hostnames = {host:host.summary.config.name for host in hosts}
        host_view.Destroy()
        dvs_view = content.viewManager.CreateContainerView(content.rootFolder,[vim.DistributedVirtualSwitch],True)
        pgs = {}
        for i in range(len(dvs_view.view)):
            pgss = dvs_view.view[i].portgroup
            pgs_i = {pg.config.key : pg.name for pg in pgss}
            pgs.update(pgs_i)
        dvs_view.Destroy()
        data = []
        for host in hosts:
            vnics = host.config.network.vnic
            data_temp = []
            for vnic in vnics:
                dvp = vnic.spec.distributedVirtualPort
                if dvp == None:
                    pgrp = "N/A"
                else:
                    pgkey = vnic.spec.distributedVirtualPort.portgroupKey
                    pgrp = pgs[pgkey]
                infodic = [vnic.device,vnic.spec.mtu,pgrp]
                data_temp.append(infodic)
            data_temp.sort()
            data_temp.insert(0,hostnames[host])
            data.append(data_temp)
        data.sort()
        return data 

    def getsiovms(self):
        si = connect.SmartConnectNoSSL(host=self._vc,user=self._uname,pwd=self._password)
        content = si.RetrieveContent()
        vm_view = content.viewManager.CreateContainerView(content.rootFolder,[vim.VirtualMachine],True)
        sio_ips = [ vm_view.view[vm].summary.guest.ipAddress for vm in range (len(vm_view.view)) if "cale" in vm_view.view[vm].summary.config.name]
        vm_view.Destroy()
        mtus = []
        for ip in sio_ips:
            try:
                u = self._svmuname
                p = self._svmpass
                command = os.popen(f"sshpass -p {p}  ssh {u}@192.168.45.64 '/sbin/ip a | grep mtu | grep eth '")
                output = command.read()
                ipa = output.split()
                mtu = [ip, ipa[14],ipa[17],ipa[27],ipa[30]]
            except IndexError:
                mtu = [ip,"Wrong Credentials",'N/A','N/A','N/A','N/A','N/A']
            mtus.append(mtu)
        return mtus
            
    def mtuping(self):
        si = connect.SmartConnectNoSSL(host=self._vc,user=self._uname,pwd=self._password)
        content = si.RetrieveContent()
        dc = content.rootFolder.childEntity[0]
        clusters = dc.hostFolder.childEntity
        #Create dictionary with cluster and cluster names
        clstrnms = {cluster:cluster.name for cluster in clusters }
        #This part will need to be looped for all clusters
        for cluster in clusters:
            print (clstrnms[cluster])
            print ('===========')
            hosts = cluster.host
            hstsnms = {host:host.summary.config.name for host in hosts}
            for host in hosts:
                print (hstsnms[host])
                vnics = host.config.network.vnic
                for vnic in vnics:
                    print (vnic.device,vnic.spec.ip.ipAddress)
            