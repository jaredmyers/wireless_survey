# WiFi scan tool GUI
# 
#

import sys
import requests
import wget
import os

import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.image as mpimg
import json

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas 
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar 
 
from PyQt5 import QtGui
from PyQt5.QtWidgets import *

from PyQt5 import QtCore
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt

from PyQt5.QtCore import QThreadPool

import random
from threading import Thread
from multiprocessing import Process


class Window(QWidget):

    def __init__(self, y_ax, x_ax, iperf_ip):
        '''constructor for scantool'''
        super().__init__()
        self.setWindowTitle("WiFi Survey Tool")
        self.resize(800, 500)
        self.threadpool = QThreadPool()

        #--- Create a top-level layout-
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        # Grid point number for current floorplan
        # IP for iperf
        self.total_gp = y_ax * x_ax
        self.current_gp = 0
        self.y_ax = y_ax
        self.x_ax = x_ax
        self.iperf_ip = iperf_ip
        
        self.current_y = 1
        self.current_x = 1
        
        # Array for realtime storage, default 0s, matrix totalpoints x 3
        self.a = np.zeros(shape=(self.total_gp,3))
        self.mbit_data_list = [0]*self.total_gp
        
        # Floorplan Display ---------------------
        self.canvas = None
        self.fig = None
        
        #----------------------- Labels
        # Floorplan Tab---------------------
        self.grid_info_txt = QLabel()
        self.mbit_info_txt = QLabel()
        self.plot_button = QPushButton('Scan Data Point')
        self.finish_button = QPushButton('Finish')
        
        
        # Selection Tab-------------------
        #self.searchTextField = QLineEdit()
        #self.ph1 = QLabel()

        # Create the tab widget w/2tabs
        tabs = QTabWidget()
        tabs.addTab(self.floorplan_tabUI(), "Floorplan")
        tabs.addTab(self.selection_tabUI(), "Selections")
        layout.addWidget(tabs)

    def floorplan_tabUI(self):
        '''Create the Floorplan page UI.'''
        
        floorplan_tab = QWidget()
        layoutV = QVBoxLayout()
        layoutH = QHBoxLayout()
        
        # for two buttons lower left
        layoutH2 = QHBoxLayout()
        layoutH2.addWidget(self.plot_button)
        layoutH2.addWidget(self.finish_button)
        
        self.grid_info_txt.setText(f"{self.current_gp}/{self.total_gp} gridpoints")
        self.sns_plot_start()
        
        layoutV.addWidget(self.canvas)
        layoutH.addLayout(layoutH2)
        layoutH2.addWidget(self.plot_button, alignment=QtCore.Qt.AlignLeft)
        layoutH2.addWidget(self.finish_button)
        layoutH.addWidget(self.mbit_info_txt)
        layoutH.addWidget(self.grid_info_txt)
        layoutV.addLayout(layoutH)
        
        floorplan_tab.setLayout(layoutV)

        # Connect interface buttons
        self.plot_button.clicked.connect(self.scan_data_point)
        self.finish_button.clicked.connect(self.plot_finished_graph)
        
        return floorplan_tab

    def selection_tabUI(self):
        '''Create the Selection page UI.'''
        
        selection_tab = QWidget()
        layoutV = QVBoxLayout()

        selection_tab.setLayout(layoutV)

        return selection_tab
                          
    def plot_start_graph(self):
        '''Adds starter flooplan to floorplan tab'''
        
        self.fig = plt.figure()
        
        # take in floorplan image, set extents, etc
        extents = [0,2500, 0, 1500]
        img = plt.imread("input/house3.png")
        image = plt.imshow(img, extent=extents)
        plt.yticks([])
        plt.xticks([])

        self.canvas = FigureCanvas(self.fig)
        
    def sns_plot_start(self):
        '''Adds starter flooplan to floorplan tab'''
        '''Using seaborn'''
        
        floorplan_data = self.rt_dataframe()
        
        self.fig = plt.figure()
        
        h = sns.heatmap(floorplan_data, cmap='coolwarm', cbar=False, alpha=0.1,
                        zorder=2, square=True, annot=False, fmt='g', cbar_kws={'label': 'TCP DL Mbit/s'})
        
        # setting ticks for heatmap
        h.set_yticklabels([2,6,10,14,18,22,26,30,34])
        h.set_xticklabels([2,6,10,14,18,22,26,30,34,38,42,46,50])
        h.set(xlabel = 'Feet', ylabel = 'Feet')
        
        # read in floorplan - set size and z
        my_image = mpimg.imread('input/house3.png')
        h.imshow(my_image, aspect=h.get_aspect(), extent=h.get_xlim() + h.get_ylim(), zorder=1)
        
        # take in floorplan image, set extents, etc
        #extents = [0,2500, 0, 1500]
        #img = plt.imread("input/house3.png")
        #image = plt.imshow(img, extent=extents)
        #plt.yticks([])
        #plt.xticks([])

        self.canvas = FigureCanvas(self.fig)
        
    def plot_finished_graph(self):
        '''Displays finished graph when finish is clicked'''
        '''Currently display seaborn block heatgraph'''
        
        floorplan_data = self.generate_dataframe()
        
        # clear current contents of heatmap on floorplan tab
        self.fig.clear()
        
        # establish seaborn heatmap to overlay ontop of floorplan
        h = sns.heatmap(floorplan_data, cmap='coolwarm', cbar=True, alpha=0.7,
                        zorder=2, square=True, annot=True, fmt='g', cbar_kws={'label': 'TCP DL Mbit/s'})
        # flip y axis
        h.invert_yaxis()
        
        # setting ticks for heatmap
        h.set_yticklabels([2,6,10,14,18,22,26,30,34])
        h.set_xticklabels([2,6,10,14,18,22,26,30,34,38,42,46,50])
        h.set(xlabel = 'Feet', ylabel = 'Feet')
        
        # read in floorplan - set size and z
        my_image = mpimg.imread('input/house3.png')
        h.imshow(my_image, aspect=h.get_aspect(), extent=h.get_xlim() + h.get_ylim(), zorder=1)
   
       # Redraw the heatmap with data
        self.fig.canvas.draw_idle()
        
        #plt.show()
        #self.canvas = FigureCanvas(fig)
    
    def scan_data_point(self):
        '''scans next data point in list'''
        
        if self.current_gp == self.total_gp:
            return
        
        avg_bits_second = None
        cmd = f'iperf3 -c {self.iperf_ip} -J > iperf_json'
        
        # should do a timeout with this or subprocess
        #self.change_infotxt("Processing iperf")
        
        self.mbit_info_txt.setText("Scanning...    ")
        
        #Quick solution to update text
        QApplication.processEvents()
        
        os.system(cmd)
        
        #self.information_txt.setText("Scan complete")
        
        if not os.path.isfile(f'iperf_json'):
            print('iperf3 output file does not exist');
            self.mbit_info_txt.setText("No iperf JSON")
            return    
        
        with open('iperf_json', 'r') as inF:
            data = json.load(inF)
        
        # grab average bits per second, convert to MBits/s with 2 decimals
        try:
            avg_bits_second = data['end']['sum_received']['bits_per_second']
            avg_mbits_second = round((avg_bits_second / 1000000), 2)
        except KeyError:
            self.information_txt.setText("iperf conn err")
        
        self.current_gp += 1
    
        self.change_grid_infotxt()
        self.change_mbittxt(str(avg_mbits_second))
        self.mbit_insert(avg_mbits_second)
        
        self.redraw_map()
        
    def multi_thread1(self, cmd):
        self.term_out = os.system(cmd)
    
    def multi_thread2(self):
         #while self.term_out == 1:
        m = self.msg.exec_()
        
        
    def change_grid_infotxt(self):
        self.grid_info_txt.setText(f"{self.current_gp}/{self.total_gp} gridpoints")
    
    def change_mbittxt(self, txt_change):
        self.mbit_info_txt.setText(f'{txt_change} Mbit/s  ')
        
    def generate_df_from_file(self):
        '''generates pandas dataframe from csv file'''
        
        floorplan_df = pd.read_csv('input/house.csv')
        floorplan_df = floorplan_df.pivot('row', 'col', 'intensity')
        
        return floorplan_df
    
    def generate_dataframe(self):
        '''generates dataframe from nparray and mbitrate list'''
        
        # Preps array with row,col,mbit for dataframe 
        x = 1
        y = 1
        mbit_count = 0
        for arr in self.a:
            arr[0] = x
            arr[1] = y
            arr[2] = self.mbit_data_list[mbit_count]
            y += 1
            mbit_count += 1
            if y == (self.x_ax + 1):
                x += 1
                y = 1
                
        df = pd.DataFrame(self.a, columns=['row','col','intensity'])
        df = df.pivot(index='row',columns='col')
        
        return df
                
    def mbit_insert(self, mbit):
        '''insert mbits/s value into list'''
        
        self.mbit_data_list[(self.current_gp - 1)] = mbit
        
        #for log purposes
        #print(self.mbit_data_list)
        
    
    def rt_dataframe(self):
        '''generates dataframe from nparray and mbitrate list'''
        '''for realtime. this is for outputting in 2 colors'''
        '''to indicate to user what has been scanned'''
        
        # Preps array with row,col,mbit for dataframe 
        x = 1
        y = 1
        mbit_count = 0
        dummy_val = 0
        for arr in self.a:
            
            # This allows scanned points to be green, unscanned grey
            # while using the Accent cmap for seaborn
            if self.mbit_data_list[mbit_count] > 0:
                dummy_val = 0
            else:
                dummy_val = 1
            
            arr[0] = x
            arr[1] = y
            arr[2] = dummy_val
            y += 1
            mbit_count += 1
            dummy_val = 0
            if y == (self.x_ax + 1):
                x += 1
                y = 1
                
        df = pd.DataFrame(self.a, columns=['row','col','intensity'])
        df = df.pivot(index='row',columns='col')
        
        return df
    
    def redraw_map(self):
        '''redraws map to update scanpoints while using application'''
        
        floorplan_data = self.rt_dataframe()
        
        # clear current contents of heatmap on floorplan tab
        self.fig.clear()
        
        # establish seaborn heatmap to overlay ontop of floorplan
        h = sns.heatmap(floorplan_data, cmap='Accent', cbar=False, alpha=0.7,
                        zorder=2, square=True, annot=False, fmt='g', cbar_kws={'label': 'TCP DL Mbit/s'})
        # flip y axis
        h.invert_yaxis()
        
        # setting ticks for heatmap
        h.set_yticklabels([2,6,10,14,18,22,26,30,34])
        h.set_xticklabels([2,6,10,14,18,22,26,30,34,38,42,46,50])
        h.set(xlabel = 'Feet', ylabel = 'Feet')
        
        # read in floorplan - set size and z
        my_image = mpimg.imread('input/house3.png')
        h.imshow(my_image, aspect=h.get_aspect(), extent=h.get_xlim() + h.get_ylim(), zorder=1)
   
       # Redraw the heatmap with data
        self.fig.canvas.draw_idle()
        
    
    def sns_heatmap(self):
        '''Displays finished seaborn block heatgraph'''
        
        floorplan_data = self.generate_df_from_file()
        
        # clear current contents of heatmap on floorplan tab
        self.fig.clear()
        
        # establish seaborn heatmap to overlay ontop of floorplan
        h = sns.heatmap(floorplan_data, cmap='coolwarm', cbar=True, alpha=0.7,
                        zorder=2, square=True, annot=True, fmt='g', cbar_kws={'label': 'TCP DL Mbit/s'})
        # flip y axis
        h.invert_yaxis()
        
        # setting ticks for heatmap
        h.set_yticklabels([2,6,10,14,18,22,26,30,34])
        h.set_xticklabels([2,6,10,14,18,22,26,30,34,38,42,46,50])
        h.set(xlabel = 'Feet', ylabel = 'Feet')
        
        # read in floorplan - set size and z
        my_image = mpimg.imread('input/house3.png')
        h.imshow(my_image, aspect=h.get_aspect(), extent=h.get_xlim() + h.get_ylim(), zorder=1)
   
       # Redraw the heatmap with data
        self.fig.canvas.draw_idle()
        
        #plt.show()
        #self.canvas = FigureCanvas(fig)
    
    def mpl_heatmap(self):
        '''Displays finished matplotlib interpolated heatmap'''
        
        floorplan_data = self.generate_df_from_file()
        
        extents = [0,2500, 0, 1500]
        # take in floorplan image, set extents, etc
        #fig = plt.figure()
        
        # clear current contents of heatmap on floorplan tab
        self.fig.clear()
        
        # start reloading heatmap data
        img = plt.imread("input/house_withmeasurements.png")
        image = plt.imshow(img, extent=extents)
        
        # regular matplotlib attempt
        heatmap = plt.imshow(floorplan_data, cmap='jet',alpha=.4, interpolation='mitchell', extent=[0,2500,0,1500], origin="lower")
        plt.yticks([])
        plt.xticks([])
        
        # Redraw the heatmap with data
        self.fig.canvas.draw_idle()
        
        #self.canvas = FigureCanvas(self.fig)
        #plt.show()

if __name__ == "__main__":

    y_ax = 9
    x_ax = 13
    iperf_server_ip = '192.168.1.8'
    
    app = QApplication(sys.argv)
    window = Window(y_ax, x_ax, iperf_server_ip)
    window.show()
    sys.exit(app.exec_())





