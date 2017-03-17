
.. Copyright SAS Institute

.. currentmodule:: saspy


===============
Troubleshooting
===============

This chapter covers covers troubleshooting procedures with SASPy. While we don't expect you to have trouble,
there are some cases where you might not have everything working right. We've tried to provide an easy reference
for diagnosing and fixing those issues here.
 

***********************************
Connection and configuration issues
***********************************

Although setting up and configuring SASPy is pretty simple, if you do have something not quite right, it
may be hard to figure out what's wrong. That's when you come to this chapter. 

We've added quite a bit of self diagnostics and error messages for many of the likely issues that can
happen trying to start up a connection to SAS. Each access method has its own set of usual suspects. With a 
little help and explaination here, you can probably diagnose and correct any issue you might have.

Problems in this category will be when using the saspy.SASsession() method to connect to a SAS session.
The very first thing to look at is your sascfg.py file (in the saspy instalation). This is where the
configurations definition are. The file itself has documentation and so does :doc:`configuration`.


Common diagnostics
------------------

Although each access method has its own ways something can go wrong, there are some common diagnostics
you will get and can use to track down the issue.

The first is that if the SASsession() method fails, it will return any erros it can, as well as the 
actual command it was trying to run to connect to SAS. That will vary with access method, but in each
case, you can cut-n-paste that command into a shell on the machine where SASPy (python) is running
and that may very well provide more diagnostics and error messages that SASPy may have displayed.

For instance, here's a very simple case using the STDIO access method on a local linux machine. The 
Configuration Definition is nothing but a valid path that should work.

.. code:: ipython3

    default  = {'saspath': '/opt/sasinside/SASHome/SASFoundation/9.4/bin/sas_u8'}

When I try to run I get the following:

.. code:: ipython3

    Linux-1> python3.5
    >>> import saspy
    >>> sas = saspy.SASsession()

    SAS Connection failed. No connection established. Double check you settings in sascfg.py file.
    
    Attempted to run program /opt/sasinside/SASHome/SASFoundation/9.4/bin/sas_u8 with the following parameters:
    ['/opt/sasinside/SASHome/SASFoundation/9.4/bin/sas_u8', '-nodms', '-stdio', '-terminal', '-nosyntaxcheck', '-pagesize', 'MAX', '']
    
    Try running the following command (where SASPy is running) manually to see if you can get more information on what went wrong:
    /opt/sasinside/SASHome/SASFoundation/9.4/bin/sas_u8 -nodms -stdio -terminal -nosyntaxcheck -pagesize MAX
    
    No SAS process attached. SAS process has terminated unexpectedly.

I can see from that error it didn't work, but it didn't really tell me why or what to do about it. Well,
it did say I should try running that command to see if I could get better diagnostics. What the heck, let's try:


.. code:: ipython3

    Linux-1> /opt/sasinside/SASHome/SASFoundation/9.4/bin/sas_u8 -nodms -stdio -terminal -nosyntaxcheck -pagesize MAX

    ERROR: The current date of Tuesday, March 14, 2017 is past the final
    ERROR: expiration date for your SAS system, which is Monday, January 2, 2017.
    ERROR: Please contact your SAS Installation Representative to obtain your
    ERROR: updated SAS Installation Data (SID) file, which includes SETINIT
    ERROR: information.
    To locate the name of your SAS Installation Representative go to
    http://support.sas.com/repfinder and provide your site number 70068118 and
    company name as Linux for x64 All Compatible Non-Planning Products. On the
    SAS REP list provided, locate the REP for operating system LIN X64.
    ERROR: Initialization of setinit information from SASHELP failed.
    NOTE: Unable to initialize the options subsystem.
    ERROR: (SASXKINI): PHASE 3 KERNEL INITIALIZATION FAILED.
    ERROR: Unable to initialize the SAS kernel.

Well go figure. My SAS has expired.  

The same process can be used with other access methods. IOM uses Java, so you could have a classpath issue
which you won't see unless you run the command yourself from a shell and then you can get a traceback or
other errors from java that didn't make it back to SASPy to display.


STDIO
-----

There are only a couple of things that can go wrong here. First, this only works on Unix, not Windows,
so if you're having problems getting to to work from Windows, well there you go.
Second, the only thing you really need to have right is the path to the SAS startup script in your SAS
instalation. The 'saspath' value in your configuration definition needs to be correct and accessible.  


STDIO over SSH
--------------

The same issues in STDIO above are true here, with one extra component; ssh. This method is still only
valid on Unix, not Windows (both client side and SAS side). The 'saspath' value has to be right, and 
it has to be right on the Remote Unix machine that you are ssh'ing to. That might not be the same path
as on your local Unix SAS deployment. 

Secondly, this requires that you have passwordless ssh configured and working for each user that will
be connecting between the local and remote machines. That can be diagnosed independant of SASPy or python.
If the connection cannot be made, you should see that error message with the command that SASPy was
trying to execute, and you can run it to get better diagnostic error messages that can tell you if its
a problem with your ssh credentials, the machine you're trying to reach isn't listening, or any other
problem there might be.

.. code:: ipython3

    >>> import saspy
    >>> sas = saspy.SASsession(cfgname='ssh')
    SAS Connection failed. No connection established. Double check you settings in sascfg.py file.
    
    Attempted to run program /usr/bin/ssh with the following parameters:['/usr/bin/ssh', '-t', 'tom64-2', '/opt/sasinside/SASHome/SASFoundation/9.4/bin/sas_en',
                                                                         '-fullstimer', '-nodms', '-stdio', '-terminal', '-nosyntaxcheck', '-pagesize', 'MAX', '']
    
    Try running the following command (where saspy is running) manually to see if you can get more information on what went wrong:
    /usr/bin/ssh -t tom64-2 /opt/sasinside/SASHome/SASFoundation/9.4/bin/sas_en -fullstimer -nodms -stdio -terminal -nosyntaxcheck -pagesize MAX

    No SAS process attached. SAS process has terminated unexpectedly.
   
So, running that command can tell me what the problem is.
   
.. code:: ipython3

    Linux-1> /usr/bin/ssh -t Linux-2 /opt/sasinside/SASHome/SASFoundation/9.4/bin/sas_en -fullstimer -nodms -stdio -terminal -nosyntaxcheck -pagesize MAX
    ssh: Could not resolve hostname Linux-2: Name or service not known

    or maybe another problem:

    Linux-1> /usr/bin/ssh -t Linux-2 /opt/sasinside/SASHome/SASFoundation/9.4/bin/sas_en -fullstimer -nodms -stdio -terminal -nosyntaxcheck -pagesize MAX
    ssh: connect to host Linux-2 port 22: Connection refused

    or if it is that you do not have passwordless ssh set up, even though you can connect to that machine, you might see this (prompting you for pw)

    Linux-1> /usr/bin/ssh -t Linux-2 /opt/sasinside/SASHome/SASFoundation/9.4/bin/sas_en -fullstimer -nodms -stdio -terminal -nosyntaxcheck -pagesize MAX
    user@Linux-2's password:
    Permission denied, please try again.
    user@Linux-2's password:
    Permission denied, please try again.
    user@Linux-2's password:
    Permission denied (publickey,gssapi-keyex,gssapi-with-mic,password).



IOM
---

This access method has the most possibilities of having something misconfigured, because it has more 
components that all have to connect together. But, it also has the most diagnostics to help you out.
There are basically two possibilities where something can go wrong; Java or IOM. Lets look at Java first.

There are two things that are likely to be the problem.

   1) Java isn't installed or configured right, or you don't have the right java command  for 'java' in your Configuration Definition
   2) You don't have your classpath right, or don't have the right jars.

Neither of these problems will result in a good message from SASPy telling you what the problem is. But, like in the cases above,
if the problem is that Java won't start up, you will get the exact command trying to be run, so you can run it and see more diagnostics
and error messages.

.. code:: ipython3

    >>> sas = saspy.SASsession(classpath='wronpath')
    SAS Connection failed. No connection established. Staus=(11358, 256)  Double check you settings in sascfg.py file.
    
    Attempted to run program /usr/bin/java with the following parameters:['/usr/bin/java', '-classpath', 'wronpath', 'pyiom.saspy2j', '-host', 'localhost', '-stdinport', '38228', '-stdoutport', '47074',
                                                                          '-stderrport', '60464', '-iomhost', 'Linux-1'  '-iomport', '8591', '-user', 'user', '']
    
    Try running the following command (where saspy is running) manually to see if it's a problem starting Java:
    /usr/bin/java -classpath wronpath pyiom.saspy2j -host localhost -stdinport 38228 -stdoutport 47074 -stderrport 60464 -iomhost Linux-1 -iomport 8591 -user user
    
    No SAS process attached. SAS process has terminated unexpectedly.
    >>>

    Linux-1> /usr/bin/java -classpath wronpath pyiom.saspy2j -host localhost -stdinport 38228 -stdoutport 47074 -stderrport 60464 -iomhost Linux-1 -iomport 8591 -user user
    Error: Could not find or load main class pyiom.saspy2j

That error shows that there is an issue with the classpath, as Java could not find the saspyiom.jar. You might also see a Java traceback for cases where you have some of the jars
in the path but are missing others.

If you run the Java command and you see an error similar to the following, about a socket connection failure, that suggests that your classpath is correct
and that the problem might be connecting to the IOM server. That error shows that java came up and is running code from saspyiom.jar. It is trying to connect
back to the saspy python process, which isn't running, thus the connection error. But it means, at least, saspyiom.jar was found.

.. code:: ipython3

    java.net.ConnectException: Connection refused
            at java.net.PlainSocketImpl.socketConnect(Native Method)
            at java.net.AbstractPlainSocketImpl.doConnect(AbstractPlainSocketImpl.java:350)
            at java.net.AbstractPlainSocketImpl.connectToAddress(AbstractPlainSocketImpl.java:206)
            at java.net.AbstractPlainSocketImpl.connect(AbstractPlainSocketImpl.java:188)
            at java.net.SocksSocketImpl.connect(SocksSocketImpl.java:392)
            at java.net.Socket.connect(Socket.java:589)
            at java.net.Socket.connect(Socket.java:538)
            at java.net.Socket.<init>(Socket.java:434)
            at java.net.Socket.<init>(Socket.java:211)
            at pyiom.saspy2j.main(saspy2j.java:109)
    Exception in thread "main" java.lang.NullPointerException
            at pyiom.saspy2j.main(saspy2j.java:116)

Now, if Java is coming up, but you still fail to connect, then it is a problem connecting to IOM. There are a few obvious misconfigurations
that can happen here. 

   1) The 'iomhost' or 'iomport' you've specified aren't right, or the server isn't up and available to be connected to.
   2) Your credentials were specifed wrong, or you don't have permission to connect.
   3) for Windows Local connection, you don't have the path to the *sspiauth.dll* in yout System Path variable  


.. code:: ipython3

    >>> sas = saspy.SASsession(iomport=333)
    The application could not log on to the server "Linux-1:333". No server is available at that port on that machine.
    SAS process has terminated unexpectedly. Pid State= (11195, 64000)
    SAS Connection failed. No connection established. Double check you settings in sascfg.py file.
    
    Attempted to run program /usr/bin/java with the following parameters:['/usr/bin/java', '-classpath', '/jars/sas.svc.connection.jar:/jars/log4j.jar:/jars/sas.security.sspi.jar:/jars/sas.core,jar:
    /jars/saspyiom.jar', 'pyiom.saspy2j', '-host', 'localhost', '-stdinport', '45757', '-stdoutport', '57809', '-stderrport', '33153', '-iomhost', 'Linux-1', '-iomport', '333', '-user', 'user', '']
        
    No SAS process attached. SAS process has terminated unexpectedly.
    

.. code:: ipython3


    >>> sas = saspy.SASsession(omruser='wrong_user')
    The application could not log on to the server "Linux-1:8591". The user ID "wrong_user" or the password is incorrect.
    SAS process has terminated unexpectedly. Pid State= (11449, 64000)
    SAS Connection failed. No connection established. Double check you settings in sascfg.py file.
    
    Attempted to run program /usr/bin/java with the following parameters:['/usr/bin/java', '-classpath', '/jars/sas.svc.connection.jar:/jars/log4j.jar:/jars/sas.security.sspi.jar:/jars/sas.core,jar:
    /jars/saspyiom.jar', 'pyiom.saspy2j', '-host', 'localhost', '-stdinport', '49660', '-stdoutport', '46794', '-stderrport', '51907', '-iomhost', 'Linux-1', '-iomport', '8591', '-user', 'wrong_user', '']
    
    No SAS process attached. SAS process has terminated unexpectedly.



.. code:: ipython3


    >>> import saspy
    >>> sas = saspy.SASsession()
    
    The native implementation module for the security package could not be found in the path.The native implementation module for the security package could not be found in the path.
    SAS process has terminated unexpectedly. RC from wait was: 4294967290
    SAS Connection failed. No connection established. Double check you settings in sascfg.py file.
    
    Attempted to run program java with the following parameters:['java', '-classpath', 'C:\\Program Files\\SASHome\\SASDeploymentManager\\9.4\\products\\deploywiz__94472__prt__xx__sp0_
    _1\\deploywiz\\sas.svc.connection.jar;C:\\Program Files\\SASHome\\SASDeploymentManager\\9.4\\products\\deploywiz__94472__prt__xx__sp0__1\\deploywiz\\log4j.jar;C:\\Program Files\\SA
    SHome\\SASDeploymentManager\\9.4\\products\\deploywiz__94472__prt__xx__sp0__1\\deploywiz\\sas.security.sspi.jar;C:\\Program Files\\SASHome\\SASDeploymentManager\\9.4\\products\\dep
    loywiz__94472__prt__xx__sp0__1\\deploywiz\\sas.core.jar;E:\\metis-master\\saspy_pip\\saspy\\java\\saspyiom.jar', 'pyiom.saspy2j', '-host', 'localhost', '-stdinport', '55330', '-std
    outport', '55331', '-stderrport', '55332', '-zero', '']
    
    Be sure the path to sspiauth.dll is in your System PATH
    
    No SAS process attached. SAS process has terminated unexpectedly.
    
    

So, hopefully this has shown you how to diagnose connection and configuration problems with SASPy. When you have things set up right, you shouldn't
have any problems, it should just work! 



*********************
Problems running code
*********************


My model didn't run
-------------------

When you run an analytical method there are a number of things that occur.
The goal is to have informative messages when things go wrong and in this section we'll explain what his happening
and how to check the various stages

#. Are the required parameters included?
   Each analytical method has a set of required parameters (there are a few that have an empty set but
   all the methods must have this specified).

   The simplest way to find the required and optional parameters is to use the `'?'` functionality.

   Here are two examples for the forest and hplogistic methods respectively:

   ::

       ?ml.forest()
       ?stat.hplogistic()

   The next best option is to use the :doc:`api` for the given method
   Both ways will show you the set of required parameters and then the list of optional parameters. The requred set
   and optional make up the complete set of parameters the method will take.

   If you are missing required parameters you will receive a SyntaxError and processing will stop.

   .. parsed-literal::

       SyntaxError: You are missing 1 required statements:
       {'model'}

   Missing optional parameter will produce no warning.

   **NOTE:** The `data` parameter does not appear in the required set but it is required for all modeling methods.

#. Do you have extra parameters
   If you include parameters that are neither required *or* optional then will be removed but as a best practice
   don't test the system.

#. Are the parameter the correct type
   Parameters must be specified with the correct type. If you provided an invalid type you should recieve a
   SyntaxWarning or SyntaxError and processing will stop.

   Here are a few of the most common parametes and their valid types

   * The `data` parameter must be a `SASData`_ object

   * The `model` parameter is a str

   * The `target` and `inputs` can be str, list, or dict types

   * The `nominals` must be a list type

   Making the parameters handle more types is a great way to get involved. Enter an issue and we can help you.

#. Were errors generated during execution
   If you make it this far the error is probably in the running of the genereated SAS code.
   To investigate you can `ERROR_LOG` attribute on your `SASResult`_ object.

   ::

       rf_model.ERROR_LOG

   The resulting output will the SAS log for that generated code. You will be able to see the SAS syntax and then
   and error or warning messages in context.

   **NOTE:** If the `ERROR_LOG` doesn't give you enough information to resolve your issue you can execute the
   following code (assuming your session object is named `sas`)

   ::

       print(sas.saslog())

   This will output the SAS log for then entire session (since you last restarted the kernel or your initial connection)

