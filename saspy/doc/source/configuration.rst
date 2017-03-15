
.. Copyright SAS Institute

.. currentmodule:: saspy

*****************
Configuring SASPy
*****************

SASPy can connect to different kinds of SAS sessions. It can connect to SAS on Unix, Mainframe, and Windows.
It can connect to a local SAS session or remote session.
Because of the wide range of connection types, there are a number of different access methods
that are part of SASPy each of which are used to connect to different kinds of SAS sessions.

The current set of access methods include `STDIO`_, and `STDIO over SSH`_, `IOM`_, and `HTTP`_. 
The HTTP access method isn't available yet, since it is for an interface which hasn't shipped yet.
The STDIO access method is only available for Linux SAS; local or remote via passwordless SSH. 
The IOM access method supports SAS on any platform.
It allows for using a local Windows connection and is also the way to connect to SAS Grid via SAS Grid Manager.
It can connect to any SAS Workspace Server.

Configuring all of these various types of connections is actually quite easy. There is a single confiuration file in the saspy directory of the repo: sascfg.py.
This file contains instructions and examples, but this document will go into more details explaining how to configure each type of connection.

sascfg.py
=========
There are three main parts to this configuration file.

        1) SAS_config_names
        2) SAS_config_options
        3) Configuration Definitions

In reverse order, the Configuration Definitions are Python Dictionaries where you configure each connection to a type of SAS session.
SAS_config_options only has one option so far, which restricts (or allows) the end users ability to override settings in the Configuration Definitions using SASsession().
SAS_config_names is the list of Configuration Definition names which are available to be used; chosen by an end user at connection time.
Configuration Definitions not listed in SAS_config_names are simply inaccessible. You can define all kinds of Configuration Definitions in the file,
but not have them availabe by simply not havging their names in the list.


STDIO
=====
The original access method for SASPy is STDIO. This works with Unix only,
because PC SAS does not support line mode style connections (via stdin, stdout, stderr).
This is for a local connection to SAS which is installed on the same Unix server.
There are only three keys for this Configuration Definition Dictionary:

saspath - Required
    Path to SAS startup script
options -
    SAS options to include in the start up command line - *must* be a Python List
encoding  -
    This is the python encoding value that matches the SAS session encoding of the SAS Session you are connecting to
    The python encoding values can be found here: `encodings-and-unicode <https://docs.python.org/3.5/library/codecs.html#encodings-and-unicode>`_
    The three most common SAS encodings, UTF8, LATIN1 and WLATIN1 which are the defaults for running SAS in Unicode, on Unix, and on Windows, respectivly,
    map to these python encoding values: utf8, latin1 and windows-1252, respectivly. 


.. code:: ipython3

    default  = {'saspath': '/opt/sasinside/SASHome/SASFoundation/9.4/bin/sas_u8'
                'options' : ["-fullstimer"]
                }

Note: the trigger to use the STDIO is the absense of any trigger for the other access methods: not having ``'ssh'``
or ``'java'`` keys in the Configuration Definition.


STDIO over SSH
==============
The remote version of the original access method for SASPy. This also works with Unix only, and it supports passwordless SSH to the Unix machine where SAS is installed.
It is up to you to make sure user accounts have passwordless SSH configured between the two system. Google it, it's not that hard.
As well as the three keys for STDIO, there are two more more required keys to configure:

ssh - Required
    The ssh command to run (Linux execv required a fully qualified path, even it it could be found in the path variable - it won't. Use fully qualified path here)

host - Required
    The host to connect to. resolvable host name or ip address.

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
as well as providing integration with all of the monitoring and administration SAS Grid Manager provides.

The IOM access method also allows saspy to connect to Windows SAS. This can be either a local Windows SAS installation or a remote IOM server running on Windows.

The IOM access method requires the use of the SAS Java IOM Client, and a classpath to access the SAS Java IOM Client jars and the saspy jar.
The ``'classpath'`` key requires a little extra explanation before we get to the Configuration Definition. There are four (4) jars that are required for the Java IOM Client.
These are provided in your existing SAS Install.
There is one jar provided in this repo: saspyiom.jar. These five jars must be provided (fully qualified paths) in a classpath variable.
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
Also worth noting: these five jars are compatible/interchangable with both Windows and Unix client systems.  



The IOM access method supports two forms: `Local`_ and `Remote`_

Remote
~~~~~~
For Remote access (any workspace server on any SAS platform) from either a Unix or Windows client, the following keys are available for the
Configuration Definition Dictionary:

java    - Required
    The path to the java executable to use (On Linux, fully qualifed path. On Windows, you may get away with simply ``java``, else put the FQP)
iomhost - Required
    the resolvable host name, or ip to the IOM server to connect to
iomport - Required
    the port that IOM is listening on for workspace connections
classpath - Required
    Classpath to IOM client jars and saspy client jar.
omruser - *not suggested*  [Required but PROMTED for at runtime]
    If blank the user will be prompted for at runtime
omrpw    - **really not suggested** [Required but PROMTED for at runtime]
    If blank (which it ought to be) the password will be prompted for at runtime
encoding  -
    This is the python encoding value that matches the SAS session encoding of the IOM server you are connecting to
    The python encoding values can be found here: `encodings-and-unicode <https://docs.python.org/3.5/library/codecs.html#encodings-and-unicode>`_
    The three most common SAS encodings, UTF8, LATIN1 and WLATIN1 which are the defaults for running SAS in Unicode, on Unix, and on Windows, respectivly,
    map to these python encoding values: utf8, latin1 and windows-1252, respectivly. 

.. code:: ipython3

    # Unix client class path
    cpL  =  "/opt/sasinside/SASHome/SASDeploymentManager/9.4/products/deploywiz__94400__prt__xx__sp0__1/deploywiz/sas.svc.connection.jar"
    cpL += ":/opt/sasinside/SASHome/SASDeploymentManager/9.4/products/deploywiz__94400__prt__xx__sp0__1/deploywiz/log4j.jar"
    cpL += ":/opt/sasinside/SASHome/SASDeploymentManager/9.4/products/deploywiz__94400__prt__xx__sp0__1/deploywiz/sas.security.sspi.jar"
    cpL += ":/opt/sasinside/SASHome/SASDeploymentManager/9.4/products/deploywiz__94400__prt__xx__sp0__1/deploywiz/sas.core.jar"
    cpL += ":/usr/lib/python3.5/site-packages/saspy/java/saspyiom.jar"

    # Windows client class path
    cpW  =  "C:\Program Files\SASHome\SASDeploymentManager\9.4\products\deploywiz__94472__prt__xx__sp0__1\deploywiz\sas.svc.connection.jar"
    cpW += ";C:\Program Files\SASHome\SASDeploymentManager\9.4\products\deploywiz__94472__prt__xx__sp0__1\deploywiz\log4j.jar"
    cpW += ";C:\Program Files\SASHome\SASDeploymentManager\9.4\products\deploywiz__94472__prt__xx__sp0__1\deploywiz\sas.security.sspi.jar"
    cpW += ";C:\Program Files\SASHome\SASDeploymentManager\9.4\products\deploywiz__94472__prt__xx__sp0__1\deploywiz\sas.core.jar"
    cpW += ";C:\ProgramData\Anaconda3\Lib\site-packages\saspy\java\saspyiom.jar"

    # Unix client and Unix IOM server
    iomlinux = {'java'      : '/usr/bin/java',
                'iomhost'   : 'linux.iom.host',
                'iomport'   : 8591,
                'encoding'  : 'latin1',
                'classpath' : cpL
               }

    # Unix client and Windows IOM server
    iomwin   = {'java'      : '/usr/bin/java',
                'iomhost'   : 'windows.iom.host',
                'iomport'   : 8591,
                'encoding'  : 'windows-1252',
                'classpath' : cpL
               }

    # Windows client and Unix IOM server
    winiomwin   = {'java'      : 'java',
                   'iomhost'   : 'linux.iom.host',
                   'iomport'   : 8591,
                   'encoding'  : 'latin1',
                   'classpath' : cpW
                  }

    # Windows client and Windows IOM server
    winiomwin   = {'java'      : 'java',
                   'iomhost'   : 'windows.iom.host',
                   'iomport'   : 8591,
                   'encoding'  : 'windows-1252',
                   'classpath' : cpW
                  }


Local
~~~~~
For Local SAS running on the same Windows machine, you only need the following Configuration Definition keys (Don't specify any of the others).

*There is also one other requirement.*

The **sspiauth.dll** file (also included in your SAS installation) must be in either your system PATH, your java.library.path, or in the home directory of your Java client.
You can search for this file in your SAS deployment, though it is likely in your SASHome\\SASFoundation\\9.4\\core\\sasext.

If adding this to your system PATH environment variable, only list the path to the directory, don't incluse the file itself i.e.: C:\\Program Files\\SASHome\\SASFoundation\\9.4\\core\\sasext. 

java      - Required
    the path to the java executable to use 
classpath - Required
    Classpath to IOM client jars and saspyiom.jar.
encoding  -
    This is the python encoding value that matches the SAS session encoding of the IOM server you are connecting to
    The python encoding values can be found here: `encodings-and-unicode <https://docs.python.org/3.5/library/codecs.html#encodings-and-unicode>`_
    The three most common SAS encodings, UTF8, LATIN1 and WLATIN1 which are the defaults for running SAS in Unicode, on Unix, and on Windows, respectivly,
    map to these python encoding values: utf8, latin1 and windows-1252, respectivly. 

.. code:: ipython3

    # Windows client class path
    cpW  =  "C:\Program Files\SASHome\SASDeploymentManager\9.4\products\deploywiz__94472__prt__xx__sp0__1\deploywiz\sas.svc.connection.jar"
    cpW += ";C:\Program Files\SASHome\SASDeploymentManager\9.4\products\deploywiz__94472__prt__xx__sp0__1\deploywiz\log4j.jar"
    cpW += ";C:\Program Files\SASHome\SASDeploymentManager\9.4\products\deploywiz__94472__prt__xx__sp0__1\deploywiz\sas.security.sspi.jar"
    cpW += ";C:\Program Files\SASHome\SASDeploymentManager\9.4\products\deploywiz__94472__prt__xx__sp0__1\deploywiz\sas.core.jar"
    cpW += ";C:\ProgramData\Anaconda3\Lib\site-packages\saspy\java\saspyiom.jar"


    # Windows client and Local Windows IOM server
    winlocal    = {'java'      : 'java',
                   'encoding'  : 'windows-1252',
                   'classpath' : cpW
                  }




**Note:** having the ``'java'`` key is the triger to use the IOM access method.
**Note:** When using the IOM access method (``'java'`` key specified), the absence of the ``'iomhost'`` key is the trigger to use a
Local Windows Session instead of remote IOM (it is a different connection type).


HTTP
====
This access method is for the next generation of remote connectivity in SAS(R) Viya. The Compute Service, which is what this connects to is not out yet.
But when it ships, this access method will be used to connect to it. 
It will work from either Unix or Windows, client side, and will connect to any SAS platform supported by the Compute Service.

The Configuration Definition Keys will be documented when this is finalized.  


