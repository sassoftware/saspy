
.. Copyright SAS Institute

.. currentmodule:: saspy


===============
Advanced topics
===============

In this chapter we will explore more detailed explanations of specific functionality.


****************
Using Batch mode
****************

Batch mode is meant to be used when you want to automate your code as Python scripts.

In batch mode, any method that would normally display results, returns a Python dictionary
instead and with two keys; LOG, LST. This is the same as how the submit() method works 
normally. 

The LOG has the SAS Log and the LST contains the results. You will likely want to set 
the results parameter to HTML (this was originally the default instead of Pandas). When
you set the results to HTML, not only are plots and graphs in HTML, but also tabular results
too.

The example below shows the contents of a Python script that runs a linear regression and 
writes all the results to a directory. You can access the directory with a web browser to
view these results by clicking on them. Adjust the filesystem path below and you should 
be able to run this code yourself.


.. code-block:: ipython3

    #! /usr/bin/python3.5
    
    import saspy
    sas = saspy.SASsession(results='html')
    
    cars = sas.sasdata('cars', libref='sashelp')
    
    sas.set_batch(True)
    
    stat = sas.sasstat()
    res = stat.reg(model='horsepower = Cylinders EngineSize', data=cars)
    
    for i in range(len(res._names)):
        x = res.__getattr__(res._names[i])
        if type(x) is not str:
            out1 = open("C:\\Public\\saspy_demo\\"+res._names[i]+".html", mode='w+b')
            out1.write(x['LST'].encode())
            out1.close()
        else:
            out1 = open("C:\\Public\\saspy_demo\\"+res._names[i]+".log", mode='w+b')
            out1.write(x.encode())
            out1.close()
    
    
The URL to see these results is: file:///C:/Public/saspy_demo/. Of course, you can
imagine integrating the results into nicer web page for reporting, but with nothing more 
than this few lines of code, you can have the results updated and refreshed by just 
re-running the script.

 
*********
Prompting
*********

There are two types of prompting that can be performed; meaning to stop processing and
prompt the user for input and then resume processing.

The first type of prompting is performed implicity. When you run the 
SASsession() method, if any required parameters for the chosen connection method 
were not specified in the configuration definition (in sascfg_personal.py), processing is interrupted 
so that the user can be prompted for the missing parameters. In addition, when there 
is more than one configuration definition in SAS_config_names, and cfgname is not 
specified in the SASsession() method (or an invalid name is specified), the user will 
be prompted to select the configuration definition to use.

The other kind of prompting is prompting that you control. The submit() method, 
and the saslib() methods both take an optional prompt parameter. This parameter 
is how you request to have the user prompted for input at run time. This option 
is used in conjunction with SAS macro variable names that you enter in the SAS 
code or options for the method.

The prompt parameter takes a Python dictionary. The keys are the SAS macro variable 
names and the values are True or False. The Boolean value indicates whether it 
is to hide what the user types in or not. It also controls whether the macro variables 
stay available to the SAS session or if they are deleted after running that code. 

You will be prompted for the values of your keys, and those values will be assigned
to the SAS macro variables for you in SAS. When your code runs, the macro variables will be 
resolved. If you specified ``True``, then the value the user types is not displayed, 
nor is the macro variable displayed in the SAS log, and the macro variable is deleted 
from SAS so that it is not accessible after that code submission. For ``False``, the 
user can see the value as it is type, the macro variables can be seen in the SAS log 
and the variables remain available in that SAS session for later code submissions.

The following are examples of how to use prompting in your programs. The first example 
uses the saslib() method to assign a libref to a third-party database. This is a
common issue--the user needs to specify credentials, but you do not want to include
user IDs and passwords in your programs. Prompting enables the user to provide
credentials at runtime.

.. code-block:: ipython3

    sas.saslib('Tera', engine='Teradata', options='user=&user pw=&mypw server=teracop1', 
               prompt={'user': False, 'mypw': True})

At runtime, the user is prompted for user and password and sees something like the
following when entering values (the user ID is visible and the password is obscured):

.. parsed-literal::

    Please enter value for macro variable user sasdemo
    Please enter value for macro variable mypw ........
 
Another example might be that you have code that creates a table, but you want to let 
the user choose the table name as well as the name of the column and a hidden value 
to assign to it. By specifing ``False``, the user can see the value, and the SAS log 
shows the non-hidden macro mariables, followed by another code submission that uses 
the previously defined non-hidden variables--which are still available.

.. code-block:: ipython3

    ll = sas.submit('''
    data &dsname;
      do &var1="&pw"; 
        output; 
      end;
    run;
    ''', prompt={'var1': False, 'pw': True, 'dsname': False})


.. parsed-literal::

    Please enter value for macro variable var1 MyColumnName
    Please enter value for macro variable hidden ........
    Please enter value for macro variable dsname TestTable1    
    
    print(ll['LOG'])

    103  ods listing close;ods html5 (id=saspy_internal) file=stdout options(bitmap_mode='inline') device=svg; ods graphics on /
    103! outputfmt=png;
    NOTE: Writing HTML5(SASPY_INTERNAL) Body file: STDOUT
    104  
    105  options nosource nonotes;
    108  %let var1=MyColumnName;
    109  %let dsname=TestTable1;
    110  
    111  data &dsname;
    112    do &var1="&hidden";
    113      output;
    114    end;
    115  run;
    NOTE: The data set WORK.TESTTABLE1 has 1 observations and 1 variables.
    NOTE: DATA statement used (Total process time):
          real time           0.00 seconds
          cpu time            0.00 seconds
          
    116  
    117  proc print data=&dsname;
    118  run;
    NOTE: There were 1 observations read from the data set WORK.TESTTABLE1.
    NOTE: PROCEDURE PRINT used (Total process time):
          real time           0.00 seconds
          cpu time            0.00 seconds
          
    119  
    120  options nosource nonotes;
    123  
    124  ods html5 (id=saspy_internal) close;ods listing;


    HTML(sas.submit('''
    proc print data=&dsname;
    run;
    ''')['LST'])

    Obs     MyColumnName
    1       cant see me


That is a highly contrived example, but you get the idea. You can prompt users 
at runtime for values you want to use in the code, and those values can be 
kept around and used later in the code, or hidden and inaccessible afterward.


***************************************************************
Moving values between Python Variables and SAS Macro Variables
***************************************************************

There are two methods on the SASsession object you can use to transfer values between Python and SAS.
symget() and symput(). To get a value from a SAS Macro Variable and assign it to a Python variable you
just call symget with the name of the macro variable.

.. code-block:: ipython3

    py_var = sas.symget(sas_macro_var)

To set the value of a SAS Macro Variable using the value of a Python variable, use symput() specifying
the macro variable name, and providing the python variable continaing the value.

.. code-block:: ipython3

    py_var = some_value
    sas.symput(sas_macro_var, py_var)

For a much better set of examples and use cases with these two methods, check out the notebook in saspy-examples:
https://github.com/sassoftware/saspy-examples/blob/master/SAS_contrib/Using_SYMGET_and_SYMPUT.ipynb



******************************************************************************
Slow performance loading SAS data into a Pandas DataFrame ( to_df(), sd2df() )
******************************************************************************

Transferring data from SAS into Python (and the reverse) has been in this module from the beginning. As usage of this has grown, 
larger sized data sets have been shown to be much slower to load and consume lots of memory. After investigations, this has to do with
trying to build out the dataframes 'in memory'. This works fine up to a point, but the memory consumption and CPU usage doesn't scale.

I've made enhancements to the algorithm, so it will work, as opposed to run indefinitely consuming too many resources, but it is still
too slow.

So, I've added a second method for doing this, using a CSV file as an intermediate store, then using the Pandas read_csv() method to create
the dataframe. This performs significantly faster, as it doesn't consume memory for storing the data in python objects. The read_csv() method
is much faster than trying to append data in memory as it's streamed into python from SAS.

There is now a parameter for these methods to specify which method to use: method=['MEMORY' | 'CSV'].
The default is still MEMORY. But you can specify CSV to use this new method: to_df(method='CSV'), sd2df(method='CSV').

There are also alias routines which specify this for you: to_df_CSV() and sd2df_CSV().

Another optimization with this is when saspy and SAS are on the same machine. When this is the case, there is no transfer required.
The CSV file written by SAS is the file specified in read_csv(). For remote connections, the CSV file still needs to be transferred from
SAS to saspy and written to disk locally for the read_csv() method. This is still significantly faster for larger data.

Starting in saspy version 3.1.7, there is now a third method for sd2df; 'DISK'. method=['MEMORY' | 'CSV' | 'DISK'], or the aliases
to_df_DISK() and sd2df_DISK(). This mehtod uses the same code as MEMORY to get the data, but stores it in a file, like the CSV method, so
that reading it into a dataframe w/ Pandas performs much better. This method allows better control over things like embedded delimiters
and newlines, which Pandas can have parsing problem with reading CSV file created from proc export.



*****************************************************************
Slow performance loading a DataFrame into a SAS data set; df2sd() 
*****************************************************************

df2sd (dataframe2sasdata) has two main steps, which were both done internal to the method. The second is transferring the data
but the first is figureing out the necessary metadata to be able to correctly define the SAS Data Set being created. This requires
identifying each column: it's name, data type, length (this is the crux here), required conversion type (date/time/datetime), ...

This metadata gathering step becomes slower the larger the data gets, only due to character columns. In SAS, I have to declare the
length in bytes, of the SAS session encoding, that the column requires to fit the data. DataFrames have no metadata about how long
any char columns are (they aren't char they are simply objects), so there's no way to know how long to declare these in SAS, other
than to apply a lanbda len function to each of these columns (transcoding to bytes in the SAS encoding), and taking the max value,
for each char column. That's all cute and nifty when the data doesn't have millions of rows and hunfreds of char columns. So, as
of V3.6.0, I've made some changes to accomodate data this large.

First, I've pulled the char length calculation code out of df2sd, into a public method (df_char_lengths()). df2sd calls this itself,
by default, so it's the same as before if you do nothing new. But, you can call that method, with a number of different paramerters
that can make it faster; calculate char length, not encoded byte lenghts (which is faster), and just multiply by the BPC (bytes per
char) of the SAS encoding (which I have defaults for or you can override and probvide your own BPC). This routine returns a dict with
each char column name and the length. df2sd can be passed these same parameters, so when it calls this method, it can do the same thing.

df2sd also can now take the dict that this routine will produce, or just a dict you code up with the lengths, skipping this whole 
disconvery process all together. So, you can code the lengths yourself, have df2sd do it but with some better performance, or call 
the method to calculate them and pass in that dict. This is good when you run df2sd on the same data more then once; figure out the 
lengths once and just pass in the dict all the times and never have to specd time recalculating.

Here are a few example cases showing this.

.. code-block:: ipython3

    # For this case SAS is running in UTF-8

    >>> sas
    Access Method         = IOM
    SAS Config name       = iomj
    SAS Config file       = /opt/tom/github/saspy/saspy/sascfg_personal.py
    WORK Path             = /sastmp/SAS_work528B00001B2F_tom64-5/SAS_work8B1F00001B2F_tom64-5/
    SAS Version           = 9.04.01M4D11092016
    SASPy Version         = 3.6.0
    Teach me SAS          = False
    Batch                 = False
    Results               = Pandas
    SAS Session Encoding  = utf-8
    Python Encoding value = utf_8
    SAS process Pid value = 6959
    
    # Create a dataframe of all CHAR columns from the cars dataset 

    >>> cars = sas.sasdata('cars','sashelp', results='text')
    >>> df = cars.to_df_DISK(dtype=str)
    >>> df.dtypes
    Make           object
    Model          object
    Type           object
    Origin         object
    DriveTrain     object
    MSRP           object
    Invoice        object
    EngineSize     object
    Cylinders      object
    Horsepower     object
    MPG_City       object
    MPG_Highway    object
    Weight         object
    Wheelbase      object
    Length         object
    dtype: object

    # Let's call the new method to get the char column lengths.

    >>> d1 =  sas.df_char_lengths(df); d1
    {'Length': 3, 'Invoice': 6, 'Wheelbase': 3, 'Model': 39, 'Make': 13, 'Cylinders': 3, 
     'DriveTrain': 5, 'Type': 6, 'MSRP': 6, 'MPG_City': 2, 'Weight': 4, 'MPG_Highway': 2,
     'Origin': 6, 'EngineSize': 3, 'Horsepower': 3}
    >>>
    
    # we can call df2sd on this DF and pass in the char col lengths so we skip that in df2sd

    >>> sd =  sas.df2sd(df, char_lengths=d1); sd
    Libref  = WORK
    Table   = _df
    Dsopts  = {}
    Results = Pandas
    
    >>> sd.columnInfo()
        Member  Num     Variable  Type  Len  Pos
    0   WORK.B    9    Cylinders  Char    3   84
    1   WORK.B    5   DriveTrain  Char    5   64
    2   WORK.B    8   EngineSize  Char    3   81
    3   WORK.B   10   Horsepower  Char    3   87
    4   WORK.B    7      Invoice  Char    6   75
    5   WORK.B   15       Length  Char    3  101
    6   WORK.B   11     MPG_City  Char    2   90
    7   WORK.B   12  MPG_Highway  Char    2   92
    8   WORK.B    6         MSRP  Char    6   69
    9   WORK.B    1         Make  Char   13    0
    10  WORK.B    2        Model  Char   39   13
    11  WORK.B    4       Origin  Char    6   58
    12  WORK.B    3         Type  Char    6   52
    13  WORK.B   13       Weight  Char    4   94
    14  WORK.B   14    Wheelbase  Char    3   98
    >>>
    
    # you can just create your own dict with lengths you want, also, and skip the discovery step altogether. 

    >>> d1 = {}
    >>> for col in df.columns:
    ...    d1[col]  = 10
    ...
    >>> d1['Make']  = 15
    >>> d1['Model'] = 40
    >>> d1
    {'MSRP': 10, 'Type': 10, 'Length': 10, 'MPG_City': 10, 'Invoice': 10, 'Model': 40, 'DriveTrain': 10, 'Horsepower': 10, 'Make': 15, 'Wheelbase': 10, 'EngineSize': 10, 'Origin': 10, 'Cylinders': 10, 'MPG_Highway': 10, 'Weight': 10}
    >>> sd =  sas.df2sd(df, char_lengths=d1); sd
    Libref  = WORK
    Table   = _df
    Dsopts  = {}
    Results = Pandas
    
    >>> sd.columnInfo()
          Member  Num     Variable  Type  Len  Pos
    0   WORK._DF    9    Cylinders  Char   10  115
    1   WORK._DF    5   DriveTrain  Char   10   75
    2   WORK._DF    8   EngineSize  Char   10  105
    3   WORK._DF   10   Horsepower  Char   10  125
    4   WORK._DF    7      Invoice  Char   10   95
    5   WORK._DF   15       Length  Char   10  175
    6   WORK._DF   11     MPG_City  Char   10  135
    7   WORK._DF   12  MPG_Highway  Char   10  145
    8   WORK._DF    6         MSRP  Char   10   85
    9   WORK._DF    1         Make  Char   15    0
    10  WORK._DF    2        Model  Char   40   15
    11  WORK._DF    4       Origin  Char   10   65
    12  WORK._DF    3         Type  Char   10   55
    13  WORK._DF   13       Weight  Char   10  155
    14  WORK._DF   14    Wheelbase  Char   10  165
    >>> sd.head()
        Make           Model   Type Origin DriveTrain   MSRP Invoice EngineSize Cylinders Horsepower MPG_City MPG_Highway Weight Wheelbase Length
    0  Acura             MDX    SUV   Asia        All  36945   33337        3.5         6        265       17          23   4451       106    189
    1  Acura  RSX Type S 2dr  Sedan   Asia      Front  23820   21761          2         4        200       24          31   2778       101    172
    2  Acura         TSX 4dr  Sedan   Asia      Front  26990   24647        2.4         4        200       22          29   3230       105    183
    3  Acura          TL 4dr  Sedan   Asia      Front  33195   30299        3.2         6        270       20          28   3575       108    186
    4  Acura      3.5 RL 4dr  Sedan   Asia      Front  43755   39014        3.5         6        225       18          24   3880       115    197
    >>>



*****************************************************************************
Using Proc iomoperate to find Object Spawner hosts and Workspace Server ports
*****************************************************************************

If you already use a client to connect to IOM servers, you may have the host and port to OMR
(the SAS Metadata Server), but not necessarily those of the Object Spawners or Workspace Servers.
For Remote IOM connections there are three configuration keys that require some of this other information.
If you can connect to your OMR Server, then you can use the following code to find out the information you need.

The three configuration keys are:

.. code-block:: ipython3

    iomhost - 
        (Required) The resolvable host name, or IP address to the IOM object spawner.
        New in 2.1.6; this can be a list of all the object spawners hosts if you have load balanced object spawners.
        This provides Grid HA (High Availability)
    iomport - 
        (Required) The port that object spawner is listening on for workspace server connections (workspace server port - not object spawner port!).
    appserver -
        If you have more than one AppServer defined on OMR, then you must pass the name of the physical workspace server
        that you want to connect to, i.e.: 'SASApp - Workspace Server'. Without this the Object spawner will only try the
        first one in the list of app servers it supports.


First, query to find any available Object Spawners. You would use the 'Machine name :' value(s) from
this for the 'iomhost' configuration key. Note that often there will only be one Object Spawner, but
there can be more then one configured.

.. code-block:: ipython3

    proc iomoperate
      uri="iom://omrhost.abc.xyz.com:8561;Bridge;USER=omruserid,PASS=omrpasswd";
      list DEFINED FILTER="Object";
    quit;

The reuslts from this should include output like the following for any defined Object Spawners.
Use the 'Machine name :' value for your 'iomhost' key.

.. code-block:: ipython3

    Object Spawner - objhost (A5H4N590.AY000003)
        Server class : IOM Spawner
        Spawnable server component : Operating System Services - objhost
        Spawnable server component : SASApp - Pooled Workspace Server
        Spawnable server component : SASApp - Stored Process Server
        Spawnable server component : SASApp - Workspace Server
        Operator port : 8581
        PortBank port : 8801
        PortBank port : 8811
        PortBank port : 8821
        Machine name : objhost.abc.xyz.com


Next, query to find any available Workspace Servers. You would use the 'Bridge port :' value from
this for the 'iomport' configuration key. When you have multiple Workspace Servers configured, which
really means you have multipe SASApp's defined (see 'Server context :' value in the output below), 
you will want to set the 'appserver' configuration key to the SASApp Workspace Server that you want
to (or have permission to) connect to. The value to use is the name shown in the output for the server;
'SASApp - Workspace Server' in the output below.  

.. code-block:: ipython3

    proc iomoperate
      uri="iom://omrhost.abc.xyz.com:8561;Bridge;USER=omruserid,PASS=omrpasswd";
      list DEFINED FILTER="- Workspace";
    quit;

The reuslts from this should include output like the following for any defined Workspace Servers.
Use the 'Bridge port :' value for your 'iomport' key.

.. code-block:: ipython3

    SASApp - Workspace Server (A5H4N590.AY000009)
        Server class : 440196D4-90F0-11D0-9F41-00A024BB830C
        Logical name : SASApp - Logical Workspace Server
        Server context : SASApp
        Bridge port : 8591
        Machine name : wrkhost.abc.xyz.com


If your site has a complex setup, you may have multiple Object Spawners and/or Workspace Servers.
If so, it's possible that the Workspace Server you want to use is only spawnable for a particular
Object Spawner. You can correlate those by looking for the name of your Workspace Server in the
'Spawnable server component :' of the Object Spawner output. 

Also, if you have multiple Workspace Server that you want to be able to connect to, you can define
a separate configuration definition (in your sascfg[_personal].py) for each one. A good naming 
convention for these is to use the 'Server context :' value as the config name. That way it's easy
to know which server you will be connecting to.


**************************************************************
Disconnecting from an IOM session and reconnecting back to it.
**************************************************************

The IOM access method has the ability to disconnect from the workspace server and
reconnect to it (the same one); IF the reconnect setting is configured for that workspace
server in the Metadata Server. See 'Client Reconnect' Advanced Options of the Workspace Server.
This feature is new in version 2.2.2.

This was implemented for cases like having a laptop in a docking station, connected to LAN (Ethernet).
Then needing to take the laptop to a meeting; network switched to WiFi. Switching the network will lose
the connection to the workspace server.

In order to have this work, before disconnecting from your current network, you submit the disconnect()
method of the SASsession object. You can then change networks. After you have a good network connection again,
the next thing you submit will reconnect to that same workspace server and run.
 

.. code-block:: ipython3

    sas = saspy.SASsession(cfgname='someIOMconfig')
    [do some work with saspy]
    sas.disconnect()
    [switch networks. be sure you have established a network connection]
    do more saspy work


*******************************************************************
Configuring Grid Option Sets to have saspy run on a specific Queue.
*******************************************************************

Working with Grid Options Sets is documented here (the 'Doc' referred to below):
http://support.sas.com/documentation/cdl/en/gridref/67371/HTML/default/viewer.htm#n1inymfs0b7go2n147xdknz0ygpx.htm

There is also a SASPy issue with details on this here: 
https://github.com/sassoftware/saspy/issues/82

This is specific to the IOM Access Method, as that is how saspy connects to the SAS Grid with this functionality.
The Appname that saspy connects as is 'SASPy'; as in APPNAME=SASPy 
 
There are 2 steps to setting this up. The first is to define the SASPy Application in metadata and set it as Grid Capable.
That part in the doc (link referenced above) is at the bottom, named 'Specifying That an Application Is Grid Capable'. 

The second is to select and configure that SASPy App in the Grid Options Set Mapping Wizard; the first part of the doc. 

1) in the 'Folders' view in SMC (like in the picture in the doc link), there's a list of applications. The doc has the SAS Addin for Microsoft Office selected.
If you right click on Applications, you can selct 'New'->'Folder.

2) Do that and set the name of the new folder to SASPy. Then right click and select Properties - just like in the picture in the doc. 
Then add a Keyword-> 'isGridCapable' and save it. Just like the picture in the doc.

After creating the SASPy folder (application), and setting it to grid capable, when you go back
in to the grid options mapping wizard (the first part of the document referenced above), SASPy
should now be available to choose and you can set this up as you want.


**********************************
Dates, Times and Datetimes, Oh my!
**********************************

The sd2df and df2sd methods transfer data between SAS Data Sets and Pandas dataframes. For most
cases, if you start with a SAS dataset and import it to a dataframe, then send it back to SAS,
you should end up with the same data in SAS as you started with. However, there are some caveats.
First, SAS Formats do not transfer to a dataframe, so on the round trip the new SAS dataset will
not necessarily have the same formats defined on it as the original data set. Starting in saspy
version3.2.0, there is an option on df2sd to specify the formats you want defined on the new data
set; outfmts={}. The keys for this are the column names and the values are the SAS formats you
want defined.                                                                                                                     

For example:
df2sd(..., outfmts={'col1' : 'YYMMDD.', 'col2' : 'TIMEAMPM.', 'some_numeric_col' : 'comma32.4'})

To see the formats that are defined on the original data set, use the contents() or columnInfo()
method on that SASdata object.

One other issue is with SAS variables having Date and Time formats, which are logically data types
of Date or Time. SAS only really has Numeric and Character data types, but the date, time, and
datetime formats on Numeric variables identify them as representing date, time, or datetime data
types. Pandas dataframe, has a datetime datatype, but not a date or a time datatype. When using 
sd2df, any SAS variable with date, time or datetime formats will be created in the dataframe as a
datetime64[ns]. It is easy enough in python to reference only the date part, or time part of a
pandas datetime column. In fact the column can be converted to datetime.date or datetime.time
with one python statement. For instance, given datetime columns, the following can convert to 
the datetime date or time:

Given df_conv.dtypes:

.. code-block:: ipython3

    dt     datetime64[ns]
    tm     datetime64[ns]


    convert datetime columns to date or time only type (honoring missing values)
    
    nat = pd.to_datetime('')
    df_conv['dt'] = df_conv['dt'].apply(lambda x: x if x is nat else pd.Timestamp.date(x))
    df_conv['tm'] = df_conv['tm'].apply(lambda x: x if x is nat else pd.Timestamp.time(x))

    
    convert these back to datetimes
    
    df_conv['dt'] = pd.to_datetime(df_conv['dt'].astype('str'), errors='coerce')
    df_conv['tm'] = pd.to_datetime(df_conv['tm'].astype('str'), errors='coerce')                                                                                                


When using df2sd to transfer a dataframe to a SAS data set, with values you want to be stored as SAS
dates, times or datetimes, the following is the appropriate way to do so. In each case, the value
in the dataframe must be a Pandas datetime64 value. For datetimes this just works. For date or
time only values, specify the (new in V3.2.0) option datetimes={} on df2sd. The datetimes={} takes
keys of the column names and values of 'date' or 'time'. The code generated to create the SAS data
set will then only use the date or time portion of the Pandas datetime64 value to populate the SAS
variables, and assign default date or time formats for those variables. You can, of course, specify
specific date or time formats using the outfmts={} option if you want.

For example:
df2sd(..., datetimes={'d' : 'date', 't' : 'time'}) 

.. code-block:: ipython3

    >>> rows = [[datetime.datetime(1965, 1, 1, 8, 0, 1), datetime.datetime(1965, 1, 1, 8, 0, 1), datetime.datetime(1965, 1, 1, 8, 0, 1)]]
    >>> df = pd.DataFrame.from_records(rows, columns=['dt','d','t'])
    >>> df
                   dt                   d                   t
    0 1965-01-01 08:00:01 1965-01-01 08:00:01 1965-01-01 08:00:01

    >>> sd = sas.df2sd(df, datetimes={'d' : 'date', 't' : 'time'}, results='text')
    >>> sd.head()
    
    
                                                               The SAS System                         11:31 Friday, January 24, 2020   2
    
                                        Obs    dt                                d            t
    
                                         1     1965-01-01T08:00:01.000000    1965-01-01    08:00:01
    >>>
    >>> # For 'dt' column, we still import it as a datetime, but specifying a numeric format will display it as a number (seconds since Jan 1,  1960)
    >>> # and I've chosen different date and time formats for the other two variables too
    >>>
    >>> sd = sas.df2sd(df, datetimes={'d' : 'date', 't' : 'time'}, outfmts={'dt' : 'comma32.4', 'd' : 'YYMMDD.', 't' : 'TIMEAMPM.'}, results='text')
    >>> sd.head()
                                                               The SAS System                         09:59 Friday, January 24, 2020   1
    
                                     Obs                                  dt           d             t

                                      1                     157,881,601.0000    65-01-01    8:00:01 AM
    >>>
    
For more examples of this date, time, datetime conversion, see the example notebook here:
https://github.com/sassoftware/saspy-examples/blob/master/Issue_examples/Issue279.ipynb
    
    
    
***********************************
Advanced sd2df and df2sd techniques
***********************************

The sd2df and df2sd methods transfer data between SAS Data Sets and Pandas dataframes. For most cases,
you don't need to specify extra options. But, there are extra options to cover a variety of specific
use cases. The section above describes using the datetime= and outfmts= with df2sd, and this section will
show how to manipulate sd2df if you want your dataframe to have non-default dtypes. Based upon an issue
request to allow the dataframe created by sd2df to have differnent types than what are created by default,
there are a couple options which can be used to accomplish this.

Both the CSV and DISK methods of sd2df use Pandas read_csv method to create the dataframe from a file
containing the SAS data. The read_csv method has many options. By default the sd2df CSV and DISK methods
supply some of these parameters to control how the dataframe is created. There are two things in particular
that must correlate to get the correct results in the dataframe. They are the format of the data values,
for a given column, and the dtype specified for the creation of the column. The format of the data is 
controlled by the SAS format being used to write the data values. The dtype is controlled by the dtype= 
parameter on read_csv. By default saspy controls both of these, matching them up to create the valid
dataframe columns.

The sd2df* methods take a kwargs parameter. This can be used to pass through pandas parameters to the
create dataframe method. dtype= is one of these that you can pass through. If you pass this through,
then sd2df will not set the dtypes itself for any column. It will pass your dtype= value to read_csv. Now,
if the format of the data values doesn't match what Pandas can parse into the dtypes you specify, then
it won't work correctly. But, as of saspy version 3.2.0, there is an option (my_fmts=) to override
saspy's choice of formats for writing the data values and use the formats defined on the data set, or
specified by you via the dsopts= parameter (or attribute of a SASdata object); my_fmts = [**False** | True].
In this way, you can control both the format of the data values and the dtypes you want Pandas to create
from them.

Let's loot at an example. One request was to have all of the data in the dataframe be string types.
This can be done quite easily with just the dtype= parameter.

.. code-block:: ipython3

    # lets get two numerics from the cars dataset. FYI, they have formats defined as DOLLAR8. 
    df = sas.sd2df_DISK('cars', 'sashelp', dtype='str',      dsopts={'keep' : 'MSRP Invoice'})
    
    >>> df.dtypes
    MSRP       object
    Invoice    object
    dtype: object
    >>>
    >>> df.head()
        MSRP Invoice
    0  36945   33337
    1  23820   21761
    2  26990   24647
    3  33195   30299
    4  43755   39014
    >>>

Now, since we're creating these as stings, we probably want the SAS formatted version of the strings;
same as we would see in the SAS output of the data. So, we set my_fmts=True.

.. code-block:: ipython3

    df = sas.sd2df_DISK('cars', 'sashelp', dtype='str', my_fmts=True,     dsopts={'keep' : 'MSRP Invoice'})
    
    >>> df.dtypes
    MSRP       object
    Invoice    object
    dtype: object
    >>>
    >>> df.head()
          MSRP  Invoice
    0  $36,945  $33,337
    1  $23,820  $21,761
    2  $26,990  $24,647
    3  $33,195  $30,299
    4  $43,755  $39,014
    >>>
    

And, if you wanted to specify your own SAS format to use for this, overriding the ones defined on
the dataset, you can specify it on the dsopts=.

.. code-block:: ipython3

    df = sas.sd2df_DISK('cars', 'sashelp', dtype='str', my_fmts=True, 
                         dsopts={'keep' : 'MSRP Invoice', 'format' : {'msrp':'dollar32.2'}})
    >>> df.dtypes
    MSRP       object
    Invoice    object
    dtype: object
    >>>
    >>> df.head()
             MSRP  Invoice
    0  $36,945.00  $33,337
    1  $23,820.00  $21,761
    2  $26,990.00  $24,647
    3  $33,195.00  $30,299
    4  $43,755.00  $39,014
    >>>
    
The dtype= parameter can also be a dictionary for each column and type. See the Pandas doc for more
on that. So, you can control the format and type of each column yourself, but it is then up to you
to be sure the values can be parsed by Pandas to the types you specify. When using these options,
sd2df will not override anything you've provided, so you control it all.

One last example where You only want to override one column and have the other defaulted.

.. code-block:: ipython3

    df = sas.sd2df_DISK('cars', 'sashelp', dtype={'invoice' : 'int'}, my_fmts=True, 
                         dsopts={'keep' : 'MSRP Invoice', 'format' : {'msrp':'dollar32.2','invoice':'best32.'}})
    
    >>> df.dtypes
    MSRP       object
    Invoice     int64
    dtype: object
    >>> df.head()
             MSRP  Invoice
    0  $36,945.00    33337
    1  $23,820.00    21761
    2  $26,990.00    24647
    3  $33,195.00    30299
    4  $43,755.00    39014
    >>>
    
Remember, if you want to send data like this back to a SAS data set and you want the original types,
you need to have any numerics as a numeric type, dates, times or datetimes as a datetime64 type. You can
use the datetimes= to create date or time SAS variables from a full datetime, and anything that is 
an Object type, will be a character variable in SAS, with the str() of the object as the value.

There's more interesting reading about this on the issue that started it. Take a look at 
https://github.com/sassoftware/saspy/issues/279 to see where this fuctionality came from.



****************************************************************
Automatic checking for ERROR: in the LOG and the warnings module
****************************************************************

Based upon an enhancement request, as of version 3.6.7, SASPy now checks for 'ERROR:' and issues a message via the warnings module
to inform you that you should take a look at the log and see if there was a problem. SASPy methods won't blindly fail just by finding
the word ERROR in the log, because that doesn't always mean what was being done failed. Nor does not having that in the log mean everything
worked perfectly. SAS isn't that straight forward, unfortunately. Most methods verify what happened, when they can, but particularly on the
data transfer methods, there are any number of things that can happen, so querying the log after these, especially when first developing
workflows, is always a good thing. You can use the lastlog() method to see the log for the last method run or saslog() to see the entire
session log. 

There is also a new attribute on the SASsession object (my SASsession variable is 'sas' in the examples). This variable is a boolean
set to True when one of these warnings is issued (regardless of how you've configured warnings; I set it every time). The name is 'check_error_log'.
You can use this to programmatically check to see if there was an ERROR in the log. One catch is that it's up to you to reset the attribute 
to False (it is Fales when the session is created). So, if you are going to check it after running a SASPy method, you should set it to False
before running that method. I can't reset it since many methods submit multiple sets of SAS code, and I need to leave it set so it's set when
all the code for a given method has completed. There's no good place where I can explicitly reset it. It's easy enough to set and check though,
when you need to use it.  

Here are some examples of the warnings messages and some ways to configure them. For a full explanation of what you can do with 
warnings, refer to the Python documentation. Warnings is part of the Python Standard Library.


.. code-block:: ipython3

    >>> # I had a table which was giving an ERROR in the log, though any error from any method would do the same
    >>>
    >>> sas.saslib('x', path='~')
    >>>
    >>> sas.check_error_log
    False
    >>>
    >>>
    >>> sas.list_tables('x')
    /opt/tom/github/saspy/saspy/sasioiom.py:976: UserWarning: Noticed 'ERROR:' in LOG, you ought to take a look and see if there was a problem
      warnings.warn("Noticed 'ERROR:' in LOG, you ought to take a look and see if there was a problem")
    [('3 BAD NAME', 'DATA'), ('A', 'DATA'), ('AF', 'DATA'), ('CARSFR', 'DATA'), ('CHARF', 'DATA'), ('PRDSALE', 'DATA')]
    >>>
    >>> # we can check the attribut to programmatically see there was an error and do whatever we want to do in the program with that info
    >>> sas.check_error_log
    True
    >>> # and we should reset it to False before checking it again; usually right before a method we check it after.
    >>> sas.check_error_log = False
    >>>
    >>> # so, look at the log to see why there was an error - I'm only showing the line with the error to save space here
    >>>
    >>> print(sas.lastlog())
    
    [...]
    ERROR: Some character data was lost during transcoding in the dataset X.PRDSALE. Either the data contains characters that are not
           representable in the new encoding or truncation occurred during transcoding.
    [...]
    >>>
    >>> # Interesting, but that wasn't an error that kept my program from working
    >>>
    >>> # with warnings, the default I observe is that a specific warning only gets issued once; this same error is in the log each time
    >>>
    >>> sas.list_tables('x')
    [('3 BAD NAME', 'DATA'), ('A', 'DATA'), ('AF', 'DATA'), ('CARSFR', 'DATA'), ('CHARF', 'DATA'), ('PRDSALE', 'DATA')]
    >>> sas.list_tables('x')
    [('3 BAD NAME', 'DATA'), ('A', 'DATA'), ('AF', 'DATA'), ('CARSFR', 'DATA'), ('CHARF', 'DATA'), ('PRDSALE', 'DATA')]
    >>>
    >>> # and again, even though warnings didn't display a message, sas.check_error_log is set because there still was an ERROR in the log
    >>> sas.check_error_log
    True
    >>>
    >>>
    >>> # You can change the behavior to have the warning issued every time, or some number of times, or even make it throw an exception
    >>>
    >>> import warnings
    >>> warnings.filterwarnings("always",module='saspy')
    >>> sas.list_tables('x')
    /opt/tom/github/saspy/saspy/sasioiom.py:976: UserWarning: Noticed 'ERROR:' in LOG, you ought to take a look and see if there was a problem
      warnings.warn("Noticed 'ERROR:' in LOG, you ought to take a look and see if there was a problem")
    [('3 BAD NAME', 'DATA'), ('A', 'DATA'), ('AF', 'DATA'), ('CARSFR', 'DATA'), ('CHARF', 'DATA'), ('PRDSALE', 'DATA')]
    >>> sas.list_tables('x')
    /opt/tom/github/saspy/saspy/sasioiom.py:976: UserWarning: Noticed 'ERROR:' in LOG, you ought to take a look and see if there was a problem
      warnings.warn("Noticed 'ERROR:' in LOG, you ought to take a look and see if there was a problem")
    [('3 BAD NAME', 'DATA'), ('A', 'DATA'), ('AF', 'DATA'), ('CARSFR', 'DATA'), ('CHARF', 'DATA'), ('PRDSALE', 'DATA')]
    >>> sas.list_tables('x')
    /opt/tom/github/saspy/saspy/sasioiom.py:976: UserWarning: Noticed 'ERROR:' in LOG, you ought to take a look and see if there was a problem
      warnings.warn("Noticed 'ERROR:' in LOG, you ought to take a look and see if there was a problem")
    [('3 BAD NAME', 'DATA'), ('A', 'DATA'), ('AF', 'DATA'), ('CARSFR', 'DATA'), ('CHARF', 'DATA'), ('PRDSALE', 'DATA')]
    >>>
    >>>
    >>>
    >>> warnings.filterwarnings("error",module='saspy')
    >>> sas.list_tables('x')
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "/opt/tom/github/saspy/saspy/sasbase.py", line 2064, in list_tables
        ll = self._io.submit(code, results='text')
      File "/opt/tom/github/saspy/saspy/sasioiom.py", line 976, in submit
        warnings.warn("Noticed 'ERROR:' in LOG, you ought to take a look and see if there was a problem")
    UserWarning: Noticed 'ERROR:' in LOG, you ought to take a look and see if there was a problem
    >>> sas.list_tables('x')
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "/opt/tom/github/saspy/saspy/sasbase.py", line 2064, in list_tables
        ll = self._io.submit(code, results='text')
      File "/opt/tom/github/saspy/saspy/sasioiom.py", line 976, in submit
        warnings.warn("Noticed 'ERROR:' in LOG, you ought to take a look and see if there was a problem")
    UserWarning: Noticed 'ERROR:' in LOG, you ought to take a look and see if there was a problem
    >>>
    >>>
    >>> warnings.resetwarnings()


Hopefully you will find this enhancement useful. It would be great if each thing done in SAS returned a clean return code to check, but that's
not the case. So, checking the log is something that's necessary sometimes. Hopefully this warning when an ERROR is seen, will make this easier.

    
**************
Jupyter magics
**************
Jupyter Notebooks have what they call Magics, which let you submit code from a diferent language
than the kernel of the notebook, or provide other functionality. SASPy supports a few magics that
you can use if you are in a Jupyter Notebook. They simply allow you to submit explicit SAS code
from a cell. There is a submitLST() method on the SASsession object which does the same thing as the ``%%SAS``
magic, and it works in all Python (UIs, IDEs, command prompt, ...) interfaces. So, using it instead
of the magic makes your code run anywhere, not just in a Jupyter notebook, but you can use these if you like.

The magics that are available with the package enable you to bypass Python 
and submit programming statements to your SAS session.

The ``%%SAS`` magic enables you to submit the contents of a cell to your SAS
session. The cell magic executes the contents of the cell and returns any 
results. ::

  %%SAS
  proc print data=sashelp.class;
  run;

  data work.a;
    set sashelp.cars;
  run;

If you are also invoking ``saspy`` methods directly in other cells within the 
same notebook, you may indicate that a ``%%SAS`` cell should share the same 
SAS session by passing your existing session as a parameter.

In a prior cell in the notebook: ::

  import saspy
  my_session = saspy.SASsession()
  
  # sending a dataset to SAS as 'mydata'
  mydata = sas.df2sd(some_pandas_dataframe, 'mydata')

Then later, invoke a SAS cell and pass your existing session so that the remote data 
set is accessible: ::

  %%SAS my_session
  proc print data=work.mydata;
  run;

The ``%%IML`` magic enables you to submit the contents of a cell to your SAS
session for processing with PROC IML. The cell magic executes the contents
of the cell and returns any results. The PROC IML statement and the trailing
QUIT; statement are submitted automatically. ::

  %%IML
  a = I(6); * 6x6 identity matrix;
  b = j(5,5,0); *5x5 matrix of 0's;
  c = j(6,1); *6x1 column vector of 1's;
  d=diag({1 2 4});
  e=diag({1 2, 3 4});

The ``%%OPTMODEL`` magic enables you to submit the contents of a cell to your SAS
session for processing with PROC OPTMODEL. The cell magic executes the contents
of the cell and returns any results. The PROC OPTMODEL statement and the 
trailing QUIT; statement are submitted automatically. ::

  %%OPTMODEL
  /* declare variables */
  var choco >= 0, toffee >= 0;

  /* maximize objective function (profit) */
  maximize profit = 0.25*choco + 0.75*toffee;

  /* subject to constraints */
  con process1:    15*choco +40*toffee <= 27000;
  con process2:           56.25*toffee <= 27000;
  con process3: 18.75*choco            <= 27000;
  con process4:    12*choco +50*toffee <= 27000;
  /* solve LP using primal simplex solver */
  solve with lp / solver = primal_spx;
  /* display solution */
  print choco toffee;

