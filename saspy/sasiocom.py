#
# Copyright SAS Institute
#
#  Licensed under the Apache License, Version 2.0 (the License);
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#

import datetime
import io
import numbers
import os
import shlex
import sys
import warnings

import logging
logger = logging.getLogger('saspy')

from saspy.sasexceptions import SASDFNamesToLongError

try:
    from win32com.client import dynamic
except ImportError:
    pass

try:
    import pandas as pd
except ImportError:
    pass


class SASConfigCOM(object):
    """
    This object is not intended to be used directly. Instantiate a SASSession
    object instead.
    """
    NO_OVERRIDE = ['kernel', 'sb']

    def __init__(self, **kwargs):
        self._kernel = kwargs.get('kernel')

        session = kwargs['sb']
        sascfg = session.sascfg.SAScfg
        name = session.sascfg.name
        cfg = getattr(sascfg, name)
        opts = getattr(sascfg, 'SAS_config_options', {})
        outs = getattr(sascfg, 'SAS_output_options', {})

        self.host = cfg.get('iomhost')
        self.port = cfg.get('iomport')
        self.user = cfg.get('omruser')
        self.pw = cfg.get('omrpw')
        self.authkey = cfg.get('authkey')
        self.class_id = cfg.get('class_id', '440196d4-90f0-11d0-9f41-00a024bb830c')
        self.provider = cfg.get('provider')
        self.encoding = cfg.get('encoding', '')

        self.output = outs.get('output', 'html5')

        self.verbose = opts.get('verbose', True)
        self.verbose = kwargs.get('verbose', self.verbose)

        self._lock = opts.get('lock_down', True)
        self._prompt = session.sascfg._prompt

        if self.authkey is not None:
            self._set_authinfo()

        for key, value in filter(lambda x: x[0] not in self.NO_OVERRIDE, kwargs.items()):
            self._try_override(key, value)

    def _set_authinfo(self):
        """
        Attempt to set the session user's credentials based on provided
        key to read from ~/.authinfo file. See .authinfo documentation
        here: https://documentation.sas.com/api/docsets/authinfo/9.4/content/authinfo.pdf.

        This method supports a subset of the .authinfo spec, in accordance with
        other IO access methods. This method will only parse `user` and `password`
        arguments, but does support spaces in values if the value is quoted. Use
        python's `shlex` library to parse these values.
        """
        if os.name == 'nt':
            authfile = os.path.expanduser(os.path.join('~', '_authinfo'))
        else:
            authfile = os.path.expanduser(os.path.join('~', '.authinfo'))

        try:
            with open(authfile, 'r') as f:
                # Take first matching line found
                parsed = (shlex.split(x, posix=False) for x in f.readlines())
                authline = next(filter(lambda x: x[0] == self.authkey, parsed), None)

        except OSError:
            logger.error('Error trying to read {}'.format(authfile))
            authline = None

        if authline is None:
            logger.error('Key {} not found in authinfo file: {}'.format(self.authkey, authfile))
        elif len(authline) < 5:
            logger.error('Incomplete authinfo credentials in {}; key: {}'.format(authfile, self.authkey))
        else:
            # Override user/pw if previously set
            # `authline` is in the following format:
            #   AUTHKEY username USERNAME password PASSWORD
            self.user = authline[2]
            self.pw = authline[4]

    def _try_override(self, attr, value):
        """
        Attempt to override a configuration file option if `self._lock` is
        False. Otherwise, warn the user.
        :param attr: Configuration attribute.
        :param value: Configuration value.
        """
        if self._lock is False:
            setattr(self, attr, value)
        else:
            err = "Param '{}' was ignored due to configuration restriction".format(attr)
            logger.warning(err, file=sys.stderr)


class SASSessionCOM(object):
    """
    Initiate a connection to a SAS server and provide access for Windows
    clients without the Java dependency. Utilizes available COM objects for
    client communication with the IOM interface.
    It may be possible to communicate with local SAS instances as well,
    although this is functionality is untested. A slight change may be
    required to the `_startsas` method to support local instances.
    """
    SAS_APP = 'SASApp'
    HTML_RESULT_FILE = 'saspy_results.html'

    # SASObjectManager.Protocols Enum values
    PROTOCOL_COM = 0
    PROTOCOL_IOM = 2

    # SAS Date/Time/Datetime formats
    FMT_DEFAULT_DATE_NAME = 'E8601DA'
    FMT_DEFAULT_DATE_LENGTH = 10
    FMT_DEFAULT_DATE_PRECISION = 0
    FMT_DEFAULT_TIME_NAME = 'E8601TM'
    FMT_DEFAULT_TIME_LENGTH = 15
    FMT_DEFAULT_TIME_PRECISION = 6
    FMT_DEFAULT_DATETIME_NAME = 'E8601DT'
    FMT_DEFAULT_DATETIME_LENGTH = 26
    FMT_DEFAULT_DATETIME_PRECISION = 6

    # Pandas data types
    PD_NUM_TYPE = ('i', 'u', 'f', 'c')
    PD_STR_TYPE = ('S', 'U', 'V')
    PD_DT_TYPE = ('M')
    PD_BOOL_TYPE = ('b')

    # ADODB RecordSet CursorTypeEnum values
    CURSOR_UNSPECIFIED = -1
    CURSOR_FORWARD = 0
    CURSOR_KEYSET = 1
    CURSOR_DYNAMIC = 2
    CURSOR_STATIC = 3

    # ADODB RecordSet LockTypeEnum values
    LOCK_UNSPECIFIED = -1
    LOCK_READONLY = 1
    LOCK_PESSIMISTIC = 2
    LOCK_OPTIMISTIC = 3
    LOCK_BATCH_OPTIMISTIC = 4

    # ADODB RecordSet CommandTypeEnum values
    CMD_UNSPECIFIED = -1
    CMD_TEXT = 1
    CMD_TABLE = 2
    CMD_STORED_PROC = 4
    CMD_UNKNOWN = 8
    CMD_FILE = 256
    CMD_TABLE_DIRECT = 512

    # ADODB Connection SchemaEnum values
    SCHEMA_COLUMNS = 4
    SCHEMA_TABLES = 20

    # ADODB ObjectStateEnum values
    STATE_CLOSED = 0
    STATE_OPEN = 1

    # FileService StreamOpenMode values
    STREAM_READ = 1
    STREAM_WRITE = 2

    def __init__(self, **kwargs):
        self._log = ''
        self.sascfg = SASConfigCOM(**kwargs)
        self._sb = kwargs.get('sb')

        self.pid = self._startsas()

    def __del__(self):
        if self.adodb.State == self.STATE_OPEN:
            self._endsas()

    def _startsas(self) -> str:
        """
        Create a workspace and open a connection with SAS.
        :return [str]:
        """
        if getattr(self, 'workspace', None) is not None:
            # Do not create a new connection
            return self.workspace.UniqueIdentifier

        factory = dynamic.Dispatch('SASObjectManager.ObjectFactoryMulti2')
        server = dynamic.Dispatch('SASObjectManager.ServerDef')

        self.keeper = dynamic.Dispatch('SASObjectManager.ObjectKeeper')
        self.adodb = dynamic.Dispatch('ADODB.Connection')

        if self.sascfg.host is None:
            # Create a local connection.
            server.MachineDNSName = '127.0.0.1'
            server.Port = 0
            server.Protocol = self.PROTOCOL_COM

            user = None
            password = None
        else:
            # Create a remote connection. The following are required:
            #   1. host
            #   2. port
            #   3. class_id
            server.MachineDNSName = self.sascfg.host
            server.Port = self.sascfg.port
            server.Protocol = self.PROTOCOL_IOM
            server.ClassIdentifier = self.sascfg.class_id

            if self.sascfg.user is not None:
                user = self.sascfg.user
            else:
                user = self.sascfg._prompt('Username: ')

            if self.sascfg.pw is not None:
                password = self.sascfg.pw
            else:
                password = self.sascfg._prompt('Password: ', pw=True)

        self.workspace = factory.CreateObjectByServer(self.SAS_APP, True,
            server, user, password)

        self.keeper.AddObject(1, 'WorkspaceObject', self.workspace)
        self.adodb.Open('Provider={}; Data Source=iom-id://{}'.format(
            self.sascfg.provider, self.workspace.UniqueIdentifier))

        ll = self.submit("options svgtitle='svgtitle'; options validvarname=any validmemname=extend pagesize=max nosyntaxcheck; ods graphics on;", "text")
        if self.sascfg.verbose:
            logger.info("SAS Connection established. Workspace UniqueIdentifier is "+str(self.workspace.UniqueIdentifier)+"\n")

        return self.workspace.UniqueIdentifier

    def _endsas(self):
        """
        Close a connection with SAS.
        """
        self.adodb.Close()
        self.keeper.RemoveObject(self.workspace)
        self.workspace.Close()
        if self.sascfg.verbose:
            logger.info("SAS Connection terminated. Workspace UniqueIdentifierid was "+str(self.pid))

    def _getlst(self, buf: int=2048) -> str:
        """
        Flush listing.
        :option buf [int]: Download buffer. Default 2048.
        :return [str]:
        """
        flushed = self.workspace.LanguageService.FlushList(buf)
        result = flushed
        while flushed:
            flushed = self.workspace.LanguageService.FlushList(buf)
            result += flushed

        return result

    def _getlog(self, buf: int=2048) -> str:
        """
        Flush log.
        :option buf [int]: Download buffer. Default 2048.
        :return [str]:
        """
        flushed = self.workspace.LanguageService.FlushLog(buf)
        result = flushed
        while flushed:
            flushed = self.workspace.LanguageService.FlushLog(buf)
            result += flushed

        # Store flush result in running log
        self._log += result

        if result.count('\nERROR:') > 0:
           warnings.warn("Noticed 'ERROR:' in LOG, you ought to take a look and see if there was a problem")
           self._sb.check_error_log = True

        return result

    def _getfile(self, fname: str, buf: int=2048, decode: bool=False) -> str:
        """
        Use object file service to download a file from the provider.
        :param fname [str]: Filename.
        :option buf [int]: Download buffer. Default 2048.
        :option decode [bool]: Decode the byte stream.
        :return [str]:
        """
        fobj = self.workspace.FileService.AssignFileref('outfile', 'DISK', fname, '', '')

        # Use binary stream to support text and image transfers. The binary
        # stream interface does not require a max line length, which allows
        # support of arbitrarily wide tables.
        stream = fobj[0].OpenBinaryStream(self.STREAM_READ)
        flushed = stream.Read(buf)
        result = bytes(flushed)
        while flushed:
            flushed = stream.Read(buf)
            result += bytes(flushed)

        stream.Close()
        self.workspace.FileService.DeassignFileref(fobj[0].FilerefName)

        if decode is True:
            result = result.decode(self.sascfg.encoding, errors='replace')

        return result

    def _gethtmlfn(self) -> str:
        """
        Return the path of the output HTML file. This is the combination of
        the `workpath` attribute and `HTML_RESULT_FILE` constant.
        :return [str]:
        """
        return self._sb.workpath + self.HTML_RESULT_FILE

    def _reset(self):
        """
        Reset the LanguageService interface to its initial state with respect
        to token scanning. Use it to release the LanguageService from an error
        state associated with the execution of invalid syntax or incomplete
        program source. This primarily occurs when a statement is submitted
        without a trailing semicolon.
        """
        self.workspace.LanguageService.Reset()

    def _tablepath(self, table: str, libref: str=None) -> str:
        """
        Define a sas dataset path based on a table name and optional libref
        name. Will return a two-level or one-level path string based on the
        provided arguments. One-level names are of this form: `table`, while
        two-level names are of this form: `libref.table`. If libref is not
        defined, SAS will implicitly define the library to WORK or USER. The
        USER library needs to have been defined previously in SAS, otherwise
        WORK is the default option. If the `libref` parameter is any value
        that evaluates to `False`, the one-level path is returned.
        :param table [str]: SAS data set name.
        :option libref [str]: Optional library name.
        :return [str]:
        """
        if not libref:
            path = "'{}'n".format(table.strip())
        else:
            path = "{}.'{}'n".format(libref, table.strip())

        return path

    def _schema(self, table: str, libref: str=None) -> dict:
        """
        Request a table schema for a given `libref.table`.
        :param table [str]: Table name
        :option libref [str]: Library name.
        :return [dict]:
        """
        #tablepath = self._tablepath(table, libref=libref)
        if not libref:
            tablepath = table
        else:
            tablepath = "{}.{}".format(libref, table)

        criteria = [None, None, tablepath]

        schema = self.adodb.OpenSchema(self.SCHEMA_COLUMNS, criteria)
        schema.MoveFirst()

        metadata = {}
        while not schema.EOF:
            col_info = {x.Name: x.Value for x in schema.Fields}
            if col_info['FORMAT_NAME'] in self._sb.sas_date_fmts:
                col_info['CONVERT'] = lambda x: self._sb.SAS_EPOCH + datetime.timedelta(days=x)    if x else x
            elif col_info['FORMAT_NAME'] in self._sb.sas_datetime_fmts:
                col_info['CONVERT'] = lambda x: self._sb.SAS_EPOCH + datetime.timedelta(seconds=x) if x else x
            # elif FIXME TIME FORMATS
            else:
                col_info['CONVERT'] = lambda x: x

            metadata[col_info['COLUMN_NAME']] = col_info
            schema.MoveNext()

        schema.Close()

        return metadata

    def _prompt(self, key: str, hide: bool=False) -> tuple:
        """
        Ask the user for input about a given key.
        :param key [str]: Key name.
        :option hide [bool]: Hide user keyboard input.
        :return [tuple]:
        """
        input_ok = False
        while input_ok is False:
            val = self.sascfg._prompt('Enter value for macro variable {} '.format(key), pw=hide)

            if val is None:
               raise RuntimeError("No value for prompted macro variable provided.")

            if val:
                input_ok = True
            else:
                print('Input not valid.')

        return (key, val)

    def _asubmit(self, code: str, results: str='html'):
        """
        Submit any SAS code. Does not return a result.
        :param code [str]: SAS statements to execute.
        """
        # Support html ods
        if results.lower() == 'html':
            ods_open = """
                ods listing close;
                ods {} (id=saspy_internal) options(bitmap_mode='inline')
                    file="{}"
                    device=svg
                    style={};
                ods graphics on / outputfmt=png;
            """.format(self.sascfg.output, self._gethtmlfn(), self._sb.HTML_Style)

            ods_close = """
                ods {} (id=saspy_internal) close;
                ods listing;
            """.format(self.sascfg.output)
        else:
            ods_open = ''
            ods_close = ''

        # Submit program
        full_code = ods_open + code + ods_close
        self.workspace.LanguageService.Submit(full_code)

    def submit(self, code: str, results: str='html', prompt: dict=None, **kwargs) -> dict:
        """
        Submit any SAS code. Returns log and listing as dictionary with keys
        LOG and LST.
        :param code [str]: SAS statements to execute.
        :option results [str]: Result format. Options: HTML, TEXT. Default HTML.
        :option prompt [dict]: Create macro variables from prompted keys.
        """
        RESET   = """;*';*";*/;quit;run;"""
        prompt  = prompt if prompt is not None else {}
        printto = kwargs.pop('undo', False)

        macro_declare = ''
        for key, value in prompt.items():
            macro_declare += '%let {} = {};\n'.format(*self._prompt(key, value))

        # Submit program
        self._asubmit(RESET + macro_declare + code + RESET, results)

        # Retrieve listing and log
        log = self._getlog()
        if results.lower() == 'html':
            # Make the following replacements in HTML listing:
            #   1. Swap \x0c for \n
            #   2. Change body class selector
            #   3. Increase font size
            lstf = self._getfile(self._gethtmlfn())
            try:
               lstf = lstf.decode()
            except UnicodeDecodeError: # older SAS used session encoding instead of utf8 like newer SAS
               try:
                  lstf = lstf.decode(self.sascfg.encoding)
               except UnicodeDecodeError:
                  lstf = lstf.decode(errors='replace')

            listing = lstf \
                .replace(chr(12), chr(10)) \
                .replace('<body class="c body">', '<body class="l body">') \
                .replace('font-size: x-small;', 'font-size: normal;')
        else:
            listing = self._getlst()

        # Invalid syntax will put the interface in to an error state. Reset
        # the LanguageService to prevent further errors.
        # FIXME: In the future, may only want to reset on ERROR. However, this
        # operation seems pretty lightweight, so calling `_reset()` on all
        # submits is not a burden.
        self._reset()

        if printto:
           self._asubmit("\nproc printto;run;\n", 'text')
           log += self._getlog()

        self._sb._lastlog = log
        return {'LOG': log, 'LST': listing}

    def saslog(self) -> str:
        """
        Return the full SAS log.
        :return [str]:
        """
        return self._log

    def exist(self, table: str, libref: str=None) -> bool:
        """
        Determine if a `libref.table` exists.
        :param table [str]: Table name
        :option libref [str]: Library name.
        :return [bool]:
        """
        #tablepath = self._tablepath(table, libref=libref)
        #criteria = [None, None, tablepath]

        #schema = self.adodb.OpenSchema(self.SCHEMA_COLUMNS, criteria)
        #exists = not schema.BOF

        #schema.Close()

        #return exists

        code  = 'data _null_; e = exist("'
        if len(libref):
           code += libref+"."
        code += "'"+table.strip()+"'n"+'"'+");\n"
        code += 'v = exist("'
        if len(libref):
           code += libref+"."
        code += "'"+table.strip()+"'n"+'"'+", 'VIEW');\n if e or v then e = 1;\n"
        code += "te='TABLE_EXISTS='; put te e;run;\n"

        ll = self.submit(code, "text")

        l2 = ll['LOG'].rpartition("TABLE_EXISTS= ")
        l2 = l2[2].partition("\n")
        exists = int(l2[0])

        return bool(exists)


    def read_sasdata(self, table: str, libref: str=None, dsopts: dict=None) -> tuple:
        """
        Read any SAS dataset and return as a tuple of header, rows
        :param table [str]: Table name
        :option libref [str]: Library name.
        :option dsopts [dict]: Dataset options.
        :return [tuple]:
        """
        TARGET = '_saspy_sd2df'
        EXPORT = """
            data {tgt};
                set {tbl} {dopt};
            run;
        """

        dsopts = self._sb._dsopts(dsopts) if dsopts is not None else ''
        tablepath = self._tablepath(table, libref=libref)
        recordset = dynamic.Dispatch('ADODB.RecordSet')

        # Create an intermediate dataset with `dsopts` applied
        export = EXPORT.format(tgt=TARGET, tbl=tablepath, dopt=dsopts)
        self.workspace.LanguageService.Submit(export)
        meta = self._schema(TARGET)

        # Connect RecordSet object to ADODB connection with params:
        #   Cursor:     Forward Only
        #   Lock:       Read Only
        #   Command:    Table Direct
        recordset.Open(TARGET, self.adodb, self.CURSOR_FORWARD,
            self.LOCK_READONLY, self.CMD_TABLE_DIRECT)
        recordset.MoveFirst()

        header = [x.Name for x in recordset.Fields]
        rows = []
        while not recordset.EOF:
            rows.append([meta[x.Name]['CONVERT'](x.Value) for x in recordset.Fields])
            recordset.MoveNext()

        recordset.Close()

        return (header, rows, meta)

    def dataframe2sasdata(self, df: '<Pandas Data Frame object>', table: str ='a',
                          libref: str ="", keep_outer_quotes: bool=False,
                                           embedded_newlines: bool=True,
                          LF: str = '\x01', CR: str = '\x02',
                          colsep: str = '\x03', colrep: str = ' ',
                          datetimes: dict={}, outfmts: dict={}, labels: dict={},
                          outdsopts: dict={}, encode_errors = None, char_lengths = None,
                          **kwargs):
        """
        Create a SAS dataset from a pandas data frame.
        :param df [pd.DataFrame]: Pandas data frame containing data to write.
        :param table [str]: Table name.
        :option libref [str]: Library name. Default work.

        None of these options are used by this access method; they are needed for other access methods
        keep_outer_quotes - for character columns, have SAS keep any outer quotes instead of stripping them off.
        embedded_newlines - if any char columns have embedded CR or LF, set this to True to get them imported into the SAS data set
        LF - if embedded_newlines=True, the chacter to use for LF when transferring the data; defaults to '\x01'
        CR - if embedded_newlines=True, the chacter to use for CR when transferring the data; defaults to '\x02'
        colsep - the column seperator character used for streaming the delimmited data to SAS defaults to '\x03'
        colrep - the char to convert to for any embedded colsep, LF, CR chars in the data; defaults to  ' '
        datetimes - not implemented yet in this access method
        outfmts - not implemented yet in this access method
        labels - not implemented yet in this access method
        outdsopts - not implemented yet in this access method
        encode_errors - not implemented yet in this access method
        char_lengths - not implemented yet in this access method
        """
        DATETIME_NAME = 'DATETIME26.6'
        DATETIME_FMT = '%Y-%m-%dT%H:%M:%S.%f'

        if self.sascfg.verbose:
           if keep_outer_quotes != False:
              logger.warning("'keep_outer_quotes=' is not used with this access method. option ignored.")
           if embedded_newlines != True:
              logger.warning("'embedded_newlines=' is not used with this access method. option ignored.")
           if LF != '\x01' or CR != '\x02' or colsep != '\x03':
              logger.warning("'LF=, CR= and colsep=' are not used with this access method. option(s) ignored.")
           if datetimes != {}:
              logger.warning("'datetimes=' is not used with this access method. option ignored.")
           if outfmts != {}:
              logger.warning("'outfmts=' is not used with this access method. option ignored.")
           if labels != {}:
              logger.warning("'labels=' is not used with this access method. option ignored.")
           if outdsopts != {}:
              logger.warning("'outdsopts=' is not used with this access method. option ignored.")
           if encode_errors:
              logger.warning("'encode_errors=' is not used with this access method. option ignored.")
           if char_lengths:
              logger.warning("'char_lengths=' is not used with this access method. option ignored.")

        tablepath = self._tablepath(table, libref=libref)

        if type(df.index) != pd.RangeIndex:
           warnings.warn("Note that Indexes are not transferred over as columns. Only actual columns are transferred")

        longname = False
        columns  = []
        formats  = {}
        for i, name in enumerate(df.columns):
            if len(name.encode(self.sascfg.encoding)) > 32:
               warnings.warn("Column '{}' in DataFrame is too long for SAS. Rename to 32 bytes or less".format(name),
                        RuntimeWarning)
               longname = True
            if df[name].dtypes.kind in self.PD_NUM_TYPE:
                # Numeric type
                definition = "'{}'n num".format(name)
                formats[name] = lambda x: str(x) if pd.isnull(x) is False else 'NULL'
            elif df[name].dtypes.kind in self.PD_STR_TYPE:
                # Character type
                # NOTE: If a character string contains a single `'`, replace
                #       it with `''`. This is the SAS equivalent to `\'`.
                length = df[name].map(len).max()
                definition = "'{}'n char({})".format(name, length)
                formats[name] = lambda x: "'{}'".format(x.replace("'", "''")) if pd.isnull(x) is False else 'NULL'
            elif df[name].dtypes.kind in self.PD_DT_TYPE:
                # Datetime type
                definition = "'{}'n num informat={} format={}".format(name, DATETIME_NAME, DATETIME_NAME)
                formats[name] = lambda x: "'{:{}}'DT".format(x, DATETIME_FMT) if pd.isnull(x) is False else 'NULL'
            else:
                # Default to character type
                # NOTE: If a character string contains a single `'`, replace
                #       it with `''`. This is the SAS equivalent to `\'`.
                length = df[name].map(str).map(len).max()
                definition = "'{}'n char({})".format(name, length)
                formats[name] = lambda x: "'{}'".format(x.replace("'", "''")) if pd.isnull(x) is False else 'NULL'

            columns.append(definition)

        if longname:
           raise SASDFNamesToLongError(Exception)

        sql_values = []
        for index, row in df.iterrows():
            vals = []
            for i, col in enumerate(row):
                func = formats[df.columns[i]]
                vals.append(func(col))

            sql_values.append('values({})'.format(', '.join(vals)))

        sql_create = 'create table {} ({});'.format(tablepath, ', '.join(columns))
        sql_insert = 'insert into {} {};'.format(tablepath, '\n'.join(sql_values))

        self.adodb.Execute(sql_create)
        self.adodb.Execute(sql_insert)
        return None

    def sasdata2dataframe(self, table: str, libref: str=None, dsopts: dict=None, method: str='', **kwargs) -> 'pd.DataFrame':
        """
        Create a pandas data frame from a SAS dataset.
        :param table [str]: Table name.
        :option libref [str]: Library name.
        :option dsopts [dict]: Dataset options.
        :option method [str]: Download method.
        :option tempkeep [bool]: Download the csv file if using the csv method.
        :option tempfile [str]: File path for the saved output file.
        :return [pd.DataFrame]:
        """
        # strip off unused by this access method options from kwargs
        # so they can't be passes to panda later
        rowsep = kwargs.pop('rowsep', ' ')
        colsep = kwargs.pop('colsep', ' ')
        rowrep = kwargs.pop('rowrep', ' ')
        colrep = kwargs.pop('colrep', ' ')

        if method.upper() == 'DISK':
           logger.error("This access method doesn't support the DISK method. Try CSV or MEMORY")
           return None

        if method.upper() == 'CSV':
            df = self.sasdata2dataframeCSV(table, libref, dsopts=dsopts, **kwargs)
        else:
            my_fmts = kwargs.pop('my_fmts', False)
            k_dts   = kwargs.pop('dtype',   None)
            if self.sascfg.verbose:
               if my_fmts != False:
                  logger.warning("'my_fmts=' is not supported in this access method. option ignored.")
               if k_dts is not None:
                  logger.warning("'dtype=' is only used with the CSV version of this method. option ignored.")

            header, rows, meta = self.read_sasdata(table, libref, dsopts=dsopts)
            df = pd.DataFrame.from_records(rows, columns=header, **kwargs)

            for col in meta.keys():
               if meta[col]['FORMAT_NAME'] in self._sb.sas_date_fmts + self._sb.sas_datetime_fmts:
                  df[col] = pd.to_datetime(df[col], errors='coerce')
               elif meta[col]['DATA_TYPE'] == 5:
                  df[col] = pd.to_numeric(df[col], errors='coerce')

        return df

    def sasdata2dataframeCSV(self, table: str, libref: str ='', dsopts: dict = None,
                             tempfile: str=None, tempkeep: bool=False, **kwargs) -> 'pd.DataFrame':
        """
        Create a pandas data frame from a SAS dataset.
        :param table [str]: Table name.
        :option libref [str]: Library name.
        :option dsopts [dict]: Dataset options.
        :option opts [dict]: dictionary containing any of the following Proc Export options(delimiter, putnames)
        :option tempkeep [bool]: Download the csv file if using the csv method.
        :option tempfile [str]: File path for the saved output file.
        :return [pd.DataFrame]:
        """
        FORMAT_STRING = '{column} {format}{length}.{precision}'
        EXPORT = """
            data _saspy_sd2df;
                format {fmt};
                set {tbl};
            run;

            proc export data=_saspy_sd2df {dopt}
                    outfile="{out}"
                    dbms=csv replace;
                    {exopts}
            run;
        """
        k_dts   = kwargs.get('dtype',   None)
        my_fmts = kwargs.pop('my_fmts', False)
        if self.sascfg.verbose:
           if my_fmts != False:
              logger.warning("'my_fmts=' is not supported in this access method. option ignored.")

        sas_csv = '{}saspy_sd2df.csv'.format(self._sb.workpath)
        dopts = self._sb._dsopts(dsopts) if dsopts is not None else ''
        tablepath = self._tablepath(table, libref=libref)

        expopts = self._sb._expopts(kwargs.pop('opts', {}))

        # Convert any date format to one pandas can understand (ISO-8601).
        # Save a reference of the column name in a list so pandas can parse
        # the column during construction.
        datecols = []
        fmtlist = []
        meta = self._schema(table, libref)
        for name, col in meta.items():
            if col['FORMAT_NAME'] in self._sb.sas_date_fmts:
                datecols.append(name)
                col_format = self.FMT_DEFAULT_DATE_NAME
                col_length = self.FMT_DEFAULT_DATE_LENGTH
                col_precis = self.FMT_DEFAULT_DATE_PRECISION
            elif col['FORMAT_NAME'] in self._sb.sas_datetime_fmts:
                datecols.append(name)
                col_format = self.FMT_DEFAULT_DATETIME_NAME
                col_length = self.FMT_DEFAULT_DATETIME_LENGTH
                col_precis = self.FMT_DEFAULT_DATETIME_PRECISION
            # elif FIXME TIME FORMATS
            else:
                col_format = col['FORMAT_NAME']
                col_length = col['FORMAT_LENGTH']
                col_precis = col['FORMAT_DECIMAL']

            if col['FORMAT_NAME']:
               full_format = FORMAT_STRING.format(
                   column=col['COLUMN_NAME'],
                   format=col_format,
                   length=col_length,
                   precision=col_precis)

               fmtlist.append(full_format)

        export = EXPORT.format(fmt=' '.join(fmtlist),
            tbl=tablepath,
            dopt=dopts,
            exopts=expopts,
            out=sas_csv)

        # Use `LanguageService.Submit` instead of `submit` for a slight
        # performance bump. We don't need the log or listing here so skip
        # the wrapper function.
        self.workspace.LanguageService.Submit(export)

        outstring = self._getfile(sas_csv, decode=True)

        # Write temp file if requested by user
        if kwargs.get('tempkeep') is True and kwargs.get('tempfile') is not None:
            with open(kwargs['tempfile'], 'w') as f:
                f.write(outstring)

        df = pd.read_csv(io.StringIO(outstring), parse_dates=datecols, **kwargs)

        if k_dts is None:  # don't override these if user provided their own dtypes
           for col in meta.keys():
              if meta[col]['FORMAT_NAME'] in self._sb.sas_date_fmts + self._sb.sas_datetime_fmts:
                 df[col] = pd.to_datetime(df[col], errors='coerce')

        return df

    def sasdata2parquet(self, parquet_file_path: str, table: str, libref: str ='',
                        dsopts: dict = None, pa_schema: 'pa_schema' = None,
                        static_columns:list = None,
                        partitioned = False, partition_size_mb = 128,
                        chunk_size_mb = 4, compression = 'snappy',
                        rowsep: str = '\x01', colsep: str = '\x02',
                        rowrep: str = ' ',    colrep: str = ' ',
                        **kwargs) -> None:

       logger.error("This access method doesn't support this method. Try the IOM access method instead.")
       return None

    def upload(self, local: str, remote: str, overwrite: bool=True, permission: str='', **kwargs):
        """
        Upload a file to the SAS server.
        :param local [str]: Local filename.
        :param remote [str]: Local filename.
        :option overwrite [bool]: Overwrite the file if it exists.
        :option permission [str]: See SAS filename statement documentation.
        """
        perms = "PERMISSION='{}'".format(permission) if permission else ''
        valid = self._sb.file_info(remote, quiet=True)

        if valid == {}:
            # Parameter `remote` references a directory. Default to using the
            # filename in `local` path.
            remote_file = remote + self._sb.hostsep + os.path.basename(local)
        elif valid is not None and overwrite is False:
            # Parameter `remote` references a file that exists but we cannot
            # overwrite it.
            # TODO: Raise exception here instead of returning dict
            return {'Success': False,
                'LOG': 'File {} exists and overwrite was set to False. Upload was stopped.'.format(remote)}
        else:
            remote_file = remote

        with open(local, 'rb') as f:
            fobj = self.workspace.FileService.AssignFileref('infile', 'DISK', remote_file, perms, '')
            stream = fobj[0].OpenBinaryStream(self.STREAM_WRITE)

            stream.Write(f.read())
            stream.Close()
            self.workspace.FileService.DeassignFileref(fobj[0].FilerefName)

        return {'Success': True,
            'LOG': 'File successfully written using FileService.'}

    def download(self, local: str, remote: str, overwrite: bool=True, **kwargs):
        """
        Download a file from the SAS server.
        :param local [str]: Local filename.
        :param remote [str]: Local filename.
        :option overwrite [bool]: Overwrite the file if it exists.
        """
        valid = self._sb.file_info(remote, quiet=True)

        if valid is None:
            # Parameter `remote` references an invalid file path.
            # TODO: Raise exception here instead of returning dict
            return {'Success': False,
                'LOG': 'File {} does not exist.'.format(remote)}
        elif valid == {}:
            # Parameter `remote` references a directory.
            # TODO: Raise exception here instead of returning dict
            return {'Success': False,
                'LOG': 'File {} is a directory.'.format(remote)}

        if os.path.isdir(local) is True:
            # Parameter `local` references a directory. Default to using the
            # filename in `remote` path.
            local_file = os.path.join(local, remote.rpartition(self._sb.hostsep)[2])
        else:
            local_file = local

        with open(local_file, 'wb') as f:
            f.write(self._getfile(remote))

        return {'Success': True,
            'LOG': 'File successfully read using FileService.'}
