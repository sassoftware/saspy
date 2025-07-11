# Changelog


## [5.103.2] - 2025-07-11

### Added

-   `None` Nothing Added

### Changed

-   `None` Nothing Changed

### Fixed

-   `Fix` I broke download() in the HTTP access method with that last release! :( 2 days ago. Cut-n-paste error doing all
of those try: except: around the http calls. This is a one line fix to remove the read I accidently inserted. The problem
that resulted was not a failure, but rather 0 byte files after the 'successful' download.

### Removed

-   `None` Nothing removed



## [5.103.1] - 2025-07-08

### Added

-   `None` Nothing Added

### Changed

-   `Enhanced` The HTTP Access Method (for Viya) has some places where it has to make an HTTP call in a loop. There were
some of these where I was doing connect() and close() on the connection, inside the loop. Other places I wasn't. There's
no need to have those in the loops, so I removed that from the places it was doing those. I also changed upload from doing
'chunked' http transfer manually, to having it done by the http request call itself. I also added try/except aound all of
the http request calls that didn't have it, to handle unexpected failures better.

### Fixed

-   ` None` Nothing Fixed

### Removed

-   `None` Nothing removed



## [5.103.0] - 2025-04-15

### Added

-   `None` Nothing Added

### Changed

-   `Enhanced` The submit*() methods of the HTTP Access Method (for Viya) include a GETstatusDelay= option for delaying the
HTTP calls to see if the code is finished, which happen in a loop until done. Once done the LOG and LST can then be retrieved.
This was implemented as a sleep() call in the loop checking the status. I've found that the API call can take a wait= value such
that it is a synchronous call with a timeout. I've changed to provide the GETstatusDelay value to the API call instead of being a
sleep delay in the python code. This will improve this loop by eliminating excessive calls while at the same time being more
performant since wait= will return as soon as the job finishes, while sleep will sleep that whole time before making another
status call. I've changed the default value of GETstatusDelay from 0 to 30 seconds to take advantage of this functionality, so
it will be used by default. GETstatusDelay is no longer required to eliminate excessive http status calls, while returning as soon
as the code finishes.

### Fixed

-   ` None` Nothing Fixed

### Removed

-   `None` Nothing removed



## [5.102.2] - 2025-03-27

### Added

-   `None`  Nothing Added

### Changed

-   ` None ` Nothing Changed

### Fixed

-   `Fix` Issue #640 found an edge case in sd2df where a row was dropped for a missing value in a single column data set for IOM
and HTTP. STDIO didn't have the problem. Pandas read_csv required a column separator for that one case even though it didn't for
cases with more than one column, even for the last column. I fixed the stream of data being provided to pandas so it handled
this case.

### Removed

-   `None` Nothing removed



## [5.102.1] - 2025-02-28

### Added

-   `Enhancement` PR #635 was contributed by a new contributor @gregorywaynepower who enhanced the install instructions for installing
saspy from other package manages and enhanced the conda instructions as well. Appreciate it!

### Changed

-   ` None ` Nothing Changed

### Fixed

-   `Fix` Issue #634 was fixed in this release. The read_csv() and write_csv() methods generated a filename statement with double
quotes around the physical path. That's fine unless there are special characters that can be configused with marco variables; '&'
for instance. I fixed this to use single quotes which won't let the SAS parser think there are embedded marco variables to resolve
in the path specification.

### Removed

-   `None` Nothing removed

## New Contributors
* @gregorywaynepower  made their first contribution in https://github.com/sassoftware/saspy/pull/635



## [5.102.0] - 2025-02-07

### Added

-   `Enhancement` Per user request (#620) I've added a parameter to the Submit*() methods, `reset=` which
resets the LanguageService to an initial state with respect to token scanning; the default is False.

### Changed

-   ` Enhancement ` I've changed the method for acquiring the local IP address of the client for the
SSH access method (STDIO over SSH) from using nslookup to using a a socket connect/close (to the remote host)
to get the IP. This was a problem with internal systems that happened w/ a VPN application that no longer
registers client machines w/ DNS such that the previous method didn't resolve the hostname. This should
cause no changes or regressions.

### Fixed

-   `Fix` From another internal consumer, I've fixed a bug in the HTTP access method around interrupt
handling for submit*() methods. When processing a keyboard interrupt in submit, while waiting for the
code to complete, the user is prompted with choices to take; `C`ancel the submitted code, `Q`uit waiting
for the results, or ignore - continue to `W`ait. Cancel is a new feature in this access method, and for
the case where Prompt=False (in the configuration file), where there can be no prompting, Cancel is
the default for this interrupt. What has been changed/fixed is that in the case of Prompt=False and
this interrupt happening and Canceling the submitted statements, that interrupt was not then being
raised so the calling code (Prompt=False is used for non-interactive scripts) could catch that and do
what was needed from the application. For the interactive case where the prompt is displayed, there
is no change. So, for the case where Prompt=False and a keyboard interrupt (ctl-C) is taken in submit,
the statements are Canceled (no change with that), and the interrupt is percolated to the caller
(this is the change), instead of just returning.

### Removed

-   `None` Nothing removed


## [5.101.1] - 2024-12-20

### Added

-   `Enhancement` For an internal request to get around a VPN DNS problem, I've enhanced the way I try to get
the local IP address for the Python machine, when using the SSH access method to connect to a remote server.
So when the local machine isn't registered in DNS, this can get the local IP to use w/out requiring setting the
`localhost` key in your configuration. `localhost` will still be used if provided.

### Changed

-   `None` Nothing changed

### Fixed

-   `None` Nothing fixed

### Removed

-   `None` Nothing removed



## [5.101.0] - 2024-11-05

### Added

-   `Enhancement` For an internal request to get data set information, like date time created/modified, ...
I added a method on the SASdata object called `attrs` which returns a 1 row dataframe with each of the attributes
returned by the ATTRN and ATTRC functions. Mostly they are character or numeric, but the create/modified are
returned as timestamps. This provides an easy programmatic way to access any of these values.

### Changed

-   `None` Nothing changed

### Fixed

-   `None` Nothing fixed

### Removed

-   `None` Nothing removed



## [5.100.4] - 2024-10-28

### Added

-   `None` Nothing added

### Changed

-   `None` Nothing changed

### Fixed

-   `Tweak` This was from an internal reported issue. I noticed 2 places where I was submitting code internally where
I was missing the results='text' that I use for internal code submissions that don't need ODS results. For an unusual
(not user case) reason that was causing them a problem. There's no issue reported from the field for this, so just
cleaning up these 2 submits so they are the same as all of the others.

### Removed

-   `None` Nothing removed



## [5.100.3] - 2024-09-10

### Added

-   `Enhancement` I added the timestamp of when the SAS Session was started to the output when submitting the SASsession Object.
See `SASsession started` below:
```
>>> sas
Access Method         = IOM
SAS Config name       = iomj
SAS Config file       = /opt/tom/github/saspy/saspy/sascfg_personal.py
WORK Path             = /sastmp/SAS_work7AD4000A185A_tom64-7/SAS_workA74A000A185A_tom64-7/
SAS Version           = 9.04.01M8P01182023
SASPy Version         = 5.100.3
Teach me SAS          = False
Batch                 = False
Results               = Pandas
SAS Session Encoding  = utf-8
Python Encoding value = utf_8
SAS process Pid value = 661594
SASsession started    = Tue Sep 10 13:52:19 2024
```

### Changed

-   `None` Nothing changed

### Fixed

-   `Fix` From Issue #516, I reworked how SASPy looks through the SASLOG to see if there was an ERROR, to set the
SASsession attreibute, `sas.check_error_log`, to True. The usual 'ERROR:' that starts a line in the SASLOG sometimes
has line number/col number embedded in it, though that's not the usual case. I reworked all of the places looking for
ERROR: in the log to use a better regex expression that finds both that case and the other; for instance:
`ERROR 180-322: Statement is not valid or it is used out of proper order.`


### Removed

-   `None` Nothing removed



## [5.100.2] - 2024-07-30

### Added

-   `None` Nothing added

### Changed

-   `None` Nothing changed

### Fixed

-   `Fix` The user contributed method sd2pq() had a bug in that the signature had a default dictionary declared,
but that persists as an independent object, and the method conditionally assigns other key:values to it which
then persist, incorrectly, in subsequent calls. See issue 611 for details. This version fixes that by defaulting
to None in the signature and using a local variable to provide the actual defaults and other values.

-   `Fix` Per issue 612, I've added `parquet` as an optional requirement for the SASPy install, so pyarrow
can be conditionally installed if wanting to use the new user contributed sd2pq() method. I also wnt ahead and
added a conditional install for pandas, via `pandas`, since I never added that to the condition install list
and it's also not a requirement except for if using the sd2df() and df2sd() methods. This doesn't affect any
behavior.

### Removed

-   `None` Nothing removed



## [5.100.1] - 2024-07-17

### Added

-   `None` Nothing added

### Changed

-   `None` Nothing changed

### Fixed

-   `Fix` The HTTP authorization interfaces keep changing and an internal user found a code path that didn't
provide the expected behavior. In order to still support older versions of viya 3.x, which don't have the SASPy
client_id and only supported user/pw authentication (that's changed in more recent 3.5 versions), I had to use
a different internal client_id. However, that client id doesn't support all the things, specifically refresh token
in this case, that the SASPy client id supports. The path through authentication in saspy when using user/pw and
providing client_id didn't use the client id you provided, but rather used the old internal one. So, this fix
simply allows you to provide a client_id (`SASPy` or other), and user/pw as the means to connect. Authorization Code
authentication uses the SASPy id by default (which supports that) as well as with any client_id you provide, so it's
only the user/pw case with client_id being provided that had to be fixed; it now uses the client_id you said.
Until I no longer have to support the old Viya 3.x versions, you do need to specify client_id='SASPy' in order to
get the refresh token, which I do use to automatically refresh your auth token so you don't have it expire after 1
hour, which they changed it to recently.


### Removed

-   `None` Nothing removed



## [5.100.0] - 2024-07-10

### Added

-   `Enhancement` Per a user request. I've added support in the sd2df* methods for dealing with SAS dates and datetimes that
are out of range of Pandas Timestamps (pandas.Timestamp.min, pandas.Timestamp.max). These values will be converted to NaT
in the dataframe. The new feature is to specify a Timestamp value (str(Timestamp)) for the high value and/or low values
(tsmin=, tsmax=) to use to replace Nat's with in the dataframe. This works for both SAS datetime and date values.
For instance, given a SASdata object: sd.to_df(tsmin='1966-01-03 00:00:00.000000', tsmax='1966-01-03 23:59:59.111111')


### Changed

-   `None` Nothing changed

### Fixed

-   `None` Nothing fixed

### Removed

-   `None` Nothing removed

### Note

- This is just a note to acknowledge that the minor version jumped from 15 to 100. What that about!?
Well, glad you asked ;) This is the 100th release of SASPy, in under its almost 10 years in existence. So, I just
thought I'd skip a few minor releases to identify the milestone. It's been a privilege to have created and supported
SASPy this whole time, and to have helped and supported all of our users who use it!
Tom


## [5.15.0] - 2024-06-27

### Added

-   `Enhancement` A user contributed method `sasdata2parquet` (sd2pq), which is like sasdata2dataframe, but for data too
big to fit in a Pandas DataFrame (not enough memory). This method streams the data over, like sd2df but it writes the data
out as parquet file(s) so that it can then be access in Python by Arrow. It was designed specifically for the users use case,
but it can be used for simple situations as well. There are a lot of parameters, but most default so they aren't needed. It
can be called as simply as:  sas.sasdata2parquet('parquet_file','cars','sashelp'). Se the API doc for more.

### Changed

-   `Deprecated` In version 5.13.0, the JWT authentication mechanism for the HTTP Access Method (Viya) was being deprecated,
so a warning message about that was added to the code path. It turns out that this is being deprecated only for connecting to
Viya using the default SASPy client_id. If however, you have created your own client_id that can use Azure JWT's to connect, then
you can continue to connect and authenticate with the JWT mechanism by providing that client_id, along with the client_secret
and the jwt to SASPy. Those are all existing configuration keys that have been there since before had an internal client id that it
defaults to.

### Fixed

-   `None` Nothing fixed

### Removed

-   `None` Nothing removed



## [5.14.0] - 2024-06-14

### Added

-   `None` Nothing added

### Changed

-   `Enhancement` Per a user request (see issue #603 for details), in the HTTP and IOM access methods, there is
now a new boolean parameter `loglines` on the submit() method which changes how the LOG is returned. Of course the
default is Fslse to preserve current behavior. The user wanted a list of dictionaries for each line of the log, which
is returned from both the HTTP and IOM API's. The dictionaries have the `line`, which has the LOG contents for that
line, and the `type` which contains identifiers like NOTE, WARRNING, ERROR, TITLE, SOURCE ... See the Issue for
details of what to output is like for each of the access methods, as the API's don't return identical information.
The STDIO (SSH) access method can't return this as there is no API for that.


### Fixed

-   `None` Nothing fixed

### Removed

-   `None` Nothing removed



## [5.13.0] - 2024-05-16

### Added

-   `None` Nothing added

### Changed

-   `Enhancement` In the HTTP access method, the upload method may encounter an error from the server when the file being uploaded
is bigger that is allowed by the server. This previously resulted in an unclear failure. I now catch this and throw a clear exception.

### Fixed

-   `Fixed` A bug was found with the append method of the SASdata object. When appending a Dataframe, the method uses df2sd to
transfer the data to SAS to then proc append it. After, it deletes that SASdata set it created. The method also allows you to
provide a SASdata object to append, but it didn't check and deletes that SASdata set too. That should not have been happening.
This is fixed in this release and only deletes the data set if it was temporarily created from the Dataframe.

### Removed

-   `Deprecated` A new requirement from Viya 4 is to deprecate the Azure JWT Authentication mechanism for SASPy. In a future
version of Viya this will no longer work. I've added this to the doc and issue a warning when trying to use this, in this release.
Support for this will be removed in a future release.




## [5.12.0] - 2024-04-18

### Added

-   `None` Nothing added

### Changed

-   `Enhancement` A new requirement in Viya 4 called for a change in the SSO authentication mechanism, to support PKCE. So this
release provides support for that. There's nothing you have to do, but you will see a different message about the URL you need
to use to get an auth code to provide, when using that authentication mechanism. In short, every time you want to authenticate,
you get a new URL (it has its own unique code in it). This is displayed in the log same as the previous URL was, but unlike
previously, where the url was the same every time for the deployment, and you could already get a code and provide it to SASsession(),
this is a unique URL every time. So you can't get an authcode ahead of time. Don't fuss at me, I don't like it either. If you need
help, open an issue and I'll see what I can do.

### Fixed

-   `None` Nothing fixed

### Removed

-   `None` Nothing removed


## [5.11.0] - 2024-04-16

### Added

-   `Enhancement` Per internal tester request, I've added an option for the STDIO access method to provide an amount of time for
SAS to terminate before killing the process, in the endsas() method. I've always waited up to 5 seconds from the subprocess
to terminate after requesting SAS shutdown, which is normally fine. If it takes longer, I kill the process. In this case,
SAS runs with some internal testing options which causes processing at termination, and takes longer than 5 seconds. So I've
added an option to allow me to wait longer before terminating the process which will allow this extra termination processing
to complete. This isn't a usual option customers would set, but it's there either way. The option is `termwait` and it takes an
integer number of seconds. In this case, the config def required: `'termwait':  60,` to get it to work as expected.

### Changed

-   `None` Nothing changed

### Fixed

-   `None` Nothing fixed

### Removed

-   `None` Nothing removed




## [5.10.0] - 2024-04-09

### Added

-   `None` Nothing added

### Changed

-   `None` Nothing changed

### Fixed

-   `None` Nothing fixed

### Removed

-   `Enhancement` Per user request, I've added the ability to request a keepalive thread in the IOM access method.
I added this in V5.9.0, but then found that this could deadlock the IOM access method if the keepalive thread executed while in the middle
of one of my SASPy methods; which I didn't think would be the case, but I didn't happen to have it happen. When it
does, it can deadlock everything. So, I'm removing this feature with this release. It just doesn't work as expected.



## [5.9.0] - 2024-04-08

### Added

-   `None` Nothing added

### Changed

-   `Enhancement` Per user request, I've added the ability to request a keepalive thread in the IOM access method.
The workspace server has a timeout option (defined in metadata), which usually defaults to 60 minutes. If no interaction
happens in that amount of time since the last interaction, the Workspace server will terminate itself. I've added an
option `keepalive` for the IOM access method that can be defined in the Configuration Definition or on SASsession(keepalive=50) to
specify you want this thread created and how many minutes in between interactions. So, if you're Workspace server has
a timeout of 60 min, you can specify `'keepalive' : 50,` in your config def to have saspy send a request every 50 min
so the timeout doesn't happen, and keep your session connected until you terminate it. The default is, of course, the
current behavior which is no keepalive thread.


### Fixed

-   `None` Nothing fixed

### Removed

-   `None` Nothing removed



## [5.7.0] - 2024-03-19

### Added

-   `None` Nothing added

### Changed

-   `Enhancement` Per user request, I've added the ability to CANCEL submit()'ed code in both the IOM and HTTP
access methods. Until now you would see a message like the following if you tried to interrupt a submit:
`SAS attention handling is not yet supported over IOM. Please enter (T) to terminate SAS or (C) to continue.`
But now, with the ability to cancel long running code, you will see something like this instead:
`Please enter (T) to Terminate SAS or (C) to Cancel submitted code or (W) continue to Wait.`
If you choose 'C' then I can now use the API to tell the server to terminate whatever was being executed and
come back immediately, so you can then run other code. Also, for IOM, I cancel any code in endsas() so that the
workspace server terminates immediately instead of only after whatever is running finishes.


### Fixed

-   `None` Nothing fixed

### Removed

-   `None` Nothing removed




## [5.6.0] - 2024-02-05

### Added

-   `None` Nothing added

### Changed

-   `Enhancement` Per user request, I've added the ability to have the SASLOG returned from the submit methods
be HTML with ERROR:, WARNING: and NOTE: lines colorized like in other SAS UI's. This is how the SAS_Kernel for
Jupyter colors it's LOG and how the log returned in the SAS_Results object in SASPy colors that log too. This
feature requires the Pygments package, so it is only available if that package in installed, else you get the
current behavior. The new `colorLOG` configuration key is how to set this. It's a boolean and defaults to False;
existing behavior. It can be specified in the Configuration Definition or on SASsession, like any other key.

### Fixed

-   `None` Nothing fixed

### Removed

-   `None` Nothing removed




## [5.5.0] - 2024-01-09

### Added

-   `None` Nothing added

### Changed

-   `Tweak` A user contribution enhanced an error case where parsing an empty log due to the SAS session
being terminated returned a less than helpful error in the exception. This now would return a clear error
as to the problem.


-   `Enhancement` Regarding a SAS process unexpectedly terminating out from under SASPy, you may have seen this or a similar
error message before: "No SAS process attached. SAS process has terminated unexpectedly." along with an arbitrary exception.
I've enhanced this case, like many other situations to now throw a new exception, SASIOConnectionTerminated, and to log the
message(s) previously returned (logger.fatal()). This should really have always been an exception as it is a fatal case where
the SAS session is no longer functional, since there's no SAS process connected anymore.


### Fixed

-   `None` Nothing fixed

### Removed

-   `None` Nothing removed



## [5.4.4] - 2023-11-02

### Added

-   `None` Nothing added

### Changed

-   `Tweak` Databricks finally enabled IPython support which allows for HTML rendering from w/in SASPy,
like in both Jupyter and Zeppelin (Zeppelin has its own rendering, but SASPy supports it). So now
display='databricks' will just use the same code as display='jupyter' so HTML can finally be rendered
for you by SASPy instead of having to run batch mode to get the HTML returned to you and then you having
to pass it to their displayHTML() method.

### Fixed

-   `None` Nothing fixed

### Removed

-   `None` Nothing removed



## [5.4.3] - 2023-10-27

### Added

-   `None` Nothing added

### Changed

-   `None` Nothing changed

### Fixed

-   `Fixed` The upload method wasn't validating that the file was uploaded successfully after the fact.
It has a number of checks up front, and if there's a failure, it could return Success=False, but each
access method is different and they didn't each get a failure the same way. So I added a more explicit
validation after the upload is completed, to prove the file really made it or not. For the HTTP access
method, I also mitigated a situation where the Compute server process could be killed for trying to
access a restricted path. Now that just gets a clean failure with a message about the problem.

### Removed

-   `None` Nothing removed



## [5.4.2] - 2023-10-18

### Added

-   `None` Nothing added

### Changed

-   `None` Nothing changed

### Fixed

-   `Fixed` Found a SAS code gen syntax error in the HTTP access method causing an error in the log
for sd2df. Needed to quote the fileref in a function. So, fixed that syntax error in that method.

### Removed

-   `None` Nothing removed



## [5.4.1] - 2023-10-06

### Added

-   `None` Nothing added

### Changed

-   `Tweak` Added to the doc for the HTTP access method, adding the 'refreshtoken' keyword which goes along with the
'authtoken' keyword if you did your own authentication to SASLogon. Refreshtoken was added when authtoken was, I just
didn't get it in the doc then.

### Fixed

-   `Fixed` Based upon Issue 562, I enhanced sd2df() to allow you to provide 'errors=' as a keyword parameter which is
used in the decode() method when converting the bytes being streamed across to characters. The errors keyword determines
how transcoding failures are handled; the default being failure. See bytes.decode() in the Python doc for valid values.

### Removed

-   `None` Nothing removed



## [5.4.0] - 2023-09-27

### Added

-   `None` Nothing added

### Changed

-   `Tweak` Changed the doc for saslib() to show how to deassign a libref using this method, as well
as how it's already doc'ed for assigning librefs. Nothing changed with the method, just documenting how to use
it for both assign and deassign.

### Fixed

-   `Fixed` An internal user found a bug with sd2df() where it was converting character variables values of
'NA' in the SAS Data Set to NaN in the dataframe instead of them being the string 'NA'. This turned out to
be due to the interaction of the na_values={...} dictionary I pass in, since I need to normalize the 30ish
different MISSING Values that SAS has, to individual values to provide Pandas so they are processed correctly.
The problem, however, is that the default value of keep_default_na= being True, appends my list to Pandas
list of what it thinks values are for NaN's instead of only using my list. The file is to specify keep_default_na=True
as well as provide my list via na_values={...}. That is fixed in this release.

### Removed

-   `None` Nothing removed



## [5.3.0] - 2023-08-29

### Added

-   `None` Nothing added

### Changed

-   `Tweak` Changed the value of Context in the HTTP config definitions in the example sascfg.py file to use
the more likely `SAS Studio compute context`. This has no effect on any code. It's just an example configuration.

-   `Enhanced` df2sd() now raises an exception (SASDFNamesToLongError) if any of the column names are longer than 32 bytes,
in the SAS Session encoding, since the data step will fail for those columns and produce errors in the log, but SAS still create
the SAS Data set, incorrectly. Previously, df2sd returned the SASData object, and issued a message about finding Errors in the log,
but didn't fail. The resultant SAS Data Set wasn't correct so checking for this and raising the exception is what should happen.
I also write a message with each column name that is too long, so you know which one(s) need to be changed. And remember, SAS's
restriction on these names is 32 bytes in the SAS Session encoding, and not necessarily 32 characters of utf-8 from Python.

### Fixed

-   `Fixed` I found a bug in the code that parses the authinfo file to find the authkey. It was using startswith(authkey)
to find the line to use, for the user and password. But startswith() isn't looking at the first word, only so many characters.
This could result in using the wrong line from the authinfo file. For instance, if you had a line with the authkey of `tom1` and
another line further in the file with authkey of `tom`, then looking for authkey='tom' would use the first line with `tom1` for the
credentials instead of the correct line starting with `tom`. Simple fix to parse it correctly so it compares the whole first
word of the line now.

### Removed

-   `None` Nothing removed



## [5.2.3] - 2023-07-28

### Added

-   `None` Nothing added

### Changed

-   `Tweak` Cleaned up a few bit of documentation. Fixed a link in one section. Nothing significant or different.

-   `Tweak` I moved a couple methods out of the individual Access Method modules and into the base module.
Over time, I had been able to make these be the same code in each access method, so now it's cleaner to have
the single implementation in one place instead of 4 places. No changes are required in user code.

-   `Tweak` Modified a lookup in the HTTP access method to be more specific, in case something changes in the
API over time. Just getting a link from the list returned by Compute. Nothing changing from users perspective.

-   `Tweak` Added some instructions to a couple of SASsession Exceptions to point users at the documentation.
Added messages pointing to the Configuration Doc, the Troubleshooting Guide in the doc and a message to open
an Issue on the saspy github site if needing more help.

### Fixed

-   `None` Nothing fixed in this release.

### Removed

-   `None` Nothing removed



## [5.2.2] - 2023-07-07

### Added

-   `None` Nothing added

### Changed

-   `Tweak` Cleaned up a few bit of documentation. Nothing significant or different.

### Fixed

-   `Fixed` Some time ago, when the Python process terminated (normally), my __del__ methods on SASsession
objects would be called, and I would cleanly terminate the SAS process that was attached. That isn't behaving
as it used to, at least with the HTTP access method for Viya. So, I've added code to explicitly register
a termination exit routing where I then call my cleanup, and that now is behaving as expected for all three
access methods. The SAS process is cleanly terminated before Python finally terminates. So, this is working
as it used to again.

### Removed

-   `None` Nothing removed



## [5.2.1] - 2023-05-31

### Added

-   `None` Nothing added

### Changed

-   `None` Nothing changed

### Fixed

-   `Fixed` A bug was found in df2sd where having a variable of all blanks caused errors in the data step
being used to read in the data. An empty or missing var is handled, but a multibyte blank string wasn't being
handled the same, required, way. This release fixes that bug in all three access methods.

### Removed

-   `None` Nothing removed



## [5.2.0] - 2023-05-30

### Added

-   `None` Nothing added

### Changed

-   `Enhancement` Added support for Proxy Authentication using user/pw. Support for having a proxy server ahead
of Viya was added in version 4.5.0, and in this release, support for authenticating to that proxy with user/pw
was added based upon a user request. This is documented in the HTTP section of the Configuration documentation.

### Fixed

-   `Fixed` A minor fix for a case where a unit test was producing a resource warning. I couldn't reproduce this,
but the fix was trivial and it fixed the users case. This was for issue 543.

-   `Fixed` A fix in the STDIO access method to explicitly use 'localhost' in the filename statement generated for
dataframe2sasdata() instead of using blank hostname. This was causing an issue for a user with multiple network
adapters and an unusual configuration. Explicitly using localhost is the correct path for this since SAS and Python
are on the same machine, so using the loopback adapter is the right choice.

### Removed

-   `None` Nothing removed



## [5.1.2] - 2023-04-28

### Added

-   `None` Nothing added

### Changed

-   `Tweak` I adjusted the doc regarding the classpath and the encryption jars; separating the two so that
it was more obvious and so that I could point to the more specific section depending upon the question.

### Fixed

-   `Fixed` Issue 541 showed a deadlock situation in the STDIO Access Method when the generated code for a
sd2df() call was long enough to block python trying to write that to STDIN because SAS was blocked writing
it out to the LOG, STDERR. So I addressed this so that the deadlock won't happen anymore. This requires no
code changes on your part.

### Removed

-   `None` Nothing removed




## [5.1.0] - 2023-04-14

### Added

-   `Enhancement` Viya has been evolving since I first introduced the HTTP Access Method to connect to SAS
w/in Viya (SAS Compute Server). The current versions are configured with TLS (SSL) by default, and there are
different ways the system can be configured for this. SASPy uses the Public REST API to interact with Viya.
This means HTTPS communication and than means CA Certificates both server side and client side. The best approach
with the latest Viya is to configure it with your companies CA Certificates that are already in use on your clients.
But, if using Viya generated certificates, then these need to be distributed and installed in the right places on
all client machines (that'sa easier said than done). For this case, I've added a new Configuration Definition key,
`cafile`, which can be used to specify the location of the Viya Certificate bundle (the path to that .pem file),
so that HTTP from python will use this certificate to create a Trusted connection. This access method has had the
`verify` key to control whether the connection is to be verified or not (Trusted). With Verify set to True, it now
fails if the connection cannot be verified. If False it doesn't try to create a verified connection, same as before.
The default it still to try and if not verifiable, fall back to unverified; same as it has been, since the original
Viya certificates were not CA Verifiable.

### Changed

-   `Tweak` Update readme and correct typo by @BrokenStreetlight in https://github.com/sassoftware/saspy/pull/538

### Fixed

-   `None` Nothing fixed

### Removed

-   `None` Nothing removed

## New Contributors
* @BrokenStreetlight made their first contribution in https://github.com/sassoftware/saspy/pull/538



## [5.0.2] - 2023-03-10

### Added

-   `None` Nothing added


### Changed

-   `Enhanced` The latest versions of Pip complain that setup.py is being deprecated and that using a pyproject.toml
file (still in conjunction with a setup.py, if you like) is the soon to be required means of building a Python Package.
This release of SASPy has a minimum pyproject.toml file which seems to be acceptable to Pip. I'm creating this release
to see if the whole process, from PyPI to conda-forge all work with this change; thus this is the only change. If all
works well, then great. If not, I'll scrap this and see what else is needed. Obviously I've tested this out and it works,
other than seeing if PiPI and conda-forge have any issue; have to run it through those to see what comes out. I expect
there to be no issue, but let's see. Well, v5.0.1 didn't build right for pypi, so take 2 with 5.0.2.


### Fixed

-   `None` Nothing fixed


### Removed

-   `None` Nothing removed




## [5.0.0] - 2023-02-28

### Added

-   `None` Nothing added


### Changed

-   `BREAK` This is a breaking change, thus the incrementation of the major digit of the Sematic Version.

The analytic methods (which are really SAS Procs) return any number of results; they produce tables, graphs, plots,
... All of these results are (supposed to be) returned in the SASResults object. This object is implemented by having
the proc code executed in a way that writes all output to an ODS Document. That is an Itemstore file created by SAS.
It's like a blob store with an internal directory structure. There is also a libname engine that can access these
stores, at the directory level. The proc generation code and the implementation of the SASResults object use the
concatenation of all of the directories in the ODS document to access and return the various outputs from the
procedure. Unfortunately, the original implementation of this never took into account the fact that many procs
produce the same set of tables/plots/... for multiple criteria. The names of these objects are the same in each set,
but stored in the document under different directories. A side effect of this is that accessing these through the
concatenated libref only sees, and can only access, the first of occurrence of these same named members. That means
that much of the actual output from these procs has NOT been returned and is NOT accessible from the SASResults
object.

To address this, I've had to learn how all of this works (this is the one part of saspy I didn't write), and rework
how the SASResults object is implemented, including some overly complicated traversal and renaming of these members
in the Document so that they can be returned and accessed via the SASResults object. Now all of the tables/plots/...
will be returned and can be accessed. The change is that now the names of these members are comprised of their
original names and part of the directory structure names (being limited to 32 chars) such that they can be easily
identified as the results for the appropriate criteria.

So, clearly, this is a breaking change for the cases where there were missing results and now the names of the
results have been changed to allow the other missing results to be available. For member names that had no duplicate
missing members, their names are not changed by this. That means that there are cases where this fix does not break
any code; if you had hard coded names of the SASResults list of results. So, new members that had been missing
previously will now be available when they hadn't previously. While names that didn't have missing duplicates won't
change. So the only thing you have to do to your programs, is adjust the name of a result you're trying to access
when that member has duplicates; as all of those members are renamed with the new algorithm. Remember, you get the
list of results by executing `dir(SASResults_object)`.

Hopefully fixing this to return the correct results is worth any code that has to be adjusted. I consider this to
have been wrong to begin with, and so making it right outweighs my aversion to introducing a breaking change.


-   `BREAK` This is a breaking change, thus the incrementation of the major digit of the Sematic Version.
The SASml method `hpcluster` is renamed to be the correct Proc name of `hpclus`, There is no proc named hpcluster
and this being named wrong caused issues with the test cases, and there was a special check in the code to catch
this name and change it to be the correct proc name. So, since this release is already a breaking change to fix
the SASResults for all of the procs, I figured it would be a good time to fix this one wrongly named proc/method.
If you use `hpcluster` in your SASPy code, I'm afraid you'll need to delete the `ter` from it to address this change.


### Fixed

-   `Fixed` Fixed a number of problems in the test suits for the analytic procs. There were a number of test cases that
failed and now pass correctly. There were Viya procs that never ran, even when connected to a Viya deployment. These
previously failed regardless, and now they run and pass when connected to Viya. None of this affects user code, it's
just cleaning up the test ware having to do with these Procs (analytic methods).

This also includes re-benching all of the test cases where there were missing results. These all now have all of the
results being returned and the tests now validate all of the correct results.


### Removed

-   `None` Nothing removed




## [4.7.0] - 2023-02-08

### Added

-   `None` Nothing added


### Changed

-   `Enhanced` The `estimate` statement in at least some procs is allowed to be specified more than once, unlike most proc statements.
There was previously no support for generating a given statement more than once. Estimate= now allows a list of strings and will generate
an estimate statement for each string in the list.


### Fixed

-   `Fixed` symget(name) returns `&name` if the marco isn't defined, which is what SAS prints out. So  I fixed symget to issue symexist
first and if not defined issue a warning and return None, which is what it should have been doing all along.


### Removed

-   `None` Nothing removed



## [4.6.0] - 2023-02-01

### Added

-   `Added` @dmsenter89 added support for Proc MI in the SASStat package. Also, added tests for this in the Stat testing file.


### Changed

-   `Enhanced` Made a significant performance improvement in the IOM Access Method with reading the log back from the SAS session.

-   `Enhanced` @ShuguangSun enhanced the run_sas script to support executing multiple scripts in one call


### Fixed

-   `Fixed` @dmsenter89 Fixed a number of things with Proc code generation for methods in the SASStat package and some minor things for all
analytic methods. Fixed statements for Proc Factor.

-   `Fixed` @dmsenter89 Fixed a number of things in the Stat testing file.


### Removed

-   `None` Nothing removed



## [4.5.0] - 2023-01-12

### Added

-   `Enhanced` Added support in the HTTP Access Method for if there's a proxy server set up to get to the actual Viya deployment.
There's a new `proxy` keyword in the config used to provide 'host:port' of the proxy.'

### Changed

-   `None` Nothing changed


### Fixed

-   `None` Nothing fixed


### Removed

-   `None` Nothing removed



## [4.4.3] - 2022-12-23

### Added

-   `None` Nothing added


### Changed

-   `None` Nothing changed


### Fixed

-   `Fix` The changes for the last release caused one issue w/ unverifiable certificates, where the error isn't
thrown when the connection is created, needed to add a connect() call at that time to catch the error; that was happening
before, in a call I moved till later, which is why the error wasn't being caught on the creation where I was checking for it.
Again, no coding chages for anyone, just made it throw the error where I was checjing for it.


### Removed

-   `None` Nothing removed



## [4.4.2] - 2022-12-23

### Added

-   `None` Nothing added


### Changed

-   `None` Nothing changed


### Fixed

-   `Fix` I caused a regression with Viya 3.5 from having to rework authentication due to chages in
Viya 4. This fixes that and requires no coding changes. This fixes issue #500


-   `Fix` I fixed another issue with the same reworking as above that presented in another specific
case. This fixes that and requires no coding changes. This fixes issue #503


### Removed

-   `None` Nothing removed





## [4.4.1] - 2022-12-01

### Added

-   `Enhanced` I added a number of security type enhancements to the repo; none of which has to do with
how the code works, and requires no code changes. This was all based upon OpenSSF best practices for
Cybersecurity regarding open source repos. You can see the new badge on the home page: in the README.


### Changed

-   `None` Nothing changed


### Fixed

-   `Fix` I made a fix to the IOM access method based upon a vulnerability scan from the newly added SAST
tool that was part of the Security based enhancements added to the repo. This requires no code changes.


-   `Fix` I made a fix for the SAS_kernel, which depends upon SASPY to do the work interacting with SAS.
There was a breaking change in the Kernel interface regarding prompting. I fixed it so it still works
with previous versions (of course; no breaking changes for my customers!), as well as with the new api.
This fix addresses SAS_kernel issue https://github.com/sassoftware/sas_kernel/issues/83


### Removed

-   `None` Nothing removed



## [4.4.0] - 2022-11-14

### Added

-   `Enhanced` @rayewright added a half dozen more ML procs to the sasViyaML package for Viya.


### Changed

-   `Enhanced` Added documentation specifically identifying datatype conversions between SAS data Sets
and Pandas dataframes; both directions. This was added in the AdvancedTopics section of the doc and the other
couple parts of that section also about data movement were moved to all be contiguous and thus make all more
clear. No code changes, just documentation.

-   `Enhanced` Added documentation for the IOM access method regarding authentication. The Configurations
section already specifies how to authenticate with different means, but now there's a part of the doc explicitly
identifying which methods are supported and the one method that is not supported; SAS Token Authentication.

-   `Enhanced` @andyjessen cleaned up some links in the doc that were still referring to master instead of main
for the branch they linked to.

-   `Enhanced` The HTTP access method, to Viya, requires a valid authentication token be passes to every request.
This token is acquired when calling SASsession(). This token had been set to expire after 10 hours. Viya has been changed
to have these tokens expire after 1 hour, so to keep this from causing problems for SASPy sessions, which can be
interactive and last much longer than one hour, I've added support to reauthenticate and get a new authtoken prior
to the current one expiring. This happens as long as the SASsession object is valid and connected. There are no coding
changes required in user code. This should all just happen under the covers with no requirements on the user or program.
I did add a method for explicitly refreshing the authtoken, but that should not be required at any time. But, it may
be of use as a diagnostic in the field if there are ever issues reauthenticating. So, again, no code changes required.


### Fixed

-   `None` Nothing fixed


### Removed

-   `None` Nothing removed



## [4.3.5] - 2022-10-17

### Added

-   `None` Nothing Added


### Changed

-   `Tweak` Had a PR with fixes to Doc; mostly typos and consistent use of terms. Also fixed a broken link.


### Fixed

-   `Fix` Fix for leaked resources. The pipes that are created between subprocess and Python were not being
released prior to subtask termination. This results in a resource leak that is identified when running with
settings that report these issues. I clean this up in both the IOM and STDIO access methods, they each had
similar concerns. No programming changes required.


-   `Fix` Fix for issue 487 where, in the df2sd() method, there was data that contained the data step
termination string which resulted in the data step, which was retrieving the data and writing it to the SAS
data step, terminating prior to processing all of the data and then SAS would take the rest of the stream
as SAS code, which fails miserably and consumes memory with all of the errors going to the log. It also
terminates the connection to the client. I've also added code in the java client to catch this kind of
failure so it wouldn't hang, like it was. So this is addressed and fixed in this release, and requires no
programming changes.


### Removed

-   `None` Nothing removed



## [4.3.4] - 2022-10-05

### Added

-   `None` Nothing Added


### Changed

-   `Tweak` I'm moving to a newer dev environment; newer OS version, newer Python version, and all the newer modules, ...
Using Sphinx to build the doc fails with this newer version, so I've had to tweak and reworks things to get the doc to build
with this newer version of evrerything. So, there were a lot of minor adjustments pushed to accomodate this. It's all working
and, of course, requires no programming changes due to any of this. A plus is that now the index, shown on the left side of the
page, finally has links to the individual methods, in the API section of the doc! This is a welcome enhancement.


### Fixed

-   `Fix` Fix for issue 480 was in the last version. That issue was a discrepency with how Python on MacOS works compared to
any other operating system. I've had to implement workarounds for Mac Python for a number of issues in the past. This release
has a couple more workarouds for problems with the Mac version of Python too. These are in the IOM access method, whereas the
last versions fix was in the STDIO access method. Again, no programming changes required.

-   `Fix` All of the analytic methods correspond to some SAS Procedure. Each method is one analytic PROC. The code that generates
the PROC syntax for all of tese methods is a bit convoluted. While fixing the method signatures for the doc building issues,
last release, I noticed that if the USER librfer is assigned, then none of the analytic method work. I've worked through that code
to resolve this, so in this release, that problem is fixed and they all work as they should have regardless of is USER is assigned
or not.


### Removed

-   `None` Nothing removed




## [4.3.3] - 2022-09-26

### Added

-   `None` Nothing Added

### Changed

-   `Tweak` The analytic methods all take a SASdata object, or the name of a SAS dataset (str). The method signatures used
['SASdata', str] to represent either/or, not a list. The current Spinx doc build no longer allows that and doesn't generate
signatures, so I hade to replace the [] with (). No programming changes, just a tweak to get the doc to build right with the
newer version of Spinx.

### Fixed

-   `Fix` Fix for issue 480. No programming changes required.

### Removed

-   `None` Nothing removed




## [4.3.2] - 2022-08-12

### Added

-   `Enhanced` Added another configuration key in the SAS_config_options dictionary for providing an override for the ODS type.
This was already available tochenge as an attribute on the SASSession object, but in a SAS_Kernel notebook, there was no
way to do that. So I added `style` to the config so it could be set when using SAS_Kernel in Jupyter.

### Changed

-   `Tweak` There are a number of methods which require querying SAS for information which is returned in the LOG and then
parsed out by SASPy. If there's something wrong on the SAS side and somehow the information isn't in the LOG, it can cause
exceptions in the method. I've added code to catch these exceptions and just handle them like an error so processing can
continue. The methods will now just fail and you can look at the log to see what the problem was.

### Fixed

-   `Fix` There were a couple methods on the SASdata object which, when returning Pandas results, didn't specify the
work library explicitly on the retrieval step. So if there was a user libref assigned, it would look there instead of
work for the data and not find it. All better now.

-   `Fix` In the IOM Access Method, the Java IOM Client code does some of the transcoding between Unicode and whatever the
SAS Session Encoding is. If there is a transcode failure, it throws an exception which terminates the Java process and the
SAS server process. I added code to catch this trye of failure, in my Java code, and return the failure, keeping the Java
and SAS processes (and SASPy) going. I don't have a way to change the behavior of the client code, so catching this and
keeping things running are what I can do, which is better than it all terminating out from under SASPy.

-   `Fix` And the big fix for this release is for df2sd() and sd2df(), fixing problems when the record length is larger
than the max (32767) for the _infile_ statement, which is used in the SAS code for these methods. This caused problems in
df2sd() if the row length was larger than 32767. There was also an issue that could be hit w/ regards to this in sd2df()
also, so that's addressed with this fix to. This is for all 3 access methods; STDIO, IOM and HTTP.

### Removed

-   `None` Nothing removed




## [4.3.1] - 2022-07-06

### Added

-   `Tweak` Thanks to our graphics design dept for creating a cool logo for SASPy! I added the graphic to the main repo
page (in the readme), and to the saspy-examples repo and to the documentation page. This has nothing to do with the code
or functionality; just a cool logo for SASPy!

### Changed

-   `Tweak` Changed the prompt in the IOM access method which asks for userid/pw to use 'OMR' instead of 'IOM' since the
configuration keys for user/pw are omruser/omrpw not iomuser/iompw. This has no effect on the code or processing, just
changing the text of the message to better correlate with the right acronym.

-   `Tweak` Made a change in the java IOM client code for upload/download to propagate and return the error if there was
a failure during the data transfer phase. Never seen this case happen before, but if it does it should be more clear.

### Fixed

-   `Fix` Added a check in the HTTP access method in upload and download to see if the status for the HTTP call was an error
and return the failure. Previously it didn't check and just returned success.

-   `Fix` Made a change in the HTTP access method's download method to read/write chunks of the data instead of the whole
file to keep from running out of, or using excess, memory in the Python process.

### Removed

-   `None` Nothing removed




## [4.3.0] - 2022-05-17

### Added

-   `New` Per a user request, I added the ability to use sshpass with the STDIO over SSH access method.
This allows you to authenticate with user/pw instead of having to use rsa keys (passwordless shh). There
are now two new keys (see the doc) for providing the path to the sshpass executable and the parameters to use.
The ssh key and other keys for this configuration stay the same.

### Changed

-   `Enhanced` The sd2df methods require multiple interactions (code submissions) to the SAS server and if any of these
intermediate steps fail or have some issue, then the method invocation fails. But, I wasn't catching these intermediate
problems which could cause non-obvious exceptions and tracebacks which were confusing. I've added code to catch failures
for these intermediate steps and throw a more clear exception if that happens. Nothing about how the methods works has
changed, just better error handling.

-   `Enhanced` The code that checks for an 'ERROR:' in the log and issues a warning to alert you to look to see what the
error was, wasn't only looking for it to start in column 1 of the log. So, it could pick up 'ERROR:' in a comment in the
code or anywhere in the log. I've enhanced this to limit false positives by only flagging 'ERROR:' starting in the first
column of the LOG.

-   `Tweak` Fixed a typo in an error message.

### Fixed

-   `Fix` The COM Access Method had a bug where the `encoding` was being used to transcode HTML results returned to
SASPy when it shouldn't, since the HTML results are already utf-8. Other code paths retrieving data from SAS did need to
use the provided encoding for transcoding from SAS Session encoding to utf-8. So, this one path was changed to not try to
transcode the HTML results. This was a fix for issue 454.

### Removed

-   `None` Nothing removed




## [4.2.0] - 2022-03-22

### Added

-   `None` Nothing Added

### Changed

-   `Tweak` If the initial connection to SAS (a SASsession) fails then there will be a failure error provided, but there
is also an exception thrown in subsequent code, trying to submit some of the initial code to gather info about the
session. This was subordinate and inconsequential, yet was confusing and needed to be addressed. So, in this release, there
is a specific exception being thrown instead of the one that happened to be thrown, which makes the problem more clear.

### Fixed

-   `Fix` There was an issue opened for the STDIO Access Method where if the code being submitted was longer than 128K,
SASPy would deadlock with SAS due to both being single threaded and the way Pipes work; trying to flush STDIN would block
in SASPy because SAS was blocked on writing to STDOUT/ERR, so they would both deadlock, not being able to read off of the
other Pipes. I reworked how submit works in STDIO, so that there's a blocked amount of STDIN sent before trying to pull off
of both STDOUT and STDERR, iterating till done, to circumvent this behavior. That works great, but it caused issues with
ATTN handling that I support in that Access Method. I needed to rework that to compensate and it's handling it much better.

### Removed

-   `None` Nothing removed




## [4.1.0] - 2022-02-07

### Added

-   `New` I added a new method, lib_path(), off the SASsession object which returns a list of the path(s) for
the libref. Depending upon the engine, 'path' may mean different things. For BASE engines (Linux/PC), it's a directory
or multiple directories if a concatenated libref. For database engines, it varies; may be the database name that you're
connected to. On MVS, it could be then name of a bound library file, or a linux directory path.

### Changed

-   `Tweak` In the submit method of the HTTP access method, for results='text', I removed extraneous empty lines before
and after the code. These resulted in extra 'return's being submitted. Removing these allows correct behavior when using
saspy to interactively debug (w/ pdb) PROC PYTHON code. With the extra 'return' before and after the command you tried
to submit, pdb executed extra commands. Now it's 1:1 with clean debugging using submit().

### Fixed

-   `None` No changes

### Removed

-   `None` Nothing removed



## [4.0.0] - 2022-01-14

### Added

-   `Doc` I added this CHANGELOG.md to the repo to start tracking release changes in this file rather than just in the release notes.
A changelog file seems to be a more conventional way to easily look through changes for each release. I'm not retroactively
adding in the previous 59 versions worth of release notes to this, but will add all future releases.

### Changed

-   `BREAK` This is a breaking change, thus the incrementation of the major digit of the Sematic Version
The change is as follows. sasdata2dataframe (sd2df or other aliases), has returned None when the SAS Data
Set provided doesn't exist. Of course, trying to use that as a dataframe results in an exception. But, if
you coded a check for this and conditionally didn't use it, then this change will break that code.
A FileNotFoundError exception is now thrown, as that's the appropriate Pythonic thing to do in this situation.
\
<br>If you happened to code this:
```
df = sas.sd2df('table','libref')
if df is None:
   # do something because the data set wasn't found in the SAS session
```
<br>Then you would need to change that to:
```
try:
   df = sas.sd2df('table','libref')
except FileNotFoundError:
   # do something because the data set wasn't found in the SAS session
```

-   `UPDATE` Due to the continuing problems with log4j, I have to keep updating the log4j jars I include in the repo for the IOM
Access Method (the IOM Java client requires them to be there even though they are not used). If you recently used the new `log4j`
configuration key in the pervious release, you may will need to update the version you're specifying.
\
<br>SASPy V3.7.8 had log4j 2.12.2 and 2.16.0 jars, but now 2.12.4 and 2.17.1 are included instead.
\
<br>So, if you happened to use `log4j='2.16.0'`, you need to change that to `log4j='2.17.1'` in this release. Be aware
that this can continue to change if more vulnerabilities are found and fixed in log4j.
\
<br>Note also that none of the vulnerabilities are exposed by SASPy as it doesn't use log4j, so there's no actual problem with these
regardless of their version. See more [here](https://sassoftware.github.io/saspy/configuration.html#attn-log4j-vulnerabilities-found-in-dec-2021)


### Fixed

-   `Fix` Changed a logger message from Info to Warning for the case where the SAS session encoding has no
Python equivalent encoding to use for transcoding to/from UTF-8. Should had been Warning level, so this is now fixed.

### Removed

-   `None` Nothing removed


