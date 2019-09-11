# test
# !pip install import_ipynb

import sys

''' basic render do nothing '''    
class BasicRender(object):
        
    def render(self, title, contents):
        pass

''' simple render uses stdout '''
class SimpleRender(BasicRender):
    
    def render(self, title, contents):        
        print("title: \n{}".format(title))
        print("contents: \n{}".format(contents))
        print('\n\n\n')


''' Result analyzer analzyes commands result
    
    render(title, contents)

    title is a dict, like { 'host':<ip>, 'cmd':<command and parameter> }
    cotents is result of the command 
    
    example: ping 172.16.2.2 -c 4 at host 172.16.1.3
    
    title : {'host':'172.16.1.3', 'cmd':'ping 172.16.2.2 -c 2'}
    contents:     
        Command exited with status 0.
        === stdout ===
        PING 172.16.2.2 (172.16.2.2) 56(84) bytes of data.
        64 bytes from 172.16.2.2: icmp_seq=1 ttl=46 time=11.7 ms
        64 bytes from 172.16.2.2: icmp_seq=2 ttl=46 time=10.5 ms

        --- 172.16.2.2 ping statistics ---
        2 packets transmitted, 2 received, 0% packet loss, time 1001ms
        rtt min/avg/max/mdev = 10.590/11.177/11.764/0.587 ms
    
'''
class ResultAnalyzer(BasicRender):
    
    def __init__(self, hide=False, analyze=True):
        self.hide = hide
        self.rt_analyze = analyze
        self.analyzed = False
        self.cur = 0
        self.notes = []
        self.results = []
         
    def render(self, title, contents):
        self.notes.append({'title': title, 'contents': contents})
        if self.rt_analyze == True:
            self.__analyze()        
        if self.hide == False:
            print("title: \n{}".format(title))
            print("contents: \n{}".format(contents))
            if self.rt_analyze == True:
                # print analyzing result
                i = len(self.notes) - 1 
                print("\nresult: {}".format('success' if self.results[i] else 'fail'))           
            print('\n\n\n')
            
    def __analyze(self):
        result_ok = True 
        if self.analyzed == False or sel.cur < len(self.notes):             
            # todo: anaylzing
            pass
        self.results.append(result_ok)
        self.cur += 1
        
    def analyze(self):
        self.__analyze()
        # todo, print results     
