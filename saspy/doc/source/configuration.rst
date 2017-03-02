
.. Copyright SAS Institute

.. currentmodule:: saspy

*****************
Configuring SASPy
*****************

SASPy can connect to different kinds of SAS sessions. It can connect to SAS on Unix, Mainframe, and Windows.
It can connect to a local SAS session or remote session.
Because of the wide range of connection types, there are a number of different access methods
that are part of SASPy each of which are used to connect to different kinds of SAS sessions.

The current set of access methods include `STDIO`_, and `STDIO over SSH`_, `IOM`_, and `HTTP`_. The HTTP access method isn't available yet, since it is for an interface which hasn't shipped yet.
The STDIO access method is only available for Linux SAS; local or remote via passwordless SSH. The IOM access method supports SAS on any platform.
It allows for using a local Windows connection and is also the way to connect to SAS Grid via SAS Grid Manager. I can connect to any SAS Workspace Server.

Configuring all of these various types of connections is actually quite easy. There is a single confiuration file in the saspy directory of the repo: sascfg.py.
This file contains instructions and examples, but this document will go into more details explaining how to configure each type of connection.

sascfg.py
=========
There are three main parts to this configuration file.

        1) SAS_config_names
        2) SAS_config_options
        3) Configuration Definitions

In reverse order, the Configuration Definitions Python Dictionaries are where you configure each connection to a type of SAS session.
SAS_config_options only has one option so far, which restricts (or allows) the end users ability to override settings in the Configuration Definitions using SASsession().
SAS_config_names is the list of Configuration Definition names, which are available to be used; chosen by an end user at connection time.
Configuration Definitions not listed in SAS_config_names are simply inaccessible. You can define all kinds of connections in the file, but not have them availabe by not havging their names in the list.


STDIO
=====
The original access method for SASPy is STDIO. This works with Unix only,
because PC SAS does not support line mode connections.
This is for a local connection to SAS which is installed on the same Unix server.
There are only two keys for this Configuration Definition Dictionary:

saspath - Required
    Path to SAS startup script
options -
    SAS options to include in the start up command line - *must* be a Python List

.. code:: ipython3

    default  = {'saspath': '/opt/sasinside/SASHome/SASFoundation/9.4/bin/sas_u8'
                'options' : ["-fullstimer"]
                }

Note: the trigger to use the STDIO is the absense of any trigger for the other access methods: not having ``'ssh'``
or ``'java'`` keys.


STDIO over SSH
==============
The remote version of the original access method for SASPy. This also works with Linux only, and it support passwordless SSH to the Linux machine where SAS is installed.
It is up to you to make sure user accounts have passwordless SSH configured between the two system. Google it, it's not that hard.
As well as the two keys for STDIO, there are two more more required keys to configure:

ssh - Required
    The ssh command to run (Linux execv required a fully qualified path, even it it could be found in the path variable - it won't. Use fully qualified path here)

host - Required
    The host to connect to. recolvable host name or ip address.

Note: having the ``'ssh'`` key is the triger to use the STDIO over SSH access method.

.. code:: ipython3

    ssh      = {'saspath' : '/opt/sasinside/SASHome/SASFoundation/9.4/bin/sas_u8',
                'ssh'     : '/usr/bin/ssh',
                'host'    : 'remote.linux.host',
                'options' : ["-fullstimer"]
               }


IOM
===
The is the newest access method which opens up many connectivity options. This is the way to use
`SAS Grid Manager <https://www.sas.com/en_us/software/foundation/grid-manager.html>`__
to connect to a SAS grid. Using this method, instead of STDIO over SSH,
lets the distribution of connections to the various grid nodes be controlled by SAS Grid Manager,
as well as integrating with all of the monitoring and administration SAS Grid Manager provides.

The IOM access method supports two forms: `Local`_ and `Remote`_

Remote
~~~~~~
For Remote access (any workspace server on any SAS platform), the following keys are available for the
Configuration Definition Dictionary:

java    - Required
    The path to the java executable to use (On Linux, fully qualifed path. On Windows, you may get away with simply ``java``, else put the FQP)
iomhost - Required
    For remote IOM case, Don't specify to use a local Windows Session] the resolvable host name, or ip to the IOM server to connect to
iomport - Required
    For remote IOM case, Don't specify to use a local Windows Session] the port IOM is listening on
classpath - Required
    Classpath to IOM client jars and saspy client jar.
omruser - *not suggested*
    If blank the user will be prompted for at runtime
    Don't specify to use a local Windows Session
omrpw    - **really not suggested** [Required for remote IOM case but PROMTED for at runtime]
    Don't specify to use a local Windows Session
encoding  -
    This is the python encoding value that matches the SAS session encoding of the IOM server you are connecting to
    **What is the default? How would they figure out what their SAS server is running in?**


.. code:: ipython3

    cpL  =  "/opt/sasinside/SASHome/SASDeploymentManager/9.4/products/deploywiz__94400__prt__xx__sp0__1/deploywiz/sas.svc.connection.jar"
    cpL += ":/opt/sasinside/SASHome/SASDeploymentManager/9.4/products/deploywiz__94400__prt__xx__sp0__1/deploywiz/log4j.jar"
    cpL += ":/opt/sasinside/SASHome/SASDeploymentManager/9.4/products/deploywiz__94400__prt__xx__sp0__1/deploywiz/sas.security.sspi.jar"
    cpL += ":/opt/sasinside/SASHome/SASDeploymentManager/9.4/products/deploywiz__94400__prt__xx__sp0__1/deploywiz/sas.core.jar"
    cpL += ":/opt/github/saspy/java/saspyiom.jar"

    iomlinux = {'java'      : '/usr/bin/java',
                'iomhost'   : 'linux.iom.host',
                'iomport'   : 8591,
                'encoding'  : 'iso-8859-1',
                'classpath' : cpL
                }

    winiomlinux = {'java'      : 'java',
                   'iomhost'   : 'linux.iom.host',
                   'iomport'   : 8591,
                   'encoding'  : 'iso-8859-1',
                   'classpath' : cpW
                  }


Local
~~~~~
For Local SAS running on the same Windows machine, you only need the following (Don't specify any of the others). The absence of ``iomhost`` triggers Local Windows mode.

java      - Required
    the path to the java executable to use (On Unix, fully qualified path. On Windows, you may get away with simply ``java``, else put the FQP)
encoding  -
    This is the python encoding value that matches the SAS session encoding of the IOM server you are connecting to
classpath - Required
    Classpath to IOM client jars and saspy client jar.

.. code:: ipython3


    winlocal = {'java'      : 'java',
                'encoding'  : 'cp1252',
                'classpath' : cpW
                }


**Note:** having the ``'java'`` key is the triger to use the IOM access method.
**Note:** When using the IOM access method (``'java'`` key specified), the absence of the ``'iomhost'`` key is the trigger to use a
Local Windows Session instead of remote IOM.

.. code:: ipython3

    cpW  =  "C:\Program Files\SASHome\SASDeploymentManager\9.4\products\deploywiz__94472__prt__xx__sp0__1\deploywiz\sas.svc.connection.jar"
    cpW += ";C:\Program Files\SASHome\SASDeploymentManager\9.4\products\deploywiz__94472__prt__xx__sp0__1\deploywiz\log4j.jar"
    cpW += ";C:\Program Files\SASHome\SASDeploymentManager\9.4\products\deploywiz__94472__prt__xx__sp0__1\deploywiz\sas.security.sspi.jar"
    cpW += ";C:\Program Files\SASHome\SASDeploymentManager\9.4\products\deploywiz__94472__prt__xx__sp0__1\deploywiz\sas.core.jar"
    cpW += ";C:\ProgramData\Anaconda3\Lib\site-packages\saspy\java\saspyiom.jar"

    winiomlinux = {'java'      : 'java',
                   'iomhost'   : 'linux.iom.host',
                   'iomport'   : 8591,
                   'encoding'  : 'iso-8859-1',
                   'classpath' : cpW
                  }


The ``'classpath'`` key requires a little extra explanation. There are four (4) jars that are required for the Java IOM Client.
These are provided in your existing SAS Install.
There is one jar provided in this repo: saspyiom.jar. These five jurs must be provided (fully qualified paths) in a classpath variable. 
This is done in a very simple way in the sascfg.py file, like so.

::

    cp  =  "C:\Program Files\SASHome\SASDeploymentManager\9.4\products\deploywiz__94472__prt__xx__sp0__1\deploywiz\sas.svc.connection.jar"
    cp += ";C:\Program Files\SASHome\SASDeploymentManager\9.4\products\deploywiz__94472__prt__xx__sp0__1\deploywiz\log4j.jar"
    cp += ";C:\Program Files\SASHome\SASDeploymentManager\9.4\products\deploywiz__94472__prt__xx__sp0__1\deploywiz\sas.security.sspi.jar"
    cp += ";C:\Program Files\SASHome\SASDeploymentManager\9.4\products\deploywiz__94472__prt__xx__sp0__1\deploywiz\sas.core.jar"
    cp += ";C:\ProgramData\Anaconda3\Lib\site-packages\saspy\java\saspyiom.jar"
 
And then simply use:

::

    'classpath' : cp,

in the Configuration Definition. Easy :)


HTTP
====
The access method is for the next generation of remote connectivity in SAS(R) Viya. The Compute Service, which is what this connects to is not out yet.
But when it ships, this access method will be used to connect to it. 
It will work from either Unix or Windows, client side, and will connect to any SAS platform supported by the Compute Service.

The Configuration Definition Keys will be documented when this is finalized.  


