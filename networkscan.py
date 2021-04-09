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
        
    def iperf_print(self, grid_points):
        '''prints out iperf3 JSON data from file'''
        
        avg_bits_second = None
        cmd = f'iperf3 -c {self.iperf_ip} -J > iperf_json'
        
        while grid_points > 0:
            
            # should do a timeout with this or subprocess
            os.system(cmd)
            print('iperf command complete')
        
            if not os.path.isfile(f'iperf_json'):
                print('iperf3 output file does not exist');
                return    
        
            with open('iperf_json', 'r') as inF:
                data = json.load(inF)
                
            print('JSON loaded')
            
            #for i in data['intervals']:
                #print(i['streams'][0]['bits_per_second'])
            #print(' ')
        
            # grab average bits per second, convert to MBits/s with 2 decimals
            try:
                avg_bits_second = data['end']['sum_received']['bits_per_second']
                avg_bits_second = round((avg_bits_second / 1000000), 2)
            except KeyError:
                print('iperf connection error')
            print('JSON read')
            print(avg_bits_second)
            
            grid_points = grid_points - 1
        
        