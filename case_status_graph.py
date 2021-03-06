#!/usr/bin/env python
"""
When plotting daily data, a frequent request is to plot the data
ignoring skips, eg no extra spaces for weekends.  This is particularly
common in financial time series, when you may have data for M-F and
not Sat, Sun and you don't want gaps in the x axis.  The approach is
to simply use the integer index for the xdata and a custom tick
Formatter to get the appropriate date string for a given index.
"""

import numpy
from matplotlib.mlab import csv2rec
from pylab import figure, show
import matplotlib.cbook as cbook
from matplotlib.ticker import Formatter
from matplotlib import pyplot
from datetime import datetime
import sys, os

if len(sys.argv) > 1:
    os.putenv('DISPLAY', ':0.0')

datafile = open('./case_status_graph.dat', 'r').readlines()[-10:]
date_list = [ d.split()[0] for d in datafile ]
issued_list = [ i.split()[1] for i in datafile ]

class MyFormatter(Formatter):
    def __init__(self, dates, fmt='%Y-%m-%d(%a)'):
        self.dates = dates
        self.fmt = fmt

    def __call__(self, x, pos=0):
        'Return the label for time x at position pos'
        odd = int(x*2) & 1
        if odd: return ''
        ind = int(round(x))
        if ind>=len(self.dates) or ind<0: return ''

        return self.dates[ind]

formatter = MyFormatter(date_list)
fig = figure()
ax = fig.add_subplot(111)
ax.xaxis.set_major_formatter(formatter)
ax.set_ylabel('Issued', fontsize=15, fontweight='bold', labelpad=20)
ax.plot(numpy.arange(len(date_list)), issued_list, 'o-')
fig.autofmt_xdate()
if len(sys.argv) > 1 and sys.argv[1] == '-s':
    pyplot.savefig('case_status_graph.pdf')
else:
    show()
