# Wireless Survey Heatmap

The goal of this application is to give a visual representation to a users home WiFi signal. The primary measurement is the bitrate of TCP packets from the wireless router to the measurement device.

![interpolation map](output/interpolation_map.png)
![block map](output/block_map.png)

## Requirements 

#### Linux tools:

* [iperf3][1] - Takes active bitrate measurements on networks.

#### Python libraries:

* [numpy][2] - used to setup/store the multi-dimensional data to be graphed 
* [pandas][3] - used to convert numpy data into dataframes for plot reading
* [matplotlib][4] - backbone for creating the graphs and visuals
* [seaborn][5] - built ontop of matplotlib for extensibility/features 
* [PyQt5][6] - Graphical UI wrapper for demonstration purposes

Extra:

* [smartdraw][7] - used to mockup floorplans
* [RaspberryPi][8] - single board computer, good for portability 

---

[1]: <https://iperf.fr>
[2]: <https://numpy.org/doc/stable/user/whatisnumpy.html>
[3]: <https://en.wikipedia.org/wiki/Pandas_%28software%29>
[4]: <https://matplotlib.org/>
[5]: <https://seaborn.pydata.org/>
[6]: <https://www.tutorialspoint.com/pyqt5/pyqt5_quick_guide.htm>
[7]: <https://www.smartdraw.com/>
[8]: <https://www.raspberrypi.org/products/raspberry-pi-4-model-b/>
