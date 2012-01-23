# Mascot Reader

This software analyses the logs from Matrix Science's Mascot software,
and provides information regarding usage.

## Quick start

~~~~{.bash}
	$ python ./log-time.py searches.log
	# presents a GUI with a graph of service usage by hour
	$ python ./log-time-user-usage.py searches.log
	# presents a GUI with a pie-chart of group usage
~~~~

## Instalation

To access the latest version of the software, you can access the git
repository on [github.com](http:://github.com/fls-bioinformatics-core/proteomics-mascot_log_reader).

~~~~{.bash}
	$ git clone git://github.com/fls-bioinformatics-core/proteomics-mascot_log_reader
~~~~

The software depends on a custom library, also available from
[github.com](http://github.com/fls-bioinformatics-core/proteomics-python2.7-proteomics-lib). However,
if you used Git to obtain the software, you can use Git to download
the software:

~~~~{.bash}
	$ git submodules update --init
~~~~

## Description

Currently there are two software programmes, processing the logs in a
different manner. The `log-time.py` software processes the logs and
determines the hourly usage of the Matrix Science Mascot software,
over the time period of the search logs provided. The
`log-time-user-usage.py` presents the usage of the server based on the
groups using the service (this therefore requires access to the group
file).

The software was writtenwith the FLS University of Manchester usage
specifically in mind. Should you notice any bugs, or issues with the
software, please contact the author(s).

## Usage

The [Quick Start section](#quick-start) presents the best way of
running the software. The main exceptions to this, are if the
dependant library has been stored elsewhere. In that case, it is
necessary to inform Python where to look for the library (providing
that this is not on the Python library search path).

~~~~{.bash}
	$ PYTHONLIB=~/lib/python2.7/ ./log-time.py searches.log
~~~~

## Author(s) ##

Julian Selley <[j.selley@manchester.ac.uk](mailto:j.selley@manchester.ac.uk)>

## License ##

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but **WITHOUT ANY WARRANTY**; without even the implied warranty of
**MERCHANTABILITY** or **FITNESS FOR A PARTICULAR PURPOSE**.
