#!/bin/env python
#
# -*- coding: utf-8 -*-
#
# Copyright (C) University of Manchester 2011 
#               Julian Selley <j.selley@manchester.ac.uk>
################################################################################

__docformat__ = 'restructuredtext en'

"""
Log Time
********
This program logs the time usage of Mascot from the search logs and spits out a
histogram.

@todo 2011-12-20 11:40 JNS: write more detail

"""

# Metadata
__version__   = '0.01'
__author__    = 'Julian Selley <j.selley@manchester.ac.uk>'
__copyright__ = 'Copyright 2011 University of Manchester, Julian Selley <j.selley@manchester.ac.uk>'
__license__   = '''\
This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
'''

# Imports
import matplotlib.pyplot as plt
import numpy
import optparse
import proteomics.mascot
import time

# parse command line options
cmdparser = optparse.OptionParser()
cmdparser.add_option('-f', '--file', action="store", type="string",
                     dest="filename", default="searches.log",
                     help="read log FILE", metavar="FILE")
(options, args) = cmdparser.parse_args()
if len(args) > 0:
    options.filename = args[0]

# obtain the log entries from the log file
log_f = proteomics.mascot.LogInputFileReader(options.filename)
logs = log_f.read_file()

# obtain the start date's of the first and last search
first_date = logs[0].start
last_date  = logs[-1].start

# get the start hour for every search and append it to a list, ready for putting
# into a histogram
hrs  = []
durs = []
# setup the duration arrays
for i in range(24):
    durs.append([])
for log_entry in logs:
    hrs.append(log_entry.start.tm_hour)
    # append the duration by the hour it occured in
    durs[log_entry.start.tm_hour].append(log_entry.duration)

# calculate the mean and median duration for each hour
mdurs  = []
mddurs = []
for idur in durs:
#    mdurs.append(float(sum(idur)) / len(idur))
    mdurs.append(numpy.mean(idur))
    mddurs.append(numpy.median(idur))

# setup figure
fig = plt.figure()
ax1 = fig.add_subplot(111)
# plot the histogram
ax1.hist(hrs, bins=24)
# plot the mean duration as a red line
ax2 = ax1.twinx()
ml  = ax2.plot(mdurs,'r-')
mdl = ax2.plot(mddurs, 'g-')
# label the figure
plt.xlabel('Time (hours)')
ax1.set_ylabel('# searches')
ax2.set_ylabel('mean of duration (secs)')
ax2.legend([ml, mdl], ["mean duration", "median duration"])
plt.title(''.join(['Mascot search start time distribution across the day (',
                   time.strftime("%d/%b/%Y", first_date), 
                   ' - ', 
                   time.strftime("%d/%b/%Y", last_date), ')']))
# re-define the x-limitations
plt.xlim(0, 23)
# show the histogram
plt.show()
