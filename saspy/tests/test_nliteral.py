import unittest
import saspy
import re


# Names that exercise every NLITERAL rule, with what SAS's NLITERAL function returns for each (written with n, which
# nliteral uses; NLITERAL writes N, which SAS treats the same). Used both to check nliteral directly and to compare
# it with NLITERAL itself in SAS.
EXPECTED = {
    # Valid SAS names are returned unchanged: an English letter or underscore, then letters, underscores or digits
    'cars':                     'cars',
    'Cars':                     'Cars',
    'CARS9':                    'CARS9',
    '_':                        '_',
    '_x1':                      '_x1',
    '__':                       '__',
    'A_B_C':                    'A_B_C',
    'a' * 32:                   'a' * 32,
    # NLITERAL doesn't check the 32 character limit
    'a' * 33:                   'a' * 33,
    'a' * 100:                  'a' * 100,

    # Anything else is a name literal in double quotes by default
    'my cars':                  '"my cars"n',
    '2024cars':                 '"2024cars"n',
    '123':                      '"123"n',
    'x-y':                      '"x-y"n',
    'x.y':                      '"x.y"n',
    'x$y':                      '"x$y"n',
    'x#y':                      '"x#y"n',
    'café':                '"café"n',

    # A single quote stays as it is inside double quotes
    "it's":                     '"it\'s"n',
    "'":                        '"\'"n',
    "''":                       '"\'\'"n',

    # Single quotes for an ampersand or percent sign, so macro references aren't resolved
    'a&b':                      "'a&b'n",
    'R&D':                      "'R&D'n",
    'a&&b':                     "'a&&b'n",
    'p%c':                      "'p%c'n",
    '%%':                       "'%%'n",
    '&':                        "'&'n",
    # ... and any single quotes are doubled inside them
    "a&b's":                    "'a&b''s'n",
    '%x\'"y':                   '\'%x\'\'"y\'n',
    'a&"b':                     '\'a&"b\'n',

    # Single quotes when there are more double quotes than single quotes
    'say "hi"':                 '\'say "hi"\'n',
    '"':                        '\'"\'n',
    '""':                       '\'""\'n',
    'x""y\'z':                  '\'x""y\'\'z\'n',

    # Double quotes when there are as many or more single quotes, with any double quotes doubled
    'x"y\'z':                   '"x""y\'z"n',
    'x"y\'\'z':                 '"x""y\'\'z"n',
    'both \' and "':            '"both \' and """n',

    # Trailing blanks are ignored
    'trail ':                   'trail',
    'trail   ':                 'trail',
    'my cars ':                 '"my cars"n',
}

# Leading blanks are removed too, as SAS drops them from names. NLITERAL keeps them in the name literal instead
BLANKS = {
    ' lead':                    'lead',
    '  a':                      'a',
    '  cars  ':                 'cars',
    '  my cars  ':              '"my cars"n',
    " it's ":                   '"it\'s"n',
    ' a&b':                     "'a&b'n",
}

# Names that are already name literals are returned unchanged. This is where nliteral differs from SAS's NLITERAL,
# which encloses them in quotes again. The value is the name the literal refers to in SAS.
LITERALS = {
    "'foo'n":                   'foo',
    '"bar"n':                   'bar',
    "'my cars'n":               'my cars',
    '"my cars"n':               'my cars',
    "'MY CARS'N":               'MY CARS',
    "'it''s'n":                 "it's",
    '"it\'s"n':                 "it's",
    '"say ""hi"""n':            'say "hi"',
    '\'say "hi"\'n':            'say "hi"',
    "'a&b'n":                   'a&b',
    "'p%c'n":                   'p%c',
}

# Strings that only look like name literals: they are enclosed in quotes as text, as NLITERAL does
NOT_LITERALS = {
    "'a'b'n":                   '"\'a\'b\'n"n',       # a single quote inside single quotes must be doubled
    '"a"b"n':                   '\'"a"b"n\'n',        # a double quote inside double quotes must be doubled
    "'foo'":                    '"\'foo\'"n',         # no n
    "foo'n":                    '"foo\'n"n',          # no opening quote
    "'foo'nx":                  '"\'foo\'nx"n',       # text after the n
    "x'foo'n":                  '"x\'foo\'n"n',       # text before the quote
    "'foo' n":                  '"\'foo\' n"n',       # a blank before the n
    "'foo'n'bar'n":             '"\'foo\'n\'bar\'n"n',  # two literals
    '\'foo"n':                  '"\'foo""n"n',        # mismatched quotes
}


# Macro references, with macro variables mydata=foo and D=elete defined. Each name: (what nliteral returns, the
# variable name SAS creates from it). Plain names are single quoted, so SAS never resolves & or % in them. A name
# literal passed in is returned unchanged: in double quotes SAS resolves it, in single quotes it doesn't.
MACRO_REFERENCES = {
    # plain names: kept exactly as written
    'R&D':                      ("'R&D'n",              'R&D'),
    '&mydata':                  ("'&mydata'n",          '&mydata'),
    '&mydata.x':                ("'&mydata.x'n",        '&mydata.x'),
    'a&&b':                     ("'a&&b'n",             'a&&b'),
    'it&s':                     ("'it&s'n",             'it&s'),
    '100%':                     ("'100%'n",             '100%'),
    '%upcase(foo)':             ("'%upcase(foo)'n",     '%upcase(foo)'),
    'P&L %':                    ("'P&L %'n",            'P&L %'),
    # name literals in double quotes: SAS resolves the macro references
    '"&mydata"n':               ('"&mydata"n',          'foo'),
    '"&mydata.x"n':             ('"&mydata.x"n',        'foox'),
    '"%upcase(foo)"n':          ('"%upcase(foo)"n',     'FOO'),
    '"R&D"n':                   ('"R&D"n',              'Relete'),
    # name literals in single quotes: SAS doesn't
    "'&mydata'n":               ("'&mydata'n",          '&mydata'),
    "'R&D'n":                   ("'R&D'n",              'R&D'),
}


class TestNliteral(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.sas = saspy.SASsession()
        cls.sas.set_batch(True)

    @classmethod
    def tearDownClass(cls):
        cls.sas._endsas()

    def helper_sas_nliteral(self, names: list) -> list:
        """
        Get what SAS's NLITERAL function returns for each name, with its N suffix written as n.
        """
        statements = []
        for i, name in enumerate(names):
            literal = name.replace("'", "''")
            statements.append(f"v = nliteral('{literal}'); put 'CPNL{i}|' v +(-1) '|';")

        log = self.sas.submit("data _null_; length v $200;\n" + "\n".join(statements) + "\nrun;")['LOG']
        found = dict(re.findall(r'^CPNL(\d+)\|(.*)\|\s*$', log, re.M))

        # PUT writes a blank value as one blank, and SAS ignores trailing blanks, so drop them
        return [re.sub(r'N$', 'n', found.get(str(i), '').rstrip(' ')) for i in range(len(names))]

    def test_nliteral_expected(self):
        """
        Test that nliteral returns the expected value for every rule
        """
        for name, expected in EXPECTED.items():
            with self.subTest(name=name):
                self.assertEqual(self.sas.nliteral(name), expected)

    def test_nliteral_matches_sas(self):
        """
        Test that nliteral returns the same as SAS's NLITERAL function, run in SAS, for every name that isn't
        already a name literal, including strings that only look like one
        """
        names = list(EXPECTED) + list(NOT_LITERALS)

        for name, sas_value in zip(names, self.helper_sas_nliteral(names)):
            with self.subTest(name=name):
                self.assertEqual(self.sas.nliteral(name), sas_value)

    def test_nliteral_existing_literal(self):
        """
        Test that a name that is already a name literal is returned unchanged, also with leading and trailing
        blanks, which are removed, and that SAS's NLITERAL would have enclosed it in quotes again
        """
        for name in LITERALS:
            with self.subTest(name=name):
                self.assertEqual(self.sas.nliteral(name), name)
                self.assertEqual(self.sas.nliteral(f'  {name}  '), name)

        for name, sas_value in zip(LITERALS, self.helper_sas_nliteral(list(LITERALS))):
            with self.subTest(sas_nliteral=name):
                self.assertNotEqual(sas_value, name)

    def test_nliteral_blanks(self):
        """
        Test that leading and trailing blanks are removed before the name is checked, where SAS's NLITERAL keeps
        leading blanks in the name literal
        """
        for name, expected in BLANKS.items():
            with self.subTest(name=name):
                self.assertEqual(self.sas.nliteral(name), expected)

        for name, sas_value in zip(BLANKS, self.helper_sas_nliteral(list(BLANKS))):
            with self.subTest(sas_nliteral=name):
                self.assertNotEqual(sas_value, BLANKS[name])

    def test_nliteral_not_a_literal(self):
        """
        Test that strings that only look like name literals are enclosed in quotes as text
        """
        for name, expected in NOT_LITERALS.items():
            with self.subTest(name=name):
                self.assertEqual(self.sas.nliteral(name), expected)

    def test_nliteral_existing_literal_usable_in_sas(self):
        """
        Test that a name literal returned unchanged still refers to the name it was written for: it is used to
        create a variable (VALIDVARNAME=ANY), and the variable's name in SAS must be the literal's name
        """
        self.sas.submit("%let _cpvvn = %sysfunc(getoption(validvarname)); options validvarname=any;")
        try:
            for literal, name in LITERALS.items():
                with self.subTest(literal=literal):
                    self.assertEqual(self.helper_variable_name(self.sas.nliteral(literal)), name)
        finally:
            self.sas.submit("options validvarname=&_cpvvn;")

    def test_nliteral_macro_references(self):
        """
        Test that SAS never resolves & or % in a plain name, even when matching macro variables exist, and that a
        name literal passed in decides it: SAS resolves macro references in double quotes and not in single quotes.
        No warnings, such as an unresolved macro reference, are expected
        """
        self.sas.symput('mydata', 'foo')
        self.sas.symput('D', 'elete')
        self.sas.submit("%let _cpvvn = %sysfunc(getoption(validvarname)); options validvarname=any;")
        try:
            for name, (literal, created) in MACRO_REFERENCES.items():
                with self.subTest(name=name):
                    self.assertEqual(self.sas.nliteral(name), literal)

                    log = self.sas.submit(f"data work._cpnl; {self.sas.nliteral(name)} = 1; run;")['LOG']
                    self.assertNotIn('WARNING', log)
                    self.assertEqual(self.helper_variable_name(literal), created)
        finally:
            self.sas.submit("options validvarname=&_cpvvn; %symdel mydata D / nowarn;")

    def helper_variable_name(self, literal: str) -> str:
        """
        Create a variable with the given name literal in SAS, and get the name SAS gave it.
        """
        self.sas.submit(f"data work._cpnl; {literal} = 1; run;")
        self.sas.submit("""
            %let _cpname = ;
            proc sql noprint;
                select name into :_cpname trimmed from dictionary.columns
                where libname = 'WORK' and memname = '_CPNL';
            quit;
        """)
        log = self.sas.submit("%put CPNAME|%superq(_cpname)|;")['LOG']
        return re.findall(r'^CPNAME\|(.*)\|\s*$', log, re.M)[-1]

    def test_nliteral_non_english_letters(self):
        """
        Test that letters outside A-Z make a name literal, including ones Python would otherwise match case
        insensitively against a-z (the long s and the Kelvin sign)
        """
        for name in ('café', 'straße', 'ſ', 'K', 'Ａ', 'naïve'):
            with self.subTest(name=name):
                self.assertEqual(self.sas.nliteral(name), f'"{name}"n')

    def test_nliteral_empty(self):
        """
        Test that an empty or all blank name raises ValueError, as it can't be a SAS name
        """
        for name in ('', ' ', '   '):
            with self.subTest(name=repr(name)):
                with self.assertRaises(ValueError):
                    self.sas.nliteral(name)

    def test_nliteral_type(self):
        """
        Test that nliteral returns a str and leaves its argument unchanged
        """
        name = 'my cars '

        result = self.sas.nliteral(name)

        self.assertIsInstance(result, str)
        self.assertEqual(name, 'my cars ')

    def test_nliteral_usable_in_sas(self):
        """
        Test that each name literal nliteral returns refers to exactly the original name in SAS: it is used to create
        a variable (VALIDVARNAME=ANY), and the variable's name in SAS must match, without leading or trailing
        blanks. Names longer than 32 characters can't be variables, so they are left out
        """
        names = [name for name in {**EXPECTED, **BLANKS} if len(name.strip()) <= 32]

        self.sas.submit("%let _cpvvn = %sysfunc(getoption(validvarname)); options validvarname=any;")
        try:
            for name in names:
                with self.subTest(name=name):
                    self.assertEqual(self.helper_variable_name(self.sas.nliteral(name)), name.strip())
        finally:
            self.sas.submit("options validvarname=&_cpvvn;")

    def test_nliteral_usable_as_member_name(self):
        """
        Test that name literals from nliteral can be used as data set names (VALIDMEMNAME=EXTEND) and found again.
        Data set names can't contain some characters, such as - and ", even with VALIDMEMNAME=EXTEND
        """
        names = ['my cars', "it's", "it''s", 'a&b', 'p%c', '%%', '2024cars', 'R&D dept']

        self.sas.submit("%let _cpvmn = %sysfunc(getoption(validmemname)); options validmemname=extend;")
        try:
            for name in names:
                with self.subTest(name=name):
                    log = self.sas.submit(f"data work.{self.sas.nliteral(name)}; x = 1; run;")['LOG']

                    self.assertNotIn('ERROR', log)
                    self.assertTrue(self.sas.exist(name, 'work'))
        finally:
            self.sas.submit("options validmemname=&_cpvmn;")


if __name__ == "__main__":
    unittest.main()
