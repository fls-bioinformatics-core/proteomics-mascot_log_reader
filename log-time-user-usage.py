#!/bin/env python
#
# -*- coding: utf-8 -*-
#
# Copyright (C) University of Manchester 2011 
#               Julian Selley <j.selley@manchester.ac.uk>
################################################################################

__docformat__ = 'restructuredtext en'

"""
Mascot Time/User usage
======================
This software draws various charts describing how a user and/or group usage of
the Mascot server, defined by the supplied log.

    $ PYTHONPATH=~/lib/python2.7/ mascot-time-user-usage.py [[-f] searches.log]

@todo 2012-01-09 12:46 JNS: write more detail

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
import logging
import matplotlib.pyplot as plt
import operator
import optparse
import proteomics.mascot
import time

# parse command line options
cmdparser = optparse.OptionParser()
cmdparser.add_option('-f', '--file', action="store", type="string",
                     dest="log_filename", default="searches.log",
                     help="read log FILE", metavar="FILE")
cmdparser.add_option('-u', '--user', action="store", type="string",
                     dest="user_filename", default="user.xml",
                     help="read user FILE", metavar="FILE")
cmdparser.add_option('-g', '--group', action="store", type="string",
                     dest="group_filename", default="group.xml",
                     help="read group FILE", metavar="FILE")
(options, args) = cmdparser.parse_args()
if len(args) > 0:
    options.log_filename = args[0]

debug1 = logging.getLogger(__name__ + '.1')
debug2 = logging.getLogger(__name__ + '.2')
debug3 = logging.getLogger(__name__ + '.3')

# obtain the log entries from the log file
debug1.debug('Starting reading log file ({0})...'.format(options.log_filename))
log_f = proteomics.mascot.LogInputFileReader(options.log_filename)
logs = log_f.read_file()
debug1.debug('Finished reading log file ({0})...'.format(options.log_filename))

# obtain the users and groups from the user and group XML files
debug1.debug('Starting reading user file ({0})...'.format(options.user_filename))
user_f = proteomics.mascot.UserXMLInputFileReader(options.user_filename)
users = user_f.read_file()
debug1.debug('Finished reading user file ({0})...'.format(options.user_filename))
debug1.debug('Starting reading group file ({0})...'.format(options.group_filename))
group_f = proteomics.mascot.GroupXMLInputFileReader(options.group_filename)
groups = group_f.read_file()
debug1.debug('Finished reading group file ({0})...'.format(options.group_filename))
# setup the groups that a uid belongs to
debug1.debug('Assembling information on the groups that users belong to...')
for group in groups:
    for uid in group.uids:
        try:
            users[[user.id for user in users].index(uid)].gids
        except AttributeError:
            users[[user.id for user in users].index(uid)].gids = []
        except ValueError:
            pass
        try:
            users[[user.id for user in users].index(uid)].gids.append(group.id)
        except ValueError:
            pass

# obtain the start date's of the first and last search
first_date = logs[0].start
last_date  = logs[-1].start

# identify the total time spent searching
total_time = sum([log.duration for log in logs])

# sum timings
debug1.debug('Iterating through the logs...')
user_timings = {}
group_timings = {}
user_counts = {}
group_counts = {}
for log in logs:
    try:
        debug2.debug('Attempting to add user with ID {0}'.format(log.uid))
        _user = users[[user.id for user in users].index(log.uid)]
        try:
            user_timings[_user.username]
        except KeyError:
            user_timings[_user.username] = []
        user_timings[_user.username].append(log.duration)
        debug2.debug('Adding timings for user {0}'.format(_user))
        for gid in _user.gids:
            _group = groups[[group.id for group in groups].index(gid)]
            try:
                group_timings[_group.name]
            except KeyError:
                group_timings[_group.name] = []
                debug3.debug('Creating group timings for {0}'.format(_group.name))
            group_timings[_group.name].append(log.duration)
            debug2.debug('Adding timings for group {0}'.format(_group))
    except ValueError:
        logging.warning("Unable to ID user for uid ({0})".format(log.uid))
        pass

debug1.debug('Suming the timings for each user and group')
for username in user_timings.keys():
    _sum = sum(user_timings[username])
    _count = len(user_timings[username])
    user_timings[username] = None
    user_timings[username] = _sum
    debug3.debug('Suming value for user {0}: duration {1}'.format(username, user_timings[username]))
    user_counts[username] = _count
for groupname in group_timings.keys():
    _sum = sum(group_timings[groupname])
    _count = len(group_timings[groupname])
    group_timings[groupname] = None
    group_timings[groupname] = _sum
    debug3.debug('Suming value for group {0}: duration {1}'.format(groupname, group_timings[groupname]))
    group_counts[groupname] = _count

# delete the generic GeneralPermissions group as every user belongs to it
# and delete the Administrators group
del(group_timings['GeneralPermissions'])
del(group_counts['GeneralPermissions'])
del(group_timings['Administrators'])
del(group_counts['Administrators'])
# generate sorted data
group_timings_sorted = sorted(group_timings.items(), key=operator.itemgetter(1))
group_counts_sorted = sorted(group_counts.items(), key=operator.itemgetter(1))

# create a plot for the first pie chart (group timings)
debug1.debug('Starting to draw pie charts...')
#fig = plt.figure()
plt.suptitle('Mascot searches by group (' +
             time.strftime("%d/%b/%Y", first_date) +
             ' - ' +
             time.strftime("%d/%b/%Y", last_date) + ')', size='xx-large')
#a1 = fig.add_subplot(121)
plt.pie([gts[1] for gts in group_timings_sorted], labels=[gts[0] for gts in group_timings_sorted], autopct='%1.f%%')
plt.title('Search times (# searches: {0}; total time: {1} min; # groups: {2})'
          .format(len(logs), total_time / 60, len(group_timings_sorted)))
debug1.debug('Finished drawing pie charts...')
# show the pie charts
plt.show()
# create a plot for the second pie chart (group # searches)
#plt.suptitle('Mascot searches by group (' +
#             time.strftime("%d/%b/%Y", first_date) +
#             ' - ' +
#             time.strftime("%d/%b/%Y", last_date) + ')', size='xx-large')
##a2 = fig.add_subplot(122)
#plt.pie([gcs[1] for gcs in group_counts_sorted], labels=[gcs[0] for gcs in group_counts_sorted], autopct='%1.f%%')
#plt.title('Number of searches')
#debug1.debug('Finished drawing pie charts...')
## show the pie charts
#plt.show()
