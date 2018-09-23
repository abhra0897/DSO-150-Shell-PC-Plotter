import sys
import glob
import serial
import time
import matplotlib.pyplot as plt
import numpy as np
from scipy.fftpack import fft

dataPoints = 1024  #default for DSO150 as per 113-15001-120 firmware
baud = 115200  #default baud rate of DSO150 as per 113-15001-120 firmware



def scanSerialPorts():
    """ Lists serial port names

        :raises EnvironmentError:
            On unsupported or unknown platforms
        :returns:
            A list of the serial ports available on the system
    """
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result



def openPort():
    portsLst = scanSerialPorts()    #scan available ports and store in variable
    for i in range(0, len(portsLst)):
        print("(index) {0:d}     (port) {1:s}".format(i, portsLst[i]))
    portNdx = int(input("Enter port index [0 - 5] for DSO150:   "))
    global ser
    ser = serial.Serial()
    ser.baudrate = baud
    ser.port = portsLst[portNdx]
    ser.open()



def closePort():
    ser.close()



def readFromDSO():
    global samplingInterval
    file1 = open("dsolog.txt", "w+") #create and open a file to store incoming data
    print("Press and hold ADJ + V/DIV buttons on DSO150 ")

    for i in range(0, 1043):  #as per 113-15001-120 firmware, 1043 (1044?) lines of data are sent by DSO150
        inputRead = ser.readline().decode()  #need to decode the UTF encoding coming from serial port
        if i > 18:  #dataset starts after 18th line
            #print(inputRead)
            file1.write(inputRead)  #store in a file to plot later
        else:
            print(inputRead);
            if  i == 18: #18th line contains the sampling interval information
                
                if "us" in inputRead:
                    inputRead = inputRead.split(',')[1].split("us")[0] #extracting 100 from "SampleInterval,00100us"
                    
                    samplingInterval = float(inputRead)/1000000.0  #from us to sec.
                elif "ms" in inputRead:
                    inputRead = inputRead.split(',')[1].split("ms")[0] #extracting 100 from "SampleInterval,00100ms"
                    #global samplingInterval
                    samplingInterval = float(inputRead)/1000.0  #from ms to sec.
                elif "ns" in inputRead:
                    inputRead = inputRead.split(',')[1].split("ns")[0] #extracting 100 from "SampleInterval,00100ns"
                    #global samplingInterval
                    samplingInterval = float(inputRead)/1000000000.0  #from ms to sec.
                else:  #if neither us nor ms, then it's s
                    inputRead = inputRead.split(',')[1].split("s")[0] #extracting 100 from "SampleInterval,00100s"
                    #global samplingInterval
                    samplingInterval = float(inputRead) / 1.0 #from sec to sec (meaningless ;) )
    print("....Done....")
    file1.close()



def plotData():
    # Number of sample points
    N = dataPoints             #1024 datapoints are default
    # sample spacing
    T = samplingInterval  #sampling interval is extracted earlier
    x = np.linspace(0.0, N*T, N)
    x1, x2, y = np.loadtxt('dsolog.txt', delimiter=',', unpack=True)
    yf = fft(y)  #freq. domain y ax.
    xf = np.linspace(0.0, 1.0/(2.0*T), N//2)  #freq. domain x ax.

    #plot freq. domain
    plt.subplot(2,1,1)
    plt.plot(xf, 2.0/N * np.abs(yf[0:N//2]), '#ffff4d')  #yellow
    ax = plt.gca()
    ax.set_xlabel('Frequency (Hz)', color = '#80bfff')  #sky blue
    ax.set_ylabel('Amplitude (V)', color = '#80bfff')   #sky blue
    ax.set_facecolor('#383535')  #dark gray
    ax.tick_params(colors='#80bfff')   #sky blue
    plt.grid()

    #plot time domain
    plt.subplot(2,1,2)
    plt.plot(x2,y, '#ff0000')  #red
    ax = plt.gca()  #gca = get current axes
    ax.set_xlabel('Time (S)', color = '#80bfff')  #sky blue
    ax.set_ylabel('Amplitude (V)', color = '#80bfff')  #sky blue
    ax.set_facecolor('#383535')  #dark gray
    ax.tick_params(colors='#80bfff')  #sky blue

    fig = plt.gcf()  #gcf = get current figure
    fig.set_facecolor('black')
    plt.grid()

    plt.show();



while True:
    openPort()
    readFromDSO()
    plotData()
    closePort()
#lol
