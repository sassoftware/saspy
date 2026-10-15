from contextlib import redirect_stdout
from io import StringIO
import unittest
import saspy

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
        stmt = self.helper_proc_stmt(encryption_key='Secret', alter_password='pw')

        self.assertIn("encryptkey='Secret'", stmt)
        self.assertIn("alter='pw'", stmt)

    def test_copy_syntax_override_options(self):
        """
        Test that override_options are passed through as option=value
        """
        stmt = self.helper_proc_stmt(override_options={'memtype': 'data', 'index': 'no'})

        self.assertIn('memtype=data', stmt)
        self.assertIn('index=no', stmt)

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
        Test copying a data set with a name literal when VALIDMEMNAME=EXTEND
        """
        self.sas.submit(f"options validmemname=extend; data {SRC}.'my cars'n; set sashelp.cars; run;")
        try:
            log = self.sas.copy("'my cars'n", SRC, DST)

            self.helper_assert_copied(log)
            self.assertTrue(self.helper_exist(DST, 'my cars'))
        finally:
            self.sas.submit("options validmemname=compat;")

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


if __name__ == "__main__":
    unittest.main()
