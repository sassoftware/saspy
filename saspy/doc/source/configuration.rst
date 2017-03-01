
.. Copyright SAS Institute

.. currentmodule:: saspy

*****************
Configuring SASPy
*****************

SASPy can connect to different kinds of SAS Sessions. It can connect to SAS on Linux and Windows. It can connect to a local SAS Session or remote.
There are a number of different access methods that are part of SASPy which are used to connect to different kinds of SAS Sessions. 

The current set of access methods include STDIO, and STDIO over SSH, IOM and HTTP. The HTTP access method isn't availble yet, since it is for an interface which hasn't shipped yet.
The STDIO access method is only available for Linux SAS; local or remote via passwordless SSH. The IOM access method supports SAS on any platform.
It allows for using a local Windows connection and is also the way to connect to SAS Grid via SAS Grid Manager. I can connect to any SAS Workspace Server.

Configuring all of these various types of connections is actually quite easy. There is a single confiuration file in the saspy directory of the repo: sascfg.py.
This file contains instructions and examples, but this document will go into more details explaining how to configure each type of connection.

sascfg.py
=============
There are three main parts to this configuration file.

        1) SAS_config_names
        2) SAS_config_options
        3) Configuration Definitions

In reverse order, the Configuration Definitions Python Dictionaries are where you configure each connection to a type of SAS session.
SAS_config_options only has one option so far, which restricts (or allows) the end users ability to override settings in the Configuration Definitions using SASsession().
SAS_config_names is the list of Configuration Definition names, which are available to be used; chosen by an end user at connection time.
Configuration Definitions not listed in SAS_config_names are simply inaccessible. You can define all kinds of connections in the file, but not have them availabe by not havging their names in the list.


STDIO
==============
The original access method for SASPy is STDIO. This works with Linux only, as PC SAS does not support a line mode type of connection. 
This is for a local connection to SAS which is installed on the same Linux machine. There are only two keys for this Configuration Definition Dictionary:

 'saspath' - [REQUIRED] path to SAS startup script i.e.: /opt/sasinside/SASHome/SASFoundation/9.4/bin/sas_u8
 'options' - SAS options to include in the start up command line - Python List


Note: the triger to use the STDIO is the absense of any trigger for the other access methods: not having 'ssh' or 'java' keys.


STDIO over SSH
===============
The remote version of the original access method for SASPy. This also works with Linux only, and it support passwordless SSH to the Linux machine where SAS is installed.
It is up to you to make sure user accounts have passwordless SSH configured between the two system. Google it, it's not that hard.
As well as the two keys for STDIO, there are two more more required keys to configure:

 'ssh'     - [REQUIRED] the ssh command to run (Linux execv required a fully qualified path, even it it could be found in the path variable - it won't. Use fully qualified path here) 
 'host'    - [REQUIRED] the host to connect to. recolvable host name or ip address.

Note: having the 'ssh' key is the triger to use the STDIO over SSH access method.


IOM
==============
The is the latest access method which opens up a lot of connectivity. This is the way to use SAS Grid MAnager to connect to a SAS Grid. Using this method, in stead of STDIO over SSH,
lets the distribution of connections to the various Grid nodes be controlled by Grid Manager, as well as integrating with all of the expected monitoring and control provided by that system.

There are two methods tha the IOM access method supports: Local and Remote.

For Remote access (any workspace server on any platform), the following keys are avaliable for the Configuration Definition Dictionary:

 'java'      - [REQUIRED] the path to the java executable to use (On Linux, fully qualifed path. On Windows, you may get away with simply 'java', else put the FQP)
 'iomhost'   - [REQUIRED for remote IOM case, Don't specify to use a local Windows Session] the resolvable host name, or ip to the IOM server to connect to
 'iomport'   - [REQUIRED for remote IOM case, Don't specify to use a local Windows Session] the port IOM is listening on
 'omruser'   - not suggested        [REQUIRED for remote IOM case but PROMTED for at runtime] Don't specify to use a local Windows Session
 'omrpw'     - really not suggested [REQUIRED for remote IOM case but PROMTED for at runtime] Don't specify to use a local Windows Session
 'encoding'  - This is the python encoding value that matches the SAS session encoding of the IOM server you are connecting to
 'classpath' - [REQUIRED] classpath to IOM client jars and saspy client jar.

For Local SAS running on the same Windows machine, you only need the following (Don't specify any of the others). The absense of 'iomhost' triggers Local Windows mode.

 'java'      - [REQUIRED] the path to the java executable to use (On Linux, fully qualifed path. On Windows, you may get away with simply 'java', else put the FQP)
 'encoding'  - This is the python encoding value that matches the SAS session encoding of the IOM server you are connecting to
 'classpath' - [REQUIRED' classpath to IOM client jars and saspy client jar.


Note: having the 'java' key is the triger to use the IOM access method.
Note: When using the IOM access method ('java' key specified), not having the 'iomhost' key is the triger to use a Local Windows Session instead of remote IOM.

The 'classpath' key requires a little extra explaination. There are 4 jars that make up the necessary Java IOM Client. These are provided in your existing SAS Install.
There is one jar provided in this repo: saspyiom.jar. These five jurs must be provided (fully qualified paths) in a classpath variable. 
This is done in a very simple way in the sascfg.py file, like so.

cp  =  "C:\Program Files\SASHome\SASDeploymentManager\9.4\products\deploywiz__94472__prt__xx__sp0__1\deploywiz\sas.svc.connection.jar"
cp += ";C:\Program Files\SASHome\SASDeploymentManager\9.4\products\deploywiz__94472__prt__xx__sp0__1\deploywiz\log4j.jar"
cp += ";C:\Program Files\SASHome\SASDeploymentManager\9.4\products\deploywiz__94472__prt__xx__sp0__1\deploywiz\sas.security.sspi.jar"
cp += ";C:\Program Files\SASHome\SASDeploymentManager\9.4\products\deploywiz__94472__prt__xx__sp0__1\deploywiz\sas.core.jar"
cp += ";C:\ProgramData\Anaconda3\Lib\site-packages\saspy\java\saspyiom.jar"
 
And then simply use:

  'classpath' : cp,

in the Configuration Definition. Easy :)


HTTP
==============
The access method is for the next generation of remote connectivity in Viya. The Compute Service, which is what this connects to is not out yet. 
But when it ships, this access method will be used to connect to it. 
It will work from either Linux or Windows, client side, and will connect to any SAS platform support by the Compute Service.

The Configuration Definition Keys will be documented when this is finalized.  


