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


