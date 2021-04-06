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


#Create data
#x = np.random.randn(70000)
#y = np.random.randn(70000)

#Create heatmap
#heatmap, xedges, yedges = np.histogram2d(x, y, bins=(128,128))
#extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]

#Gimme colorbar
#hm=plt.imshow(marks, cmap='Blues',interpolation="nearest")

#Plot heatmap
#plt.clf()
#plt.title('Crappy Heatmap Example')
#plt.ylabel('y')
#plt.xlabel('x')
#plt.imshow(heatmap, extent=extent)
#plt.show()

#plt.imshow(heatmap.T, extent=extent, origin='lower')
#plt.show()