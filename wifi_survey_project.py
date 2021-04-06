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

graph = Graph(70000,70000)

graph.generate_heatmap()


#netscan = NetworkScan('192.168.1.5')

#netscan.iperf_scan()
#netscan.iperf_print()