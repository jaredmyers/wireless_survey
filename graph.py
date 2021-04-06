# sample class that will probably be interface
# with matplotlib for heatgraphing
#

import numpy as np
import numpy.random
import matplotlib.pyplot as plt

class Graph:
    '''Graph Class for heatmap + anything else'''
    
    def __init__(self, x, y):
        '''constructor for graph class'''
        self.x = np.random.randn(x)
        self.y = np.random.randn(y)
        
    def generate_heatmap(self):
        '''generates heat map from x, y'''
        
        #Create heatmap
        img = plt.imread('apt.png')
        heatmap, xedges, yedges = np.histogram2d(self.x, self.y, bins=(128,128))
        extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]
        
        #Plot heatmap
        plt.clf()
        plt.title('Crappy Heatmap Example')
        plt.ylabel('y')
        plt.xlabel('x')
        plt.imshow(heatmap, extent=extent)
        plt.show()
        
    #def test_bg(self):
        
        
    
    