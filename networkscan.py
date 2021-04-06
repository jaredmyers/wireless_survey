# sample class that will probably
# become the code that interfaces with the cmdline

import os
import json

class NetworkScan:
    '''Network Scan Class'''
    #species = 'canis failiaris'
    def __init__(self, iperf_ip):
        '''constructor for NetworkScan'''
        self.iperf_ip = iperf_ip
        
    def iperf_scan(self):
        '''performs iperf3 scan, outputs JSON file for parsing'''
        
        cmd = f'iperf3 -c {self.iperf_ip} -J > iperf_json'
        os.system(cmd)
        
    def iperf_print(self):
        '''prints out iperf3 JSON data from file'''
        
        if not os.path.isfile(f'iperf_json'):
            print('iperf3 output file does not exist');
            return    
        
        with open('iperf_json', 'r') as inF:
            data = json.load(inF)
        
        for i in data['intervals']:
            print(i['streams'][0]['bits_per_second'])
        
        print(' ')
        print(data['end']['sum_received']['bits_per_second'])
        