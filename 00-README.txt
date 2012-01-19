=============
mascot_reader
=============

This software analyses the logs from Matrix Science's Mascot software, and
provides information regarding usage. The software is written in Python
(version 2.7) and is documented in the code. The software depends on the
'proteomics.mascot' library written by the same author, and available from
https://github.com/slyeel/python2.7-proteomics-lib, via 'git' which has been
used for version control.

In order to use the software, you will either require the proteomics library in
the current directory, or run it with the location of the library defined.
That is providing the library has not been placed in a global site-packages
directory.

EXAMPLE:
  PYTHONLIB=~/lib/python2.7/ python ./log-time.py searches.log
_______________________________________________________________________________

./log-time.py
-------------
This program uses the logs to determine when the Mascot server is under load.
It draws a histogram plot displaying each hour and the number of searches
performed within that hour, across the search log time period. This is useful
for administrators to ascertain when the Mascot server is busy, and when it has
quiet periods.

./log-time-user-usage.py
------------------------
This program uses the logs, the user and group files, to ascertain which groups
(or with some modifications to the code, which users) are using the Mascot
server. It draws out a pie chart of the percentage usage of each group
(assuming the users and groups have been defined). This software has been
written with the FLS University of Manchester usage specifically in mind.


