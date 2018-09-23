## DSO 150 / DSO Shell PC Plotter
"DSO 150 / DSO Shell PC Plotter" lets us connect the JYETech's DSO 150 / DSO Shell oscilloscope with PC using serial port and plot the data automatically. It eliminates the needs for connecting to a serial terminal software, then copying the data manually and saving in a file, and finally plotting them using any plotting software (MATlab, libre office calc, MS Excell to name a few). It does everything on your behalf, and moreover, the software performs FFT to plot in frequency domain also.

### Installation
The code is written in python3. So, the user must have python3 installed on his/her PC. OS doesn't matter. If you already do not have pyhton3 installed, go to https://www.python.org and download. The latest version is 3.7.0 at the time of writing this readme.

However, you may need to install few more dependencies to run the software if not already installed. The dependencies are:

- PySerial  (https://pythonhosted.org/pyserial/pyserial.html#installation)
- matplotlib  (https://matplotlib.org/users/installing.html)
- NumPy  (http://www.numpy.org)
- SciPy  (https://www.scipy.org/install.html)

##### Install using "pip" (All OSs)
Note that you need to have Python and pip already installed on your system. The following command works in any OS (Windows, Linux, Mac).

    python -m pip install --user numpy scipy matplotlib ipython jupyter pandas sympy nose

do not use sudo pip

##### Install system-wide via a Linux package manager
Users on Linux can install packages from repositories provided by the distributions. These installations will be system-wide, and may have older package versions than those available using pip.

    sudo apt-get install python-numpy python-scipy python-matplotlib ipython ipython-notebook python-pandas python-sympy python-nose

##### For Mac
Use pip or your favorite package manager. I really am not concerened about Mac.

### How to use the software
Usage is pretty simple.

- Connect your DSO 150 / DSO Shell with PC using USB to Serial converter.
- Run the python script using "python3 dso150PCplot.py".
- Software displays available serial ports.
- Enter the index number of the serial port that refers to the DSO 150.
- PC will receive data from DSO 150 and plot in frequency domain and in time domain.
- Data will be saved in dsologs.txt file in your current directory.
- Hover your cursor on the graph to see the value at that point. Value is displayed at the bottom right corner.

### How to get serial data from DSO 150 / Shell
Do the following steps.

- Connect TX of DSO to RX of USB-Serial converter
- Connect RX of DSO to TX of USB-Serial converter
- Connect GND of DSO to GND of USB-Serial converter

If your firmware is 113-15001-120, then PRESS AND HOLD ADJ + V/DIV BUTTONS for 2 - 3 seconds. DSO will send 1024 samples to the PC to plot. This is NOT a continuous transfer.
The above method may work with previous firmwares too.

### Compatibility and modification
This software is tested with 113-15001-120 firmware.
With different firmware of DSO, serial output pattern may change. Please study the code which is well-commented to modify it in case your firmware is different.

Hints: Our targets are:
- Line 18 (or 19) of serial data. It contains the sampling period information.
- Last 1024 lines. They contain the original data that we plot.
