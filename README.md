## Updates

### How far along are we? 

* testing of networking tools (iperf3, iwlist) ***complete***
* getting structured networking data into python ***complete***
* testing matplotlib and graphing capabilities ***complete***
* getting a test heatmap up and running ***complete***
* understanding how to get an overlay image and heatmap to play nicely together ***complete***
* obtain real site data for a proper graph ***complete***
* tweak heatmap and overlay to ensure spacial accuracy ***complete***
* write function to automate the parsing of data directly from networking tools
* create a gui wrapper that allows user to click/touch on a map point and gather bitrate data
* grab a raspberryPi 5-7inch touch screen and a portable battery to make the demo look baller

#### 04/09/21
Real site data measured, graph/overlay working. Heatmap tweaks successful.
See [current output here](house_output.png)

#### 04/08/21 #3
New site map created for current location. Overlays working. Next: will collect site data
for ~100 grid points on site, then organize into a CSV for parsing and visualization. The overlay
will need to be tweaked to ensure its a 1:1 mapping. After that's functional, then the process will
be automated.  

#### 04/08/21 #2
Heatmap + floorplan test overlay functional. Next is gather real data for the space and see
how it looks. 

#### 04/08/21 #1
Current heatmapping from a local CSV appears functional. Now on to figuring out 
the image overlay situation and how to accurately associate the two. 

#### 04/06/21
Created a floorplan png overlay file for matplotlib. This is a scaled mockup of an apartment
with wifi location and plot points on the map for measurement.

#### 04/05/21
Created skeleton code labeled the following:

* networkscan.py - Generating network data into a JSON file then parsing/outputing 
* graph.py - invoking a very basic instance of a heatmap with matplotlib for starters
* wifisurveyproject.py - currently the main


## it220 Wireless survey - Overview

#### Some noteworthy data we have readily available access to thus far:

* bitrate (TCP and UDP)
* signal quality
* signal level dBm
* channels
* frequency (2.4, 5) 

#### Important tools currently being used

* [iperf3](https://iperf.fr) - used for network measurements 
* [iwlist](https://www.systutorials.com/docs/linux/man/8-iwlist/) - used for interacting with wireless network interface
* [matplotlib](https://matplotlib.org/) - used for graphing/visualization
* [RaspberryPi](https://www.raspberrypi.org/products/raspberry-pi-4-model-b/)
* [smartdraw](https://www.smartdraw.com/) - used for drawing floorplans

#### Objective
Heatmapping bitrate will be the primary goal, and then possibly graphing other data.


