
.. Copyright SAS Institute

******************************
Installation and configuration
******************************

=============
Installation
=============

This package installs just like any other Python package.
It is a pure Python package and works with Python 3.x
installations.  To install the latest version using `pip`, you execute the following::

    pip install saspy

or, for a specific release::

    pip install http://github.com/sassoftware/saspy/releases/saspy-X.X.X.tar.gz


To use this module after installation, you need to edit the sascfg.py file to 
configure it to be able to connect and start a SAS session. Follow the 
instructions in the next section.

* If you run into any problems, see :doc:`troubleshooting`.
* If you have questions, open an issue at https://github.com/sassoftware/saspy/issues.



===============
Configuration
===============

This module can connect and start different kinds of SAS sessions. It can connect to SAS 
on Unix, Mainframe, and Windows. It can connect to a local SAS session or remote session.
Because of the wide range of connection types, there are a number of different access methods
which are used to connect to different kinds of SAS sessions.

The current set of connection methods are as follows:

`STDIO`_
  This connection method is available on the Linux platform only. This 
  method enables you to connect to SAS on the same host as your Python process.

`STDIO over SSH`_
  This connection method is also available on the Linux platform only. This
  method can connect to SAS that is installed on a remote host, if you have passwordless
  SSH configured for your Linux user account.


`IOM`_
  The integrated object method (IOM) connection method supports SAS on any platform.
  This method can make a local Windows connection and it is also the way to connect 
  to SAS Grid through SAS Grid Manager. This method can connect to a SAS Workspace
  Server on any supported SAS platform.

Though there are several connection methods available, a single configuration file
is used to enable all the connection methods. The file contains instructions and
examples, but this section goes into more detail to explain how to configure each
type of connection.

Depending upon how you did your installation, the sascfg.py file may be in different 
locations on the file system:

* In a regular pip install, it is under the site-packages directory in the Python 
  installation. 
* If you cloned the repo or downloaded and extraced the repo and then installed, 
  it may use the sascfg.py file from that location and not copy it to site-packages.
 
First, make sure that you update the sascfg.py file that Python uses. If you are 
familiar with pip and Git, then you probably know where to look. If you are not
familiar with those tools, then there is a very simple way to determine the location
that Python is using to get at this module.

After installing, start Python and ``import saspy``. Then, simply submit 
``saspy.SAScfg``. Python will show you where it found the module. Edit that one.

.. code-block:: ipython3

    # this is an example of a repo install on Windows:

    C:\>python
    Python 3.6.0 |Anaconda custom (64-bit)| (default, Dec 23 2016, 11:57:41) [MSC v.1900 64 bit (AMD64)] on win32
    Type "help", "copyright", "credits" or "license" for more information.
    >>> import saspy
    >>> saspy.SAScfg
    <module 'saspy.sascfg' from 'E:\\metis-master\\saspy_pip\\saspy\\sascfg.py'>
    >>>

    # this is an example of a repo install on Linux:

    Linux-1> python3.5
    Python 3.5.1 (default, Jan 19 2016, 21:32:20)
    [GCC 4.4.7 20120313 (Red Hat 4.4.7-16)] on linux
    Type "help", "copyright", "credits" or "license" for more information.
    >>> import saspy
    >>> saspy.SAScfg
    <module 'saspy.sascfg' from '/opt/tom/gitlab/metis/saspy_pip/saspy/sascfg.py'>
    >>>
    
    # this is an example of a PyPi install on Linux into site-packages:

    Linux-1> python3.5
    Python 3.5.1 (default, Jan 19 2016, 21:32:20)
    [GCC 4.4.7 20120313 (Red Hat 4.4.7-16)] on linux
    Type "help", "copyright", "credits" or "license" for more information.
    >>> import saspy
    >>> saspy.SAScfg
    <module 'saspy.sascfg' from '/usr/lib/python3.5/site-packages/saspy/sascfg.py'>
    >>>
    
        
sascfg.py details
=================
There are three main parts to this configuration file.

        1) SAS_config_names
        2) SAS_config_options
        3) Configuration definitions

In reverse order, the configuration definitions are Python dictionaries. Each dictionary 
has the settings for one connection method (STDIO, SSH, IOM, and so on) to a SAS session.

SAS_config_options has one option. The option restricts (or allows) an end users' ability 
to override settings in the configuration definitions using ``SASsession()``.

SAS_config_names is the list of configuration definition names to make available to an
end user at connection time. Any configuration definitions that are not listed in 
SAS_config_names are simply inaccessible by an end user. You can add several configuration
definitions in the file but not make them available by simply excluding the names from 
the list.


STDIO
=====
This is the original access method. This works with Unix only,
because SAS on Windows platforms does not support line-mode style connections
(through stdin, stdout, stderr). This connection method is for a local 
connection to SAS that is installed on the same host as Python.

There are only three keys for this configuration definition dictionary:

saspath - 
    (Required) Path to SAS startup script
options -
    SAS options to include in the start up command line. These **must** be a
    Python list.
encoding -
    This is the Python encoding value that matches the SAS session encoding
    of the SAS session to which you are connecting. The Python encoding 
    values can be found at `encodings-and-unicode <https://docs.python.org/
    3.5/library/codecs.html#encodings-and-unicode>`_.
    The three most common SAS encodings, UTF8, LATIN1, and WLATIN1 are the 
    default encodings for running SAS in Unicode, on Unix, and on Windows,
    respectively. Those map to Python encoding values: utf8, latin1, and
    windows-1252, respectively. 


.. code-block:: ipython3

    default  = {'saspath': '/opt/sasinside/SASHome/SASFoundation/9.4/bin/sas_u8'
                'options' : ["-fullstimer"]
                }

.. note:: The trigger to use the STDIO connection method is the absence of any
          trigger for the other access methods: not having ``'ssh'`` or ``'java'``
          keys in the configuration definition.


STDIO over SSH
==============
This is the remote version of the original connection method. This also works 
with Unix only, and it supports passwordless SSH to the Unix machine where SAS
is installed. It is up to you to make sure that user accounts have passwordless
SSH configured between the two systems. Google it, it's not that difficult.

In addition to the three keys for STDIO, there are two more keys to configure:

ssh - 
    (Required) The ssh command to run (Linux execv requires a fully qualified
    path. Even if the command is found in the PATH variable, it won't be used.
    Enter the fully qualified path.)

host - 
    (Required) The host to connect to. Enter a resolvable host name or IP address.

.. code-block:: ipython3

    ssh      = {'saspath' : '/opt/sasinside/SASHome/SASFoundation/9.4/bin/sas_u8',
                'ssh'     : '/usr/bin/ssh',
                'host'    : 'remote.linux.host',
                'options' : ["-fullstimer"]
               }

.. note:: The ``'ssh'`` key is the trigger to use the STDIO over SSH connection
          method.



IOM
===
The connection method opens many connectivity options. This method enables you to use
`SAS Grid Manager <https://www.sas.com/en_us/software/foundation/grid-manager.html>`__
to connect to a SAS grid. This method, compared to STDIO over SSH, enables SAS Grid
Manager to control the distribution of connections to the various grid nodes
and integrates all the monitoring and administration that SAS Grid Manager provides.

The IOM connection method also enables you to connect to SAS on Windows platforms.
The connection can be to a local SAS installation or a remote IOM server running on 
Windows.

The IOM connection method requires the following:

* The SAS Java IOM Client
* Setting the CLASSPATH to access the SAS Java IOM Client JAR files.
* Setting the CLASSPATH to include the the saspyiom.jar file.
* Setting the CLASSPATH to include client side encryption jars, if you have encryption configured for your IOM

The ``'classpath'`` key for the configuration definition requires a little additional
explanation before we get to further details. There are four (4) JAR files that are 
required for the Java IOM Client. The JAR files are available from your existing SAS
installation.  There is one JAR file that is provided with this package: 
saspyiom.jar. These five JAR files must be provided (fully qualified paths) in a 
CLASSPATH environment variable. This is done in a very simple way in the sascfg.py 
file, like so:

::

    cp  =  "C:\\Program Files\\SASHome\\SASDeploymentManager\\9.4\\products\\deploywiz__94472__prt__xx__sp0__1\\deploywiz\\sas.svc.connection.jar"
    cp += ";C:\\Program Files\\SASHome\\SASDeploymentManager\\9.4\\products\\deploywiz__94472__prt__xx__sp0__1\\deploywiz\\log4j.jar"
    cp += ";C:\\Program Files\\SASHome\\SASDeploymentManager\\9.4\\products\\deploywiz__94472__prt__xx__sp0__1\\deploywiz\\sas.security.sspi.jar"
    cp += ";C:\\Program Files\\SASHome\\SASDeploymentManager\\9.4\\products\\deploywiz__94472__prt__xx__sp0__1\\deploywiz\\sas.core.jar"
    cp += ";C:\\ProgramData\\Anaconda3\\Lib\\site-packages\\saspy\\java\\saspyiom.jar"

    # And, if you've configured IOM to use Encryption, you need these client side jars.
    cp += ";C:\\Program Files\\SASHome\\SASVersionedJarRepository\\eclipse\\plugins\\sas.rutil_904300.0.0.20150204190000_v940m3\\sas.rutil.jar"
    cp += ";C:\\Program Files\\SASHome\\SASVersionedJarRepository\\eclipse\\plugins\\sas.rutil.nls_904300.0.0.20150204190000_v940m3\\sas.rutil.nls.jar"
    cp += ";C:\\Program Files\\SASHome\\SASVersionedJarRepository\\eclipse\\plugins\\sastpj.rutil_6.1.0.0_SAS_20121211183517\\sastpj.rutil.jar"
    

And then simply refer to the ``cp`` variable in the configuration definition:

::

    'classpath' : cp,

Also worth noting: these five JAR files are compatible with both Windows and Unix client systems.  

.. note::
    If you have a \\u or \\U in your classpath string, like: "c:\\User\\sastpw\\...', you will have to use either 
    a double backslash instead, like \\\\u or \\\\U ("c:\\\\User\\sastpw\\...') or mark the string as raw (not 
    unicode) with a r prefix, like r"C:\\User\\sastpw\\..." 
    or else you will get an error like this: SyntaxError: (unicode error) 'unicodeescape' codec can't decode 
    bytes in position 3-4: truncated \UXXXXXXXX escape 



The IOM access method now has support for getting the required user/password from an authinfo file in the user's home directory
instead of prompting for it. On linux, the file is named .authinfo and on windows, it's _authinfo. The format of the line in the authinfo file is
as follows. The first value is the authkey value you specify for `authkey`. Next is the 'user' key followed by the value (the user id)
and then 'password' key followed by its value (the user's password). Note that there are permission rules for this file. On linux the file must
have permissions of 600, only the user can read or write the file. On Windows, the file should be equally locked down to where only the owner
can read and write it.  

::

    authkey user omr_user_id password omr_user_password

So, for a Configuration Definition that specifies the following authkey:

::

    'authkey' : 'IOM_Prod_Grid1',

The authinfo file in the home directory for user Bob, with a password of BobsPW1 would have a line in it as follows:
 
::

    IOM_Prod_Grid1 user Bob password BobsPW1


Remote
~~~~~~
A remote connection is defined as a connection to any workspace server on any SAS platform 
from either a Unix or Windows client. 

The following keys are available for the configuration definition dictionary:

java    - 
    (Required) The path to the Java executable to use. For Linux, use a fully qualifed
    path. On Windows, you might be able to simply enter ``java``. If that is not successful,
    enter the fully qualified path.
iomhost - 
    (Required) The resolvable host name, or IP address to the IOM server.
iomport - 
    (Required) The port that IOM server is listening on for workspace connections.
classpath - 
    (Required) The CLASSPATH to the IOM client JAR files and saspyiom.jar.
authkey -
    The keyword that starts a line in the authinfo file containing user and or password for this connection.
omruser - 
    (**Discouraged**)  The user ID is required but if this field is left blank,
    the user is **prompted** for a user ID at runtime, unless it's found in the authinfo file.
omrpw  - 
    (**Strongly discouraged**) A password is required but if this field is left
    blank, the user is **prompted** for a password at runtime, unless it's found in the authinfo file.
encoding  -
    This is the Python encoding value that matches the SAS session encoding of 
    the IOM server to which you are connecting. The Python encoding values can be 
    found at `encodings-and-unicode <https://docs.python.org/3.5/
    library/codecs.html#encodings-and-unicode>`_.
    The three most common SAS encodings, UTF8, LATIN1, and WLATIN1 are the 
    default encodings for running SAS in Unicode, on Unix, and on Windows,
    respectively. Those map to Python encoding values: utf8, latin1, and 
    windows-1252, respectively. 
appserver -
    If you have more than one AppServer defined on OMR, then you must pass the name of the physical workspace server
    that you want to connect to, i.e.: 'SASApp - Workspace Server'. Without this the Object spawner will only try the
    first one in the list of app servers it supports.

.. code-block:: ipython3

    # Unix client class path
    cpL  =  "/opt/sasinside/SASHome/SASDeploymentManager/9.4/products/deploywiz__94400__prt__xx__sp0__1/deploywiz/sas.svc.connection.jar"
    cpL += ":/opt/sasinside/SASHome/SASDeploymentManager/9.4/products/deploywiz__94400__prt__xx__sp0__1/deploywiz/log4j.jar"
    cpL += ":/opt/sasinside/SASHome/SASDeploymentManager/9.4/products/deploywiz__94400__prt__xx__sp0__1/deploywiz/sas.security.sspi.jar"
    cpL += ":/opt/sasinside/SASHome/SASDeploymentManager/9.4/products/deploywiz__94400__prt__xx__sp0__1/deploywiz/sas.core.jar"
    cpL += ":/usr/lib/python3.5/site-packages/saspy/java/saspyiom.jar"

    # Windows client class path
    cpW  =  "C:\\Program Files\\SASHome\\SASDeploymentManager\\9.4\\products\\deploywiz__94472__prt__xx__sp0__1\\deploywiz\\sas.svc.connection.jar"
    cpW += ";C:\\Program Files\\SASHome\\SASDeploymentManager\\9.4\\products\\deploywiz__94472__prt__xx__sp0__1\\deploywiz\\log4j.jar"
    cpW += ";C:\\Program Files\\SASHome\\SASDeploymentManager\\9.4\\products\\deploywiz__94472__prt__xx__sp0__1\\deploywiz\\sas.security.sspi.jar"
    cpW += ";C:\\Program Files\\SASHome\\SASDeploymentManager\\9.4\\products\\deploywiz__94472__prt__xx__sp0__1\\deploywiz\\sas.core.jar"
    cpW += ";C:\\ProgramData\\Anaconda3\\Lib\\site-packages\\saspy\\java\\saspyiom.jar"

    # Unix client and Unix IOM server
    iomlinux = {'java'      : '/usr/bin/java',
                'iomhost'   : 'linux.iom.host',
                'iomport'   : 8591,
                'encoding'  : 'latin1',
                'classpath' : cpL,
                'appserver' : 'SASApp Prod - Workspace Server'
                }

    # Unix client and Windows IOM server
    iomwin   = {'java'      : '/usr/bin/java',
                'iomhost'   : 'windows.iom.host',
                'iomport'   : 8591,
                'encoding'  : 'windows-1252',
                'classpath' : cpL,
                'appserver' : 'SASApp Test - Workspace Server'
               }

    # Windows client and Unix IOM server
    winiomlinux = {'java'      : 'java',
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
A local connection is defined as a connection to SAS that is running on the same
Windows machine. You only need the following configuration definition keys. (Do not
specify any of the others).

**There is one additional requirement.** The sspiauth.dll file--also included in 
your SAS installation--must be in your system PATH environment variable, your 
java.library.path, or in the home directory of your Java client. You can search 
for this file in your SAS deployment, though it is likely
in SASHome\\SASFoundation\\9.4\\core\\sasext.

If you add the file to the system PATH environment variable, only list the path to 
the directory--do not include the file itself. For example:

::

    C:\Program Files\SASHome\SASFoundation\9.4\core\sasext 

java      - 
    (Required) The path to the Java executable to use. 
classpath - 
    (Required) The CLASSPATH to the IOM client JAR files and saspyiom.jar.
encoding  -
    This is the Python encoding value that matches the SAS session encoding of 
    the IOM server to which you are connecting. The Python encoding values can be 
    found at `encodings-and-unicode <https://docs.python.org/3.5/
    library/codecs.html#encodings-and-unicode>`_.
    The three most common SAS encodings, UTF8, LATIN1, and WLATIN1 are the 
    default encodings for running SAS in Unicode, on Unix, and on Windows,
    respectively. Those map to Python encoding values: utf8, latin1, and 
    windows-1252, respectively. 

.. code-block:: ipython3

    # Windows client class path
    cpW  =  "C:\\Program Files\\SASHome\\SASDeploymentManager\\9.4\\products\\deploywiz__94472__prt__xx__sp0__1\\deploywiz\\sas.svc.connection.jar"
    cpW += ";C:\\Program Files\\SASHome\\SASDeploymentManager\\9.4\\products\\deploywiz__94472__prt__xx__sp0__1\\deploywiz\\log4j.jar"
    cpW += ";C:\\Program Files\\SASHome\\SASDeploymentManager\\9.4\\products\\deploywiz__94472__prt__xx__sp0__1\\deploywiz\\sas.security.sspi.jar"
    cpW += ";C:\\Program Files\\SASHome\\SASDeploymentManager\\9.4\\products\\deploywiz__94472__prt__xx__sp0__1\\deploywiz\\sas.core.jar"
    cpW += ";C:\\ProgramData\\Anaconda3\\Lib\\site-packages\\saspy\\java\\saspyiom.jar"


    # Windows client and Local Windows IOM server
    winlocal    = {'java'      : 'java',
                   'encoding'  : 'windows-1252',
                   'classpath' : cpW
                  }

.. note:: Having the ``'java'`` key is the trigger to use the IOM access method.
.. note:: When using the IOM access method (``'java'`` key specified), the 
         absence of the ``'iomhost'`` key is the trigger to use a local Windows
         session instead of remote IOM (it is a different connection type).



IOM to MVS SAS
~~~~~~~~~~~~~~
Yes, you can even connect to a SAS server running on MVS (Mainframe SAS). 
There are a couple of requirements for this to work right. First, you need version 2.1.5 or higher of this module.
There were a couple tweaks I needed to make to the IOM access method and those are in 2.1.5.

Also, you need to use the HFS file system for the WORK (and/or USER) library and you also need to set the default file
system to HFS so temporary files used by this module use HFS instead of the native MVS file system. You can still access
the native file system in the code you run, but for internal use, this module needs to access the HFS file system.
To set the default file system (options filesystem=hfs;) you can either set it in the workspace severs config file,
or you can submit the options statement from your python code after making a connection: 


::

    sas = saspy.SASsession()
    ll  = sas.submit('options filesystem=hfs;')


The other thing is to set the encoding correctly for this to work. MVS is an EBCDIC system, not ASCII. For the most part,
this is all handled in IOM for you, but there is a small amount of transcoding required internally in this module. The 
default encoding on MVS is OPEN_ED-1047, although it can be set to any number of other EBCDIC encodings. The default Python
encodings do not include the 1047 code page. I did find a 'cp1047' code page in a separate pip installable module which
seems to match the OPEN_ED-1047 code page. 

At the time of this writing, the only transcoding I need to do in python for this to work can be accomplished using the
'cp500' encoding which is part of the default set, so you don't have to install other modules. It's possible this could
change in the future, but I don't have any expectations of that for now, so using 'cp500' is ok if you don't want to
install other non-standard python modules. 


