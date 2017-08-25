# A Python interface to MVA SAS

This module allows a python process to connect to SAS 9.4 and run SAS code,
generated by the supplied object and methods or explicitly user written, and returns
results as text, HTML5 documents (via SAS ODS), or as Pandas Data Frames. It supports running
analytics and returning the resulting graphics and result data. It can convert between SAS Data
Sets and Pandas Data Frames. It has multiple access methods which allow it to connect to
local or remote Linux SAS, IOM SAS on Windows or Linux (Including Grid Manager),
and local PC SAS. It can run w/in Jupyter Notebooks, in line mode python or in python batch
scripts. It is expected that the user community can and will contribute enhancements. 

## Requirements

This module requires Python3.x or above. It also requires SAS 9.4 or above. 

# Documentation

All of the doc, including install and configuration information can be found at
[sassoftware.github.io/saspy](https://sassoftware.github.io/saspy/).

# Installation

Thsi module can be installed via pip. This will pull down the latest PyPI package and install it.

    pip install saspy

However, if that's too easy, you can also download a specific release from
[SASpy project releases page](https://github.com/sassoftware/saspy/releases), or just clone
the repo and and instll from that. To install a given release, use the following, 
where the X.X.X is the release version you want.

    pip install https://github.com/sassoftware/saspy/releases/download/vX.X.X/saspy.tar.gz

# Resources

[Python](http://www.python.org/)

[Documentation](https://sassoftware.github.io/saspy/).

Copyright SAS Institute
