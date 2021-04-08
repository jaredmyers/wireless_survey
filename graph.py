# sample class that will probably be interface
# with matplotlib for heatgraphing
#

import numpy as np
import numpy.random
import matplotlib.pyplot as plt
from scipy.ndimage.filters import gaussian_filter

import pandas as pd
import plotly as plty
import seaborn as sns
import plotly.express as px

class Graph:
    '''Graph Class for heatmap + anything else'''
    
    def __init__(self, x, y):
        '''constructor for graph class'''
        self.x = np.random.randn(x)
        self.y = np.random.randn(y)
       # self.uniform_data = np.random.rand(20,20)
        
    def generate_heatmap(self):
        '''generates heat map from x, y'''
       
        # regular matplotlib attempt
        flight_data = pd.read_csv('flights.csv')
        flight_data = flight_data.pivot('month', 'year', 'passengers')
        plt.imshow(flight_data, cmap='jet', interpolation='bilinear')
        plt.show()
        
              
        '''
        
        # df = pd.read_csv('test_csv.csv')
       # print(df.head(10))
       # symbol = ((np.asarray(df['Symbol'])).reshape(5,5))
       # percentage = ((np.asarray(df['Change'])).reshape(5,5))
        
       # result = df.pivot(index='Yrows',columns='Xcols',values='Change')
       # print(result)
        
        
        
        
        flight_data_smooth = gaussian_filter(flight_data, sigma=1)
        
        # from seaborn attempt
        #flight_data = sns.load_dataset('flights')
        
        display_flight = sns.heatmap(flight_data, cmap='coolwarm', cbar=False)



       # This example runs with pcolormesh
        x = [1, 2, 3, 4, 5]
        y = [0.1, 0.2, 0.3, 0.4, 0.5]
       
        intensity = [
            [130,10,15,20,25],
            [30,35,40,45,50],
            [55,60,65,70,75],
            [80,85,90,95,100],
            [105,110,115,120,125]]
       
        x, y = np.meshgrid(x,y)
       
        intensity = np.array(intensity)
        
        plt.pcolormesh(x,y,intensity)
        plt.colorbar()
        plt.show()
        #------------------------------------
       
        #Create heatmap
        #img = plt.imread('apt.png')
        #heatmap, xedges, yedges = np.histogram2d(self.x, self.y, bins=(128,128))
        #extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]
        
        #Plot heatmap
        #plt.clf()
        # plt.title('Crappy Heatmap Example')
        #plt.ylabel('y')
        #plt.xlabel('x')
        #plt.imshow(heatmap, extent=extent)
        #plt.show()
        #ax = sns.heatmap(self.uniform_data, linewidth=0-.5)
       #plt.show()
        
    #def test_bg(self):
        
        '''
    
    