## Updates

#### 04/05/21
Created skeleton code labeled the following:

* networkscan.py - Generating network data into a JSON file then parsing/outputing 
* graph.py - invoking a very basic instance of a heatmap with matplotlib for starters
* wifisurveyproject.py - currently the main

#### 04/06/21
Created an architecture floorplan png overlay file. This is a to-scale mockup of an apartment
with wifi location and plot points on the map for measurment. 

### Whats next
Now that the apartment overlay is created, this allows for the testing/mapping of matplotlib. 
Once some tests are done to experiment with how the code will look/function, then the graphing
section and networking data will be joined together.

Networking data (bitrate) is currently being generated by iperf3 in linux, then output to JSON. 
A function will be created to join the JSON networking data with necessary plot points outlined 
in the map overlay. This data will most likely output as a CSV for matplotlib and heatmap 
generation.

In the end, there will most likely need to be a GUI wrapper implemented for this, but we'll cross
that bridge when we get to it. I have a fleshed out wrapper from another project made with PyQt5
that will probably be useful. 


## it220 Wireless survey - Overview

#### Some noteworthy data we have readily available access to thus far:

* bitrate (TCP and UDP)
* signal quality
* signal level dBm
* channels
* frequency (2.4, 5) 

#### Important tools currently being used

* [iperf3](https://iperf.fr)
* [iwlist](https://www.systutorials.com/docs/linux/man/8-iwlist/)
* [matplotlib](https://matplotlib.org/)
* [RaspberryPi](https://www.raspberrypi.org/products/raspberry-pi-4-model-b/)
* [smartdraw](https://www.smartdraw.com/)

#### Objective
Heatmapping bitrate will be the primary goal, and then possibly graphing other data.


