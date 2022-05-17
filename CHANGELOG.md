# Changelog

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



# Changelog

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



# Changelog

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


