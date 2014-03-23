#!/usr/bin/env python

import serial
import random
from collections import deque
from matplotlib import pyplot as plt

class AnalogData:
    def __init__(self, maxLen):
        self.ax = deque()
        self.ay = deque()
        self.x = []
        self.maxLen = maxLen
 
    def addToBuf(self, buf, val):
        while len(buf) >= self.maxLen:
            buf.popleft()
        buf.append(val)
        while len(self.x) < len(buf):
            self.x.append(len(self.x))
 
    # add data
    def add(self, data):
        assert(len(data) == 2)
        self.addToBuf(self.ax, data[0])
        self.addToBuf(self.ay, data[1])

class AnalogPlot:
    def __init__(self, analogData):
        plt.figure( figsize=(10,10) )
        self.axline, = plt.plot(analogData.x, "b+-")
        self.ayline, = plt.plot(analogData.x, "r+-")
        plt.ylabel('temperature')
        plt.xlabel('ticks')
        plt.title('sensors temperature')
        plt.legend( (self.axline, self.ayline), ("internal temperature", "external temperature") )
        plt.ion()
 
    def update(self, analogData):
        if 0 != len(analogData.ax) and 0 != len(analogData.ay) and len(analogData.ax) == len(analogData.ay):
            plt.xlim([analogData.x[0], analogData.x[-1]])
            mx = max(max(analogData.ax) + 5, max(analogData.ay) + 5)
            mn = min(min(analogData.ax) - 5, max(analogData.ay) - 5)
            plt.ylim([mn, mx])
            self.axline.set_xdata(analogData.x)
            self.ayline.set_xdata(analogData.x)
            self.axline.set_ydata(analogData.ax)
            self.ayline.set_ydata(analogData.ay)
            plt.draw()
 
analogData = AnalogData(100)
analogPlot = AnalogPlot(analogData)

ser = serial.Serial('/dev/ttyACM0', 9600)

while True:
    read1 = False
    read2 = False
    temp1 = 0.0
    temp2 = 0.0
    while not read1 or not read2:
        line = ser.readline().strip()
        if 0 != len(line):
            print line
            parts = line.split()
            if 3 == len(parts):
                index = int(parts[0])
                temp = float(parts[2])
                if 1 == index:
                    read1 = True
                    temp1 = temp
                elif 2 == index:
                    read2 = True
                    temp2 = temp
    print temp1, temp2
    analogData.add( (temp1, temp2) )
    analogPlot.update(analogData)

