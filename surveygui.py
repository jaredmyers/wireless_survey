# WiFi scan tool GUI
# 
#

import sys
import requests
import wget
import os

import pandas as pd
import matplotlib
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas 
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar 
import matplotlib.pyplot as plt 

from PyQt5 import QtGui
from PyQt5.QtWidgets import *

from PyQt5 import QtCore
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt

import random


class Window(QWidget):

    def __init__(self):
        '''constructor for scantool'''
        super().__init__()
        self.setWindowTitle("WiFi Survey Tool")
        self.resize(800, 500)

        #--- Create a top-level layout-
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        
        # Floorplan Display ---------------------
        self.canvas = None
        
        #----------------------- Labels
        # Floorplan Tab---------------------
        self.information_txt = QLabel()
        self.plot_button = QPushButton('Scan Data Point')
        
        
        # Selection Tab-------------------
        self.searchTextField = QLineEdit()
        self.ph1 = QLabel()

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
        
        # to display button and text under graph
        #layoutH2 = QHBoxLayout()
        #layoutH2.addWidget(self.plot_button)
        self.information_txt.setText("This is some information")
        
        self.plotGraph()
        layoutV.addWidget(self.canvas)
        layoutH.addWidget(self.plot_button)
        layoutH.addWidget(self.information_txt)
        layoutV.addLayout(layoutH)
        #layoutV.addLayout(layoutH2)
        
        floorplan_tab.setLayout(layoutV)
        
        return floorplan_tab


    def selection_tabUI(self):
        '''Create the Selection page UI.'''
        
        selection_tab = QWidget()
        layoutV = QVBoxLayout()

        selection_tab.setLayout(layoutV)

        return selection_tab

                               
    def plotGraph(self):
        '''Adds graph to floorplan tab'''
       
        extents = [0,2600, 0, 1500]
        # take in floorplan image, set extents, etc
        fig = plt.figure()
        img = plt.imread("house.png")
        image = plt.imshow(img, extent=extents)
        
         # regular matplotlib attempt
        floorplan_data = pd.read_csv('house.csv')
        floorplan_data = floorplan_data.pivot('col', 'row', 'intensity')
        heatmap = plt.imshow(floorplan_data, cmap='jet',alpha=.4, interpolation='Mitchell',
                             extent=[0,2500,0,1500], origin="lower")
        
        self.canvas = FigureCanvas(fig)

if __name__ == "__main__":

    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())





