import sys

ncltools_path = 'E:\\wangfl-workspace\\20_projects\\20_ncltools\\scripts'
if ncltools_path not in sys.path:
    sys.path.append(ncltools_path)
data_path = 'E:\\wangfl-workspace\\20_projects\\20_ncltools\\data'
if data_path not in sys.path:
    sys.path.append(data_path)

import json
from fabric import Connection
from render import *

''' ExperimentDescription is a json string holding static description of experiment '''
class ExperimentDescription(object):
    
    def __init__(self, fname):    
        self.filename = fname
        fn = open(fname, 'rb')
        self.expDesp = json.load(fn)
        fn.close()
            
    def getExperimentDescription(self):
        return self.expDesp
    
    def getExperimentFileName(self):
        return self.filename
    
    def getExperimentDomain(self):
        return self.expDesp["ExperimentDomainName"]
        
    def getNodeDescription(self, nodeidx):
        return self.expDesp["Nodes"][nodeidx]
    
    def getNumberOfNodes(self):
        return len(self.expDesp["Nodes"])

    def getNodeName(self, nodeidx):
        return self.expDesp["Nodes"][nodeidx]["Name"]
        
    def getVmDescription(self, nodeidx, vmidx):
        return self.expDesp["Nodes"][nodeidx]["VMs"][vmidx]
   
    def getNumberOfVms(self, nodeidx):
        return len(self.expDesp["Nodes"][nodeidx]["VMs"])
   
    def getVmName(self, nodeidx, vmidx):
        return self.expDesp["Nodes"][nodeidx]["VMs"][vmidx]["Name"]
    
    def printNodesAndVms(self):

        k=0
        m=self.getNumberOfNodes()

        while k<m:

            print(self.getNodeName(k))

            i = 0
            n = self.getNumberOfVms(k)
            while i<n:
                print("  " + self.getVmName(k, i))
                i += 1
            print("")

            k += 1
     

        
''' Vagrantfile holds static description of a node '''
class Vagrantfile(object):
    
    def __init__(self, fname):    
        pass
    
    def getVagrantfile():
        pass


''' Node holds connection to a phsycal node '''
class Node (object):

    def __init__(self, node_p, domain=''):    
        self.gateway = 'users.ncl.sg'
        self.node_p = node_p        
        self.name = node_p['Name']
        self.domain = domain
        self.connection = None
        self.set_user_passwd()
    
    # set user and password 
    def set_user_passwd(self, user=None, passwd=None):
        if user == None:
            self.user = 'ntechni3'
            self.passwd = 'deterinavm1'
        else:
            self.user = user
            self.passwd = passwd
    
    # internal function to check connection 
    def __check_connection(self):
        
        if self.connection == None or self.connection.is_connected == False :
            c = Connection(host=self.gateway, user=self.user)
            c.connect_kwargs.password = self.passwd
            
            h = self.user + '@' + self.node_p['Name']+ '.' + self.domain
            self.connection = Connection(host=h, gateway=c)
            self.connection.connect_kwargs.password = self.passwd
 
        else:
            pass
        
        return True
    
    # run command at node 
    def run(self, cmd):
        self.__check_connection()
        try:
            result = self.connection.run(cmd,  hide=True)
        except Exception as ex:
            template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            result = message
            print(message) 
            raise
        return result
    
    # check internet access at node
    def check_internet(self):
        self.__check_connection()
        return self.connection.run("ping 8.8.8.8 -c 2",  hide=True) 
    
    # command: vagrant status 
    def vagrant_status(self, vm_n=None):
        self.__check_connection()
        if vm_n==None:
            return self.connection.run("vagrant status",  hide=True)
        else:
            cmd = "vagrant status "+vm_n
            return self.connection.run(cmd,  hide=True)
    
    # command: vagrant up
    def vagrant_up(self, vm_n=None):
        self.__check_connection()
        if vm_n==None:
            return self.connection.run("vagrant up",  hide=True)
        else: 
            cmd = "vagrant up "+vm_n
            return self.connection.run(cmd,  hide=True)            
    
    # vagrant halt
    def vagrant_halt(self, vm_n=None):
        self.__check_connection()
        if vm_n==None:
            return self.connection.run("vagrant halt",  hide=True)
        else: 
            cmd = "vagrant halt "+vm_n
            return self.connection.run(cmd,  hide=True)            
    
    # command: vagrant provision
    def vagrant_provision(self, vm_n=None):
        self.__check_connection()
        if vm_n==None:
            return self.connection.run("vagrant provision",  hide=True)
        else: 
            cmd = "vagrant provision "+vm_n
            return self.connection.run(cmd,  hide=True)            
    
    # command: vagrant destroy
    def vagrant_destroy(self, vm_n=None):
        self.__check_connection()
        if vm_n==None:
            return self.connection.run("vagrant destroy",  hide=True)
        else: 
            cmd = "vagrant destroy "+vm_n
            return self.connection.run(cmd,  hide=True)            
    
    
    def diagnose(self):
        print(self.connection)
    
    def close_connection(self):
        if self.connection != None:    
            self.connection.close()
            self.connection = None 
    


    
''' Vm  '''
class Vm (object):
    
    def __init__(self, vm_p, node=None):    
        self.node = node
        self.vm_p = vm_p 
        self.name = vm_p['Name']
    
    def run(self, cmd):
        cmd1 = "vagrant ssh "+self.vm_p['Name'] 
        cmd2 = " -c " + "'" + cmd + "' "
        # print(cmd1+cmd2)
        return self.node.run(cmd1+cmd2)
                
    def check_internet(self):
        return self.run("ping 8.8.8.8 -c 2") 
        
    def ping_ip(self, ip):
        cmd1 = "vagrant ssh "+self.vm_p['Name'] 
        cmd2 = " -c " + "'ping " + ip + " -c 2' "
        try:
            result = self.node.run(cmd1+cmd2)
        except:
            raise
        return result
        
    def ping_ips(self, ips):       
        result = ""
        for ip in ips:
            try:
                result += str(self.ping_ip(ip))
                result += "\n"
            except:
                raise
        return result

    def ip_addroute(self, ip_group, gw_ip):
        result = ""
        cmd1 = "vagrant ssh "+self.vm_p['Name'] 
        cmd2 = " -c " + "'ip r del " + ip_group +"'"
        result += str(self.node.run(cmd1+cmd2)) 
        cmd3 = " -c " + "'ip r add "+ip_group+" via "+ gw_ip + "'"        
        result += self.node.run(cmd1+cmd3)
        return result
    
    def ip_printroute(self):
        cmd1 = "vagrant ssh "+self.vm_p['Name'] 
        cmd2 = " -c 'ip r'"
        return self.node.run(cmd1+cmd2)
        

                
''' Experiment represents a running experiment '''    
class Experiment(object):
    
    def __init__(self, jsonfile=None, expDesp:ExperimentDescription=None, render:BasicRender=BasicRender()):
        
        if jsonfile != None:
            self.expDesp=ExperimentDescription(jsonfile)
        else:
            self.expDesp = expDesp
            
        if self.expDesp != None:
            self.domain = expDesp.getExperimentDomain()        
            self.__instanciateNodesAndVms()
        
        self.render = render
        
    def __instanciateNodesAndVms(self):
        self.nvs = []
        self.vmips =[]
        i = 0
        m = self.expDesp.getNumberOfNodes()
        while i<m:
            node = Node(self.expDesp.getNodeDescription(i), self.domain)      
            vms =[]
            j = 0
            n = self.expDesp.getNumberOfVms(i)
            while j<n:
                vm_p = self.expDesp.getVmDescription(i,j)
                vms.append(Vm(vm_p, node))
                for net in vm_p['Nets']:  
                    self.vmips.append(net['IP'])
                j += 1
            # self.nodes.append([node, vms])
            self.nvs.append({'node':node, 'vms':vms})
            i += 1
    
    def printNodesAndVms(slef):
        print(self.nodes)
    
    # check internet access at all nodes and vms  
    def check_internet(self, node_i = None, vm_i = None, exclude=[]):
    
        result = ""
        for nv in self.nvs:  # self.nodes:
            rslt = str(nv['node'].check_internet())
            result += rslt
            self.render.render("ping@"+nv['node'].name+"\n", rslt)
            for vm in nv['vms']:
                if vm.name in exclude:
                    continue
                rslt = str(vm.check_internet())
                result += rslt
                self.render.render("ping@"+vm.name+"\n", rslt)
                
        return result
    
    # check connectivity at all vms 
    def check_connectivity(self, node_i = None,  vm_i = None, exclude=[]):
        
        result = ""
        ips = self.vmips
        if node_i == None:
            for nv in self.nvs:
                for vm in nv['vms']:
                    if vm.name in exclude:
                        continue
                   
                    for ip in ips:
                        try:
                            rslt = str(vm.ping_ip(ip))
                        except:
                            continue
                        self.render.render("ping@"+vm.name+"\n", rslt)
                        result += rslt
        else:
            if vm_i == None:
                for vm in self.nvs[node_i]['vms']:
                    if vm.name in exclude:
                        continue
                    result += str(vm.ping_ips(ips))
            else:
                vm = self.nvs[node_i].vms[vm_i]
                result += str(vm.ping_ips(ips))
                
        return result
    
    
    def getNode(self, node_i):
        return self.nvs[node_i]['node']
    
    def getNodeByName(self, node_n):
        for nv in self.nvs:
            if nv['node'].name == node_n:
                return nv['node']
        return None 
    
    def getVm(self, node_i, vm_i):
        return self.nvs[node_i]['vms'][vm_i]
            
    def getVmByName(self, node_n, vm_n):
        for nv in self.nvs:
            if nv['node'].name == node_n:
                for vm in nv['vms']:
                    if vm.name == vm_n:
                        return vm
        return None
    
    def getNodeName(self, node_i=None):
        l = []
        if node_i==None:
            for nv in self.nvs:
                l.append(nv['node'].name)
            return l
        else:
            if node_i >=0 and node_i< len(self.nvs):
                return self.nvs[node_i]['node'].name
            else: 
                return None
        
    def getVmName(self, node_n=None, vm_i=None):
        l = []
        for nv in self.nvs:
            if node_n == None or nv['node'].name == node_n:
                if vm_i==None:
                    for vm in nv['vms']:
                        l.append(vm.name)
                    return l
                else:
                    if vm_i >=0 and vm_i < len(nv['vms']):
                        return nv['vms'][vm_i].name
                    else:
                        return None
        
class Kali(Vm):
    pass
    
class Win7(Vm):
    pass
    
class Router(Vm):
    pass
    
class Ubuntu(Vm):
    pass
    
class Web(Ubuntu):
    pass
    
class Email (Ubuntu):
    pass
    
class Dns (Ubuntu):
    pass 
    
class Db (Ubuntu):
    pass
    
