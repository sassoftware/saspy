from contextlib import redirect_stdout
from io import StringIO
import unittest
import saspy
import re

SRC = 'cpsrc'
DST = 'cpdst'

class TestSASsessionCopy(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.sas = saspy.SASsession()
        cls.sas.set_batch(True)

        # Path based source and destination libraries under WORK, so they are local to the SAS server
        cls.sas.submit(f"""
            options dlcreatedir;
            libname {SRC} "%sysfunc(pathname(work))/{SRC}";
            libname {DST} "%sysfunc(pathname(work))/{DST}";
        """)

    @classmethod
    def tearDownClass(cls):
        cls.sas._endsas()

    def setUp(self):
        """
        Start every test with an empty destination library and a known set of
        members in the source library.
        """
        self.sas.check_error_log = False
        self.sas.submit(f"""
            proc datasets lib={SRC} kill nolist memtype=all; quit;
            proc datasets lib={DST} kill nolist memtype=all; quit;
            data {SRC}.cars {SRC}.cars1 {SRC}.cars2 {SRC}.cars3 {SRC}.other;
                set sashelp.cars;
            run;
        """)

    def helper_code(self, *args, **kwargs) -> list:
        """
        Get the code copy() generates, without submitting it.
        :return [list]: the non-blank lines of generated code, stripped
        """
        captured = StringIO()
        with redirect_stdout(captured):
            self.sas.teach_me_SAS(True)
            try:
                self.sas.copy(*args, **kwargs)
            finally:
                self.sas.teach_me_SAS(False)

        return [l.strip() for l in captured.getvalue().splitlines() if l.strip()]

    def helper_proc_stmt(self, **kwargs) -> str:
        """
        Get only the PROC COPY statement generated for copying cars from SRC to DST.
        """
        return self.helper_code('cars', SRC, DST, **kwargs)[0]

    def helper_exist(self, libref: str, member: str, memtype: str = 'DATA') -> bool:
        """
        Check for a member of any type in a library.
        """
        self.sas.submit(f"""
            proc sql noprint;
                select count(*) into :_cpcnt trimmed from dictionary.members
                where libname = "{libref.upper()}" and upcase(memname) = "{member.upper()}"
                  and memtype = "{memtype.upper()}";
            quit;
        """)
        return self.sas.symget('_cpcnt', outtype='int') > 0

    def helper_members(self, libref: str) -> set:
        """
        Get the set of data set names in a library.
        """
        # Reset first, since SELECT INTO leaves the macro variable unchanged when no rows are found
        self.sas.submit(f"""
            %let _cpmems = ;
            proc sql noprint;
                select memname into :_cpmems separated by ' ' from dictionary.members
                where libname = "{libref.upper()}" and memtype = 'DATA';
            quit;
        """)
        return set(self.sas.symget('_cpmems', outtype='str').split())

    def helper_assert_copied(self, log: str):
        """
        Assert the PROC COPY step ran without errors.
        """
        self.assertNotIn('ERROR', log, msg="PROC COPY log contains an ERROR")
        self.assertFalse(self.sas.check_error_log, msg="check_error_log was set by PROC COPY")

    # ------------------------------------------------------------------
    # Generated syntax (not submitted to SAS)
    # ------------------------------------------------------------------

    def test_copy_syntax_default(self):
        """
        Test that with no options, a plain PROC COPY with a SELECT statement is generated
        """
        code = self.helper_code('cars', SRC, DST)

        self.assertEqual(code, [f'proc copy in={SRC} out={DST} ;', 'select cars;', 'run;'])

    def test_copy_syntax_table_list(self):
        """
        Test that a list of tables is generated as a space separated SELECT list
        """
        code = self.helper_code(['cars', 'cars1', 'cars2'], SRC, DST)

        self.assertEqual(code[1], 'select cars cars1 cars2;')

    def test_copy_syntax_exclude(self):
        """
        Test that exclude=True generates an EXCLUDE statement instead of SELECT
        """
        self.assertEqual(self.helper_code(['cars', 'cars1'], SRC, DST, exclude=True)[1], 'exclude cars cars1;')
        self.assertEqual(self.helper_code('cars', SRC, DST, exclude=False)[1], 'select cars;')

    def test_copy_syntax_boolean_options(self):
        """
        Test that each boolean argument maps to its PROC COPY option for True, False and None
        """
        EXPECTED = {
            'move':             {True: 'move',           False: None},
            'clone':            {True: 'clone',          False: 'noclone'},
            'force':            {True: 'force',          False: None},
            'cas_acceleration': {True: 'accel',          False: 'noaccel'},
            'copy_constraints': {True: 'constraint=yes', False: 'constraint=no'},
            'copy_timestamps':  {True: 'datecopy',       False: None},
            'copy_indexes':     {True: 'index=yes',      False: 'index=no'},
        }
        default = f'proc copy in={SRC} out={DST} ;'

        for arg, values in EXPECTED.items():
            for value, option in values.items():
                with self.subTest(arg=arg, value=value):
                    stmt = self.helper_proc_stmt(**{arg: value})
                    if option is None:
                        self.assertEqual(stmt, default)
                    else:
                        self.assertEqual(stmt, f'proc copy in={SRC} out={DST} {option};')

            with self.subTest(arg=arg, value=None):
                self.assertEqual(self.helper_proc_stmt(**{arg: None}), default)

    def test_copy_syntax_multiple_options(self):
        """
        Test that multiple options are all generated on the PROC COPY statement
        """
        stmt = self.helper_proc_stmt(move=True, clone=False, copy_indexes=True, copy_timestamps=True)

        self.assertEqual(stmt, f'proc copy in={SRC} out={DST} move noclone datecopy index=yes;')

    def test_copy_syntax_member_types(self):
        """
        Test that member_types generates a parenthesized MEMTYPE= list for a string or a list
        """
        self.assertIn('memtype=(data)', self.helper_proc_stmt(member_types='data'))
        self.assertIn('memtype=(data catalog)', self.helper_proc_stmt(member_types=['data', 'catalog']))

    def test_copy_syntax_passwords(self):
        """
        Test that encryption_key and alter_password generate quoted ENCRYPTKEY= and ALTER= options
        """
        # The values themselves are masked in teach_me_SAS mode; test_copy_encrypted checks them when submitted
        stmt = self.helper_proc_stmt(encryption_key='Secret', alter_password='pw')

        self.assertEqual(stmt, f"proc copy in={SRC} out={DST} encryptkey='*****' alter='*****';")

    def test_copy_syntax_override_options(self):
        """
        Test that override_options are passed through as option=value
        """
        stmt = self.helper_proc_stmt(override_options={'memtype': 'data', 'index': 'no'})

        self.assertIn('memtype=data', stmt)
        self.assertIn('index=no', stmt)

    def test_copy_syntax_masks_passwords(self):
        """
        Test that teach_me_SAS mode never shows a password or encryption key, however it is passed,
        and that each one is replaced with the mask in place
        """
        # Every password contains SECRET, so finding SECRET anywhere in the output means a (partial) leak
        SECRET = 'S3cret'
        SCENARIOS = {
            # name:                        (copy() arguments,                                                expected masked text)
            'encryption_key':              (dict(encryption_key=SECRET),                                    "encryptkey='*****'"),
            'encryption_key apostrophe':   (dict(encryption_key=f"{SECRET}'{SECRET}"),                      "encryptkey='*****'"),
            'alter_password':              (dict(alter_password=SECRET),                                    "alter='*****'"),
            'alter_password apostrophe':   (dict(alter_password=f"{SECRET}'{SECRET}"),                      "alter='*****'"),
            'override encryptkey':         (dict(override_options={'encryptkey': f"'{SECRET}'"}),           "encryptkey='*****'"),
            'override ALTER':              (dict(override_options={'ALTER': f"'{SECRET}'"}),                "ALTER='*****'"),
            'override pw':                 (dict(override_options={'pw': f"'{SECRET}'"}),                   "pw='*****'"),
            'override Protect':            (dict(override_options={'Protect': f"'{SECRET}'"}),              "Protect='*****'"),
            'override unquoted':           (dict(override_options={'pw': SECRET}),                          "pw='*****'"),
            'override double quoted':      (dict(override_options={'pw': f'"{SECRET} {SECRET}"'}),          "pw='*****'"),
            'override doubled quote':      (dict(override_options={'pw': f"'{SECRET}''{SECRET}'"}),         "pw='*****'"),
            'override space before =':     (dict(override_options={'pw ': f"'{SECRET}'"}),                  "pw='*****'"),
            'override OVERRIDE=':          (dict(override_options={'override': f"(alter='{SECRET}')"}),     "override=(alter='*****')"),
            'member alter':                (dict(table=f"cars(alter='{SECRET}')"),                          "select cars(alter='*****');"),
            'member read':                 (dict(table=f"cars(read='{SECRET}')"),                           "select cars(read='*****');"),
            'member write':                (dict(table=f"cars(write='{SECRET}')"),                          "select cars(write='*****');"),
            'member list':                 (dict(table=[f"cars(alter={SECRET})", f"cars1(read={SECRET})"]), "select cars(alter='*****') cars1(read='*****');"),
            'member exclude':              (dict(table=f"cars(alter='{SECRET}')", exclude=True),            "exclude cars(alter='*****');"),
        }

        for scenario, (kwargs, expected) in SCENARIOS.items():
            with self.subTest(scenario=scenario):
                table = kwargs.pop('table', 'cars')
                code = ' '.join(self.helper_code(table, SRC, DST, **kwargs))

                self.assertNotIn(SECRET, code, msg="password shown in teach_me_SAS output")
                self.assertIn(expected, code)

    def test_copy_syntax_masks_all_passwords(self):
        """
        Test that every password in one statement is masked, with teach_me_SAS turned on as teach_me_SAS(1)
        """
        captured = StringIO()
        with redirect_stdout(captured):
            self.sas.teach_me_SAS(1)
            try:
                self.sas.copy("cars(read='r1')", SRC, DST, encryption_key='k1', alter_password='a1',
                              override_options={'pw': "'p1'", 'protect': "'p2'", 'override': "(write='w1')"})
            finally:
                self.sas.teach_me_SAS(0)
        code = ' '.join(captured.getvalue().split())

        self.assertEqual(code, f"proc copy in={SRC} out={DST} encryptkey='*****' alter='*****' pw='*****' protect='*****' "
                               f"override=(write='*****'); select cars(read='*****'); run;")

    def test_copy_syntax_masks_only_passwords(self):
        """
        Test that options and member names that are not passwords, even ones that look similar, are not masked
        """
        code = ' '.join(self.helper_code(['altered', 'readme', 'pw_cars', 'write_log', 'cars(memtype=data)'], SRC, DST,
                                         copy_indexes=False, override_options={'memtype': 'data', 'protected': 'no'}))

        self.assertEqual(code, f"proc copy in={SRC} out={DST} index=no memtype=data protected=no; "
                               f"select altered readme pw_cars write_log cars(memtype=data); run;")

    def test_copy_passwords_not_masked_when_submitted(self):
        """
        Test that the real encryption key and alter password are used when not in teach_me_SAS mode,
        and that the SAS log does not show them
        """
        self.sas.submit(f"data {SRC}.enc(encrypt=aes encryptkey='S3cret' alter='Pw9'); set sashelp.cars; run;")
        try:
            log = self.sas.copy('enc', SRC, DST, encryption_key='S3cret', alter_password='Pw9')

            self.helper_assert_copied(log)
            self.assertTrue(self.helper_exist(DST, 'enc'))
            self.assertNotIn('S3cret', self.sas.lastlog())
            self.assertNotIn('Pw9', self.sas.lastlog())
        finally:
            self.sas.submit(f"""
                proc datasets lib={SRC} nolist; delete enc(alter='Pw9'); quit;
                proc datasets lib={DST} nolist; delete enc(alter='Pw9'); quit;
            """)

    def test_copy_encryption_key_quotes(self):
        """
        Test that encryption keys containing quotes, which SAS allows, reach SAS unchanged: each data set is
        created with the key written independently as a double quoted SAS literal, then copied with copy()
        """
        KEYS = ["it's", "a''b", "''", "'start", "end'", 'say "hi"', "x'y'z", "with spaces 'and' quotes", "Q'" * 32]

        for key in KEYS:
            with self.subTest(key=key):
                literal = key.replace('"', '""')
                self.sas.submit(f"""
                    proc datasets lib={DST} kill nolist; quit;
                    data {SRC}.enc(encrypt=aes encryptkey="{literal}"); set sashelp.cars; run;
                """)
                self.sas.check_error_log = False

                # A wrong key must fail, so a successful copy proves SAS received exactly this key
                self.assertIn('ERROR', self.sas.copy('enc', SRC, DST, encryption_key=key + 'x'))
                self.sas.check_error_log = False

                log = self.sas.copy('enc', SRC, DST, encryption_key=key)
                self.helper_assert_copied(log)
                self.assertTrue(self.helper_exist(DST, 'enc'))

    def test_copy_encryption_key_quotes_multiple_members(self):
        """
        Test moving several AES encrypted, alter protected data sets in one step with a key containing quotes
        """
        KEY = "it's a ''key''"
        self.sas.submit(f"""
            data {SRC}.e1(encrypt=aes encryptkey="{KEY}" alter=Pw9) {SRC}.e2(encrypt=aes encryptkey="{KEY}" alter=Pw9);
                set sashelp.cars;
            run;
        """)
        try:
            log = self.sas.copy(['e1', 'e2'], SRC, DST, encryption_key=KEY, alter_password='Pw9', move=True)

            self.helper_assert_copied(log)
            self.assertEqual(self.helper_members(DST), {'E1', 'E2'})
            self.assertFalse(self.helper_exist(SRC, 'e1') or self.helper_exist(SRC, 'e2'))
        finally:
            self.sas.submit(f"""
                proc datasets lib={SRC} nolist; delete e1(alter=Pw9) e2(alter=Pw9); quit;
                proc datasets lib={DST} nolist; delete e1(alter=Pw9) e2(alter=Pw9); quit;
            """)

    def test_copy_password_aliases_when_submitted(self):
        """
        Test that the password routes masked in teach_me_SAS mode are real ones: PW=, PROTECT= and a member level
        ALTER= all let PROC COPY move an alter protected data set
        """
        SCENARIOS = {
            'override pw':      dict(override_options={'pw': "'Pw9'"}),
            'override protect': dict(override_options={'protect': "'Pw9'"}),
            'member alter':     dict(table="enc(alter='Pw9')"),
        }

        for scenario, kwargs in SCENARIOS.items():
            with self.subTest(scenario=scenario):
                self.sas.submit(f"""
                    proc datasets lib={DST} nolist; delete enc(alter='Pw9'); quit;
                    data {SRC}.enc(alter='Pw9'); set sashelp.cars; run;
                """)
                self.sas.check_error_log = False
                table = kwargs.pop('table', 'enc')

                log = self.sas.copy(table, SRC, DST, move=True, **kwargs)

                self.helper_assert_copied(log)
                self.assertFalse(self.helper_exist(SRC, 'enc'), msg="alter protected data set was not moved")
                self.assertTrue(self.helper_exist(DST, 'enc'))

        self.sas.submit(f"proc datasets lib={DST} nolist; delete enc(alter='Pw9'); quit;")

    def test_copy_unknown_argument(self):
        """
        Test that a misspelled argument raises TypeError instead of being silently ignored
        """
        with self.assertRaises(TypeError):
            self.sas.copy('cars', SRC, DST, copy_index=True)

        self.assertFalse(self.helper_exist(DST, 'cars'), msg="copy ran despite the invalid argument")

    def test_copy_nosub(self):
        """
        Test that teach_me_SAS mode returns None and does not run PROC COPY
        """
        captured = StringIO()
        with redirect_stdout(captured):
            self.sas.teach_me_SAS(True)
            ret = self.sas.copy('cars', SRC, DST)
            self.sas.teach_me_SAS(False)

        self.assertIsNone(ret)
        self.assertIn('proc copy', captured.getvalue())
        self.assertFalse(self.helper_exist(DST, 'cars'), msg="teach_me_SAS mode copied the data set")

    # ------------------------------------------------------------------
    # Return values / log handling
    # ------------------------------------------------------------------

    def test_copy_batch_returns_log(self):
        """
        Test that in batch mode only the NOTE, WARNING and ERROR messages are returned,
        without the submitted code, page headers or timing note
        """
        EXPECTED = '\n'.join([
            f'NOTE: Copying {SRC.upper()}.CARS to {DST.upper()}.CARS (memtype=DATA).',
            f'NOTE: There were 428 observations read from the data set {SRC.upper()}.CARS.',
            f'NOTE: The data set {DST.upper()}.CARS has 428 observations and 15 variables.',
        ])

        log = self.sas.copy('cars', SRC, DST)

        self.assertEqual(log, EXPECTED)

    def test_copy_log_messages_only(self):
        """
        Test that warnings and errors are kept, and every returned line is a message or its continuation
        """
        # An invalid option gives an ERROR whose list of valid options wraps onto a continuation line
        log = self.sas.copy('cars', SRC, DST, override_options={'nolist': 'x'})

        self.assertIn('ERROR 22-322', log)
        self.assertIn('MEMTYPE', log, msg="wrapped continuation line of the ERROR was dropped")
        for line in log.splitlines():
            self.assertRegex(line, r'^(NOTE|WARNING|ERROR)[ \d-]*:|^ {6,}\S', msg="returned log has a non-message line")
        self.assertNotIn('proc copy', log.lower())
        self.assertNotIn('Total process time', log)

    def test_copy_not_batch_prints_log(self):
        """
        Test that when not in batch mode the SAS log is printed and None is returned,
        and that quiet=True suppresses the print
        """
        self.sas.set_batch(False)
        try:
            captured = StringIO()
            with redirect_stdout(captured):
                ret = self.sas.copy('cars', SRC, DST)
            self.assertIsNone(ret)
            self.assertIn('NOTE: Copying', captured.getvalue())

            captured = StringIO()
            with redirect_stdout(captured):
                ret = self.sas.copy('cars', SRC, DST, quiet=True)
            self.assertIsNone(ret)
            self.assertEqual(captured.getvalue(), '')
        finally:
            self.sas.set_batch(True)

    def test_copy_lastlog(self):
        """
        Test that lastlog() still returns the full log for the PROC COPY step
        """
        self.sas.copy('cars', SRC, DST)

        self.assertIn('proc copy', self.sas.lastlog().lower())

    def test_copy_error_log(self):
        """
        Test that an invalid libref is reported in the returned log and sets check_error_log
        """
        log = self.sas.copy('cars', 'nolib', DST)

        self.assertIn('ERROR', log)
        self.assertTrue(self.sas.check_error_log)

    # ------------------------------------------------------------------
    # Ways to specify input members (run in SAS)
    # ------------------------------------------------------------------

    def test_copy_single_table(self):
        """
        Test copying a single data set given as a string
        """
        log = self.sas.copy('cars', SRC, DST)

        self.helper_assert_copied(log)
        self.assertEqual(self.helper_members(DST), {'CARS'})

    def test_copy_table_list(self):
        """
        Test copying a list of data sets
        """
        log = self.sas.copy(['cars', 'cars1'], SRC, DST)

        self.helper_assert_copied(log)
        self.assertEqual(self.helper_members(DST), {'CARS', 'CARS1'})

    def test_copy_table_mixed_case(self):
        """
        Test that member names and librefs are not case sensitive
        """
        log = self.sas.copy('CaRs', SRC.upper(), DST.capitalize())

        self.helper_assert_copied(log)
        self.assertEqual(self.helper_members(DST), {'CARS'})

    def test_copy_table_prefix(self):
        """
        Test copying all data sets that begin with a prefix (cars:)
        """
        log = self.sas.copy('cars:', SRC, DST)

        self.helper_assert_copied(log)
        self.assertEqual(self.helper_members(DST), {'CARS', 'CARS1', 'CARS2', 'CARS3'})

    def test_copy_table_numbered_range(self):
        """
        Test copying a numbered range of data sets (cars1-cars2)
        """
        log = self.sas.copy('cars1-cars2', SRC, DST)

        self.helper_assert_copied(log)
        self.assertEqual(self.helper_members(DST), {'CARS1', 'CARS2'})

    def test_copy_table_member_memtype(self):
        """
        Test copying a data set with a member level memtype (cars(memtype=data))
        """
        log = self.sas.copy('cars(memtype=data)', SRC, DST)

        self.helper_assert_copied(log)
        self.assertEqual(self.helper_members(DST), {'CARS'})

    def test_copy_table_name_literal(self):
        """
        Test copying data sets that need a name literal when VALIDMEMNAME=EXTEND, given as name literals, alongside
        a standard name
        """
        self.sas.submit(f"""
            %let _cpvmn = %sysfunc(getoption(validmemname));
            options validmemname=extend;
            data {SRC}.'my cars'n {SRC}."it's"n; set sashelp.cars; run;
        """)
        try:
            log = self.sas.copy(["'my cars'n", '''"it's"n''', 'cars'], SRC, DST)

            self.helper_assert_copied(log)
            self.assertTrue(self.helper_exist(DST, 'my cars'))
            self.assertTrue(self.helper_exist(DST, "it's"))
            self.assertTrue(self.helper_exist(DST, 'cars'))
        finally:
            self.sas.submit("options validmemname=&_cpvmn;")

    def test_copy_exclude(self):
        """
        Test that exclude=True copies every member except those listed
        """
        log = self.sas.copy(['cars1', 'cars2', 'cars3'], SRC, DST, exclude=True)

        self.helper_assert_copied(log)
        self.assertEqual(self.helper_members(DST), {'CARS', 'OTHER'})

    def test_copy_missing_table(self):
        """
        Test that copying a member that does not exist is an ERROR and copies nothing
        """
        log = self.sas.copy('notable', SRC, DST)

        self.assertIn('ERROR', log)
        self.assertTrue(self.sas.check_error_log)
        self.assertEqual(self.helper_members(DST), set())

    # ------------------------------------------------------------------
    # Ways to specify source and destination libraries (run in SAS)
    # ------------------------------------------------------------------

    def test_copy_from_sashelp_to_work(self):
        """
        Test copying from a read only library into WORK
        """
        self.sas.submit("proc datasets lib=work nolist; delete cars; quit;")

        log = self.sas.copy('cars', 'sashelp', 'work')

        self.helper_assert_copied(log)
        self.assertTrue(self.sas.exist('cars', 'work'))

    def test_copy_from_concatenated_library(self):
        """
        Test copying from a concatenated library
        """
        self.sas.submit(f"data work.cpwork; set sashelp.cars; run; libname cpcat ({SRC} work);")
        try:
            log = self.sas.copy(['cars', 'cpwork'], 'cpcat', DST)

            self.helper_assert_copied(log)
            self.assertEqual(self.helper_members(DST), {'CARS', 'CPWORK'})
        finally:
            self.sas.submit("libname cpcat clear;")

    def test_copy_xport_round_trip(self):
        """
        Test copying to and from an XPORT transport file library
        """
        # XPORT only allows 8 character variable names, so let SAS truncate the long ones in cars
        self.sas.submit("""
            %let _cpvvn = %sysfunc(getoption(validvarname));
            options validvarname=v6;
            libname cpxpt xport "%sysfunc(pathname(work))/cpcopy.xpt";
        """)
        try:
            log = self.sas.copy('cars', SRC, 'cpxpt')
            self.helper_assert_copied(log)

            log = self.sas.copy('cars', 'cpxpt', DST)
            self.helper_assert_copied(log)
            self.assertEqual(self.helper_members(DST), {'CARS'})
        finally:
            self.sas.submit("libname cpxpt clear; options validvarname=&_cpvvn;")

    # ------------------------------------------------------------------
    # Options (run in SAS)
    # ------------------------------------------------------------------

    def test_copy_member_types(self):
        """
        Test that member_types limits the copy to those member types
        """
        self.sas.submit(f"proc format lib={SRC}.formats; value yn 1='Yes' 0='No'; run;")

        # A selected member that is not one of member_types is an ERROR, so exclude instead to copy all of a type
        log = self.sas.copy('other', SRC, DST, member_types='data', exclude=True)
        self.helper_assert_copied(log)
        self.assertEqual(self.helper_members(DST), {'CARS', 'CARS1', 'CARS2', 'CARS3'})
        self.assertFalse(self.helper_exist(DST, 'formats', 'catalog'))

        log = self.sas.copy(['cars', 'formats'], SRC, DST, member_types=['data', 'catalog'])
        self.helper_assert_copied(log)
        self.assertTrue(self.helper_exist(DST, 'formats', 'catalog'))

    def test_copy_move(self):
        """
        Test that move=True removes the data set from the source library
        """
        log = self.sas.copy('cars', SRC, DST, move=True)

        self.helper_assert_copied(log)
        self.assertTrue(self.helper_exist(DST, 'cars'))
        self.assertFalse(self.helper_exist(SRC, 'cars'))

    def test_copy_clone(self):
        """
        Test that clone=True keeps the source compression and clone=False does not
        """
        self.sas.submit(f"data {SRC}.comp(compress=yes); set sashelp.cars; run;")

        def compress() -> str:
            self.sas.submit(f"""
                proc sql noprint;
                    select compress into :_cpcomp trimmed from dictionary.tables
                    where libname = "{DST.upper()}" and memname = 'COMP';
                quit;
            """)
            return self.sas.symget('_cpcomp', outtype='str')

        self.helper_assert_copied(self.sas.copy('comp', SRC, DST, clone=True))
        self.assertEqual(compress(), 'CHAR')

        self.helper_assert_copied(self.sas.copy('comp', SRC, DST, clone=False))
        self.assertEqual(compress(), 'NO')

    def test_copy_indexes(self):
        """
        Test that copy_indexes controls whether indexes are copied
        """
        self.sas.submit(f"proc datasets lib={SRC} nolist; modify cars; index create model; quit;")

        def indexes() -> int:
            self.sas.submit(f"""
                proc sql noprint;
                    select count(*) into :_cpidx trimmed from dictionary.indexes
                    where libname = "{DST.upper()}" and memname = 'CARS';
                quit;
            """)
            return self.sas.symget('_cpidx', outtype='int')

        self.helper_assert_copied(self.sas.copy('cars', SRC, DST, copy_indexes=False))
        self.assertEqual(indexes(), 0)

        self.helper_assert_copied(self.sas.copy('cars', SRC, DST, copy_indexes=True))
        self.assertGreater(indexes(), 0)

    def test_copy_constraints(self):
        """
        Test that copy_constraints controls whether integrity constraints are copied
        """
        self.sas.submit(f"proc datasets lib={SRC} nolist; modify cars; ic create nonull_model = not null(model); quit;")

        def constraints() -> int:
            self.sas.submit(f"""
                proc sql noprint;
                    select count(*) into :_cpic trimmed from dictionary.table_constraints
                    where table_catalog = "{DST.upper()}" and table_name = 'CARS';
                quit;
            """)
            return self.sas.symget('_cpic', outtype='int')

        self.helper_assert_copied(self.sas.copy('cars', SRC, DST, copy_constraints=False))
        self.assertEqual(constraints(), 0)

        self.helper_assert_copied(self.sas.copy('cars', SRC, DST, copy_constraints=True))
        self.assertGreater(constraints(), 0)

    def test_copy_timestamps(self):
        """
        Test that copy_timestamps=True keeps the creation date of the source data set
        """
        def crdate(libref: str) -> str:
            self.sas.submit(f"""
                proc sql noprint;
                    select put(crdate, datetime20.) into :_cpcr trimmed from dictionary.tables
                    where libname = "{libref.upper()}" and memname = 'CARS';
                quit;
            """)
            return self.sas.symget('_cpcr', outtype='str')

        self.helper_assert_copied(self.sas.copy('cars', 'sashelp', DST, copy_timestamps=True))
        self.assertEqual(crdate(DST), crdate('sashelp'))

        self.helper_assert_copied(self.sas.copy('cars', 'sashelp', DST))
        self.assertNotEqual(crdate(DST), crdate('sashelp'))

    def test_copy_force(self):
        """
        Test that force=True is required to move a data set with an audit trail
        """
        self.sas.submit(f"proc datasets lib={SRC} nolist; audit cars; initiate; quit;")

        log = self.sas.copy('cars', SRC, DST, move=True)
        self.assertTrue(self.helper_exist(SRC, 'cars'), msg="data set with audit trail moved without force")

        self.sas.check_error_log = False
        log = self.sas.copy('cars', SRC, DST, move=True, force=True)
        self.assertNotIn('ERROR', log)
        self.assertFalse(self.helper_exist(SRC, 'cars'))
        self.assertTrue(self.helper_exist(DST, 'cars'))

    def test_copy_encrypted(self):
        """
        Test copying an AES encrypted, alter protected data set with encryption_key and alter_password
        """
        self.sas.submit(f"data {SRC}.enc(encrypt=aes encryptkey='Secret' alter=pw); set sashelp.cars; run;")
        try:
            log = self.sas.copy('enc', SRC, DST, encryption_key='secret')
            self.assertIn('ERROR', log, msg="encryption key should be case sensitive")
            self.assertFalse(self.helper_exist(DST, 'enc'))

            self.sas.check_error_log = False
            log = self.sas.copy('enc', SRC, DST, encryption_key='Secret', alter_password='pw', move=True)
            self.helper_assert_copied(log)
            self.assertTrue(self.helper_exist(DST, 'enc'))
            self.assertFalse(self.helper_exist(SRC, 'enc'))
        finally:
            self.sas.submit(f"""
                proc datasets lib={SRC} nolist; delete enc(alter=pw); quit;
                proc datasets lib={DST} nolist; delete enc(alter=pw); quit;
            """)

    def test_copy_override_options(self):
        """
        Test that override_options are valid PROC COPY options when submitted
        """
        self.sas.submit(f"proc format lib={SRC}.formats; value yn 1='Yes' 0='No'; run;")

        log = self.sas.copy('formats', SRC, DST, override_options={'memtype': 'catalog'})

        self.helper_assert_copied(log)
        self.assertTrue(self.helper_exist(DST, 'formats', 'catalog'))
        self.assertFalse(self.helper_exist(DST, 'cars'))

    # ------------------------------------------------------------------
    # SASdata.copy
    # ------------------------------------------------------------------

    def helper_shape(self, libref: str, member: str) -> tuple:
        """
        Get the number of observations and variables of a data set.
        """
        self.sas.submit(f"""
            %let _cpnobs = ; %let _cpnvar = ;
            proc sql noprint;
                select nobs, nvar into :_cpnobs trimmed, :_cpnvar trimmed from dictionary.tables
                where libname = "{libref.upper()}" and memname = "{member.upper()}";
            quit;
        """)
        return self.sas.symget('_cpnobs', outtype='int'), self.sas.symget('_cpnvar', outtype='int')

    def helper_sasdata_shape(self, sd) -> tuple:
        """
        Get the number of observations and variables a SASdata object shows, with its dsopts applied.
        """
        log = self.sas.submit(f"data work._cpchk; set {sd.libref}.'{sd.table}'n {sd._dsopts()}; run;")['LOG']
        found = re.search(r'WORK\._CPCHK has (\d+) observations and (\d+) variables', log)
        return (int(found.group(1)), int(found.group(2))) if found else None

    def helper_sasdata_code(self, sd, **kwargs) -> list:
        """
        Get the code SASdata.copy prints in teach_me_SAS mode, as stripped, non-blank lines, and its return value.
        """
        captured = StringIO()
        with redirect_stdout(captured):
            self.sas.teach_me_SAS(True)
            try:
                ret = sd.copy(DST, **kwargs)
            finally:
                self.sas.teach_me_SAS(False)
        return [l.strip() for l in captured.getvalue().splitlines() if l.strip()], ret

    def test_sasdata_copy(self):
        """
        Test that SASdata.copy copies the data set and returns a SASdata object for the copy, leaving the original
        SASdata object pointing at the source, with lastlog() showing the PROC COPY log
        """
        sd = self.sas.sasdata('cars', SRC, results='text')

        sd2 = sd.copy(DST)

        self.assertIn('proc copy', self.sas.lastlog().lower(), msg="lastlog() is not the PROC COPY log")
        self.assertNotIn('ERROR', self.sas.lastlog())
        self.assertIsInstance(sd2, saspy.SASdata)
        self.assertEqual((sd2.table, sd2.libref, sd2.results), ('cars', DST, 'text'))
        self.assertEqual(self.helper_shape(DST, 'cars'), (428, 15))
        self.assertTrue(self.helper_exist(SRC, 'cars'))
        self.assertEqual(sd.libref, SRC)

    def test_sasdata_copy_syntax(self):
        """
        Test that teach_me_SAS mode prints PROC COPY for this data set as a name literal, with options passed through
        and the password masked, returns None and copies nothing
        """
        sd = self.sas.sasdata('cars', SRC)

        code, ret = self.helper_sasdata_code(sd, move=True, copy_indexes=False, alter_password='Pw9')

        self.assertIsNone(ret)
        self.assertEqual(code, [f"proc copy in={SRC} out={DST} move index=no alter='*****';", 'select cars;', 'run;'])
        self.assertFalse(self.helper_exist(DST, 'cars'))
        self.assertEqual(sd.libref, SRC)

    def test_sasdata_copy_name_literal(self):
        """
        Test that data sets whose names need a name literal (VALIDMEMNAME=EXTEND) are copied, with the literal in
        double quotes, in double quotes around a single quote, and in single quotes around an ampersand
        """
        NAMES = {'my cars': '"my cars"n', "it's": '"it\'s"n', 'a&b': "'a&b'n"}

        self.sas.submit(f"""
            %let _cpvmn = %sysfunc(getoption(validmemname));
            options validmemname=extend;
            data {SRC}."my cars"n {SRC}."it's"n {SRC}.'a&b'n; set sashelp.cars; run;
        """)
        try:
            for name, literal in NAMES.items():
                with self.subTest(name=name):
                    code, _ = self.helper_sasdata_code(self.sas.sasdata(name, SRC))
                    self.assertEqual(code[1], f'select {literal};')

                    sd2 = self.sas.sasdata(name, SRC).copy(DST)

                    self.assertIsInstance(sd2, saspy.SASdata)
                    self.assertEqual(sd2.table, name)
                    self.assertTrue(self.helper_exist(DST, name))
        finally:
            self.sas.submit("options validmemname=&_cpvmn;")

    def test_sasdata_copy_move(self):
        """
        Test that a move returns a SASdata object for the moved data set and leaves the original SASdata object
        unchanged; a move whose source can't be deleted copies the data set but returns None
        """
        sd2 = self.sas.sasdata('cars', SRC).copy(DST, move=True)

        self.assertEqual(sd2.libref, DST)
        self.assertTrue(self.helper_exist(DST, 'cars'))
        self.assertFalse(self.helper_exist(SRC, 'cars'))

        # The wrong alter password: PROC COPY copies the data set, then can't delete the source, which is an error
        self.sas.submit(f"data {SRC}.alt(alter=Pw9); set sashelp.cars; run;")
        sd = self.sas.sasdata('alt', SRC)
        try:
            with self.assertLogs('saspy', level='ERROR'):
                self.assertIsNone(sd.copy(DST, move=True, alter_password='wrong'))

            self.assertIn('Invalid or missing ALTER password', self.sas.lastlog())
            self.assertTrue(self.helper_exist(DST, 'alt'))
            self.assertTrue(self.helper_exist(SRC, 'alt'))
            self.assertEqual(sd.libref, SRC)
        finally:
            self.sas.submit(f"""
                proc datasets lib={SRC} nolist; delete alt(alter=Pw9); quit;
                proc datasets lib={DST} nolist; delete alt(alter=Pw9); quit;
            """)

    def test_sasdata_copy_error(self):
        """
        Test that a failed copy returns None, logs an error pointing to lastlog(), and leaves an older data set of the
        same name in the destination unchanged
        """
        self.sas.submit(f"data {SRC}.enc(encrypt=aes encryptkey='S3cret'); set sashelp.cars; run;")
        sd = self.sas.sasdata('enc', SRC)

        for existing in (False, True):
            with self.subTest(existing=existing):
                self.sas.submit(f"proc datasets lib={DST} kill nolist; quit;")
                if existing:
                    self.sas.submit(f"data {DST}.enc; set sashelp.class; run;")

                with self.assertLogs('saspy', level='ERROR') as logs:
                    self.assertIsNone(sd.copy(DST, encryption_key='wrong'))

                self.assertIn('Check lastlog()', logs.output[0])
                self.assertIn('Invalid ENCRYPTKEY value', self.sas.lastlog())
                self.assertEqual(self.helper_exist(DST, 'enc'), existing)
                if existing:
                    self.assertEqual(self.helper_shape(DST, 'enc'), (19, 5), msg="older data set was changed")

        with self.assertLogs('saspy', level='ERROR'):
            self.assertIsNone(self.sas.sasdata('notable', SRC).copy(DST))

    def test_sasdata_copy_after_error(self):
        """
        Test repeated submits after errors: each failed copy is reported, a copy after a failed copy succeeds, and an
        error in an earlier, unrelated submit doesn't make the next copy fail
        """
        self.sas.submit(f"data {SRC}.enc(encrypt=aes encryptkey='S3cret'); set sashelp.cars; run;")
        enc  = self.sas.sasdata('enc', SRC)
        cars = self.sas.sasdata('cars', SRC)

        for attempt in (1, 2):
            with self.subTest(failed_copy=attempt), self.assertLogs('saspy', level='ERROR'):
                self.assertIsNone(enc.copy(DST, encryption_key='wrong'))

        self.assertIsInstance(cars.copy(DST), saspy.SASdata)
        self.assertNotIn('ERROR', self.sas.lastlog())

        self.sas.submit("data _null_; set work.no_such_data_set; run;")
        self.assertIsInstance(enc.copy(DST, encryption_key='S3cret'), saspy.SASdata)
        self.assertEqual(self.helper_members(DST), {'CARS', 'ENC'})

    def test_sasdata_copy_messages(self):
        """
        Test that the SAS messages are printed when not in batch mode, unless quiet=True
        """
        sd = self.sas.sasdata('cars', SRC)
        self.sas.set_batch(False)
        try:
            for quiet in (False, True):
                with self.subTest(quiet=quiet):
                    captured = StringIO()
                    with redirect_stdout(captured):
                        sd2 = sd.copy(DST, quiet=quiet)

                    self.assertIsInstance(sd2, saspy.SASdata)
                    self.assertEqual('NOTE: Copying' in captured.getvalue(), not quiet)
        finally:
            self.sas.set_batch(True)

    def test_sasdata_copy_dsopts(self):
        """
        Test that the whole data set is copied, and the returned SASdata object has the same dsopts, as its own dict,
        so it shows the same subset of the copy
        """
        dsopts = {'where': 'msrp > 50000', 'keep': 'make model msrp'}
        sd = self.sas.sasdata('cars', SRC, dsopts=dsopts)

        sd2 = sd.copy(DST)

        self.assertEqual(self.helper_shape(DST, 'cars'), (428, 15))
        self.assertEqual(sd2.dsopts, dsopts)
        self.assertEqual(self.helper_sasdata_shape(sd2), (52, 3))

        sd2.dsopts['obs'] = 5
        self.assertNotIn('obs', sd.dsopts, msg="the returned SASdata object shares its dsopts dict")

    def test_sasdata_copy_dsopts_passwords(self):
        """
        Test that passwords in dsopts are passed to PROC COPY as written and replace the matching argument with a
        warning, and that the returned SASdata object can read the copy with them
        """
        SCENARIOS = {
            # name:          (source protection,                 dsopts passwords,             copy() arguments)
            'encryptkey':    ("encrypt=aes2 encryptkey='it''s'", {'encryptkey': "'it''s'"},    dict(encryption_key='wrong')),
            'ENCRYPTKEY':    ("encrypt=aes encryptkey='it''s'",  {'ENCRYPTKEY': "'it''s'"},    dict(encryption_key='wrong')),
            'pw, for move':  ("alter=Pw9",                       {'pw': 'Pw9'},                dict(alter_password='wrong', move=True)),
        }

        for name, (protection, passwords, arguments) in SCENARIOS.items():
            with self.subTest(dsopts=name):
                self.sas.submit(f"""
                    proc datasets lib={DST} kill nolist; quit;
                    data {SRC}.enc({protection}); set sashelp.cars; run;
                """)
                sd = self.sas.sasdata('enc', SRC, dsopts={'where': 'msrp > 50000', **passwords})
                try:
                    with self.assertLogs('saspy', level='WARNING') as logs:
                        sd2 = sd.copy(DST, **arguments)

                    self.assertIn('Passwords in dsopts', logs.output[0])
                    self.assertIsInstance(sd2, saspy.SASdata)
                    self.assertEqual(self.helper_sasdata_shape(sd2), (52, 15))
                finally:
                    self.sas.submit(f"""
                        proc datasets lib={SRC} nolist; delete enc(alter=Pw9); quit;
                        proc datasets lib={DST} nolist; delete enc(alter=Pw9); quit;
                    """)

    def test_sasdata_copy_dsopts_passwords_syntax(self):
        """
        Test that passwords in dsopts are added to the PROC COPY statement in place of the matching arguments and are
        masked in teach_me_SAS mode; an argument that doesn't match a dsopts password is kept, without a warning
        """
        sd = self.sas.sasdata('cars', SRC, dsopts={'where': 'msrp > 50000', 'encryptkey': "'it''s'", 'pw': 'Pw9'})

        with self.assertLogs('saspy', level='WARNING'):
            code, _ = self.helper_sasdata_code(sd, encryption_key='wrong', alter_password='wrong',
                                               override_options={'index': 'no'})

        self.assertEqual(code[0], f"proc copy in={SRC} out={DST} index=no encryptkey='*****' pw='*****';")

        sd = self.sas.sasdata('cars', SRC, dsopts={'alter': 'Pw9'})

        with self.assertRaises(AssertionError), self.assertLogs('saspy', level='WARNING'):
            code, _ = self.helper_sasdata_code(sd, encryption_key='k1')

        self.assertEqual(code[0], f"proc copy in={SRC} out={DST} encryptkey='*****' alter='*****';")

    def test_sasdata_copy_removed_arguments(self):
        """
        Test that the member list arguments of SASsession.copy, and the removed ignore_dsopts, are not accepted
        by SASdata.copy
        """
        sd = self.sas.sasdata('cars', SRC)

        for arg in ('exclude', 'member_types', 'ignore_dsopts'):
            with self.subTest(arg=arg):
                with self.assertRaises(TypeError):
                    sd.copy(DST, **{arg: True})


if __name__ == "__main__":
    unittest.main()
