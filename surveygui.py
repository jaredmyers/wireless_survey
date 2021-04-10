# WiFi scan tool GUI
# 
#

import sys
import requests
import wget
import os

import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import json

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas 
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar 
 
from PyQt5 import QtGui
from PyQt5.QtWidgets import *

from PyQt5 import QtCore
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt

import random


class Window(QWidget):

    def __init__(self, grid_point_num, iperf_ip):
        '''constructor for scantool'''
        super().__init__()
        self.setWindowTitle("WiFi Survey Tool")
        self.resize(800, 500)

        #--- Create a top-level layout-
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        # Grid point number for current floorplan
        # IP for iperf
        self.total_gp = grid_point_num
        self.gp = 0
        self.iperf_ip = iperf_ip
        
        # Floorplan Display ---------------------
        self.canvas = None
        
        #----------------------- Labels
        # Floorplan Tab---------------------
        self.grid_info_txt = QLabel()
        self.mbit_info_txt = QLabel()
        self.plot_button = QPushButton('Scan Data Point')
        self.finish_button = QPushButton('Finish')
        self.grid_data_list = []
        
        
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
        
        self.grid_info_txt.setText(f"{self.gp}/{self.total_gp} gridpoints")
        self.plot_start_graph()
        
        layoutV.addWidget(self.canvas)
        layoutH.addLayout(layoutH2)
        layoutH2.addWidget(self.plot_button, alignment=QtCore.Qt.AlignLeft)
        layoutH2.addWidget(self.finish_button)
        layoutH.addWidget(self.mbit_info_txt)
        layoutH.addWidget(self.grid_info_txt)
        layoutV.addLayout(layoutH)
        
        floorplan_tab.setLayout(layoutV)

        self.plot_button.clicked.connect(self.scan_data_point)
        
        return floorplan_tab


    def selection_tabUI(self):
        '''Create the Selection page UI.'''
        
        selection_tab = QWidget()
        layoutV = QVBoxLayout()

        selection_tab.setLayout(layoutV)

        return selection_tab

                               
    def plot_start_graph(self):
        '''Adds starter flooplan to floorplan tab'''
       
        extents = [0,2500, 0, 1500]
        # take in floorplan image, set extents, etc
        fig = plt.figure()
        img = plt.imread("house.png")
        image = plt.imshow(img, extent=extents)
        
        self.canvas = FigureCanvas(fig)
        
    def plot_finished_graph(self):
        pass
    
    def scan_data_point(self):
        '''scans next data point in list'''
        
        avg_bits_second = None
        cmd = f'iperf3 -c {self.iperf_ip} -J > iperf_json'
        
        # should do a timeout with this or subprocess
        #self.change_infotxt("Processing iperf")
        os.system(cmd)
        #self.information_txt.setText("Scan complete")
        
        if not os.path.isfile(f'iperf_json'):
            print('iperf3 output file does not exist');
            self.information_txt.setText("No iperf JSON")
            return    
        
        with open('iperf_json', 'r') as inF:
            data = json.load(inF)
        
        # grab average bits per second, convert to MBits/s with 2 decimals
        try:
            avg_bits_second = data['end']['sum_received']['bits_per_second']
            avg_Mbits_second = round((avg_bits_second / 1000000), 2)
        except KeyError:
            self.information_txt.setText("iperf conn err")
            
        #self.information_txt.setText("JSON read")
        #self.information_txt.setText(str(avg_Mbits_second))
            
        self.gp += 1
        
        self.change_grid_infotxt()
        self.change_mbittxt(str(avg_Mbits_second))
        self.grid_data_list.append(avg_Mbits_second)
        
        #self.infor_txt.setText(str(self.grid_point_num))
        
    def change_grid_infotxt(self):
        self.grid_info_txt.setText(f"{self.gp}/{self.total_gp} gridpoints")
    
    def change_mbittxt(self, txt_change):
        self.mbit_info_txt.setText(f'{txt_change} Mbit/s  ')

if __name__ == "__main__":

    floorplan_gridpoint_num = 117
    iperf_server_ip = '10.0.0.74'
    
    app = QApplication(sys.argv)
    window = Window(floorplan_gridpoint_num, iperf_server_ip)
    window.show()
    sys.exit(app.exec_())





