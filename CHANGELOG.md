# Changelog



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
this name anc change it to be the correct proc name. So, since this release is already a breaking change to fix
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


