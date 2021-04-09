# Home WiFi Survey Tool
# main
#

import numpy as np
import numpy.random
import matplotlib.pyplot as plt
import os
import subprocess

from networkscan import NetworkScan
from graph import Graph

#iperf_server_ip = '10.0.0.74'


#netscan = NetworkScan(iperf_server_ip)

#netscan.iperf_scan()
#netscan.iperf_print(1)

graph = Graph()
graph.generate_heatmap()