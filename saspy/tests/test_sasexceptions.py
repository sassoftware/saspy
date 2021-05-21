from unittest import mock
import unittest
import saspy
import sys
import tempfile
import os


CONFIG_STDIO = """
SAS_config_names = ['default']
default = {'saspath': '/opt/sasinside/SASHome/SASFoundation/9.4/bin/sas_u8'}
"""
CONFIG_SSH = """
SAS_config_names = ['ssh']
ssh = {'saspath': '/opt/sasinside/SASHome/SASFoundation/9.4/bin/sas_en',
    'ssh': '/usr/bin/ssh',
    'host': 'remote.linux.host',
    'encoding': 'latin1',
    'options': ["-fullstimer"]}
"""
CONFIG_IOMWIN = """
SAS_config_names = ['iomwin']
iomwin = {'java': '/usr/bin/java',
    'iomhost': 'windows.iom.host',
    'iomport': 8591,
    'encoding': 'windows-1252',
    'classpath': '/dummy/path/to/saspyiom.jar'}
"""
CONFIG_INVALID = """
SAS_config_names = ['not_supported']
not_supported = {'whatever': 'some value'}
"""


class TestSASExceptions(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """
        Create dummy config files for test cases. Use `NamedTemporaryFile`
        instead of in-memory `StringIO` because `SASsession` expects a file
        path, not a file-like object when passed a `cfgfile`.
        """
        # STDIO config file
        with tempfile.NamedTemporaryFile('w', delete=False) as tf:
            tf.write(CONFIG_STDIO)
            cls.config_stdio = tf.name

        # SSH config file
        with tempfile.NamedTemporaryFile('w', delete=False) as tf:
            tf.write(CONFIG_SSH)
            cls.config_ssh = tf.name

        # Windows IOM config file
        with tempfile.NamedTemporaryFile('w', delete=False) as tf:
            tf.write(CONFIG_IOMWIN)
            cls.config_iomwin = tf.name

        # Invalid config file
        with tempfile.NamedTemporaryFile('w', delete=False) as tf:
            tf.write(CONFIG_INVALID)
            cls.config_invalid = tf.name

        # Empty config file
        with tempfile.NamedTemporaryFile('w', delete=False) as tf:
            tf.write('')
            cls.config_empty = tf.name

    @classmethod
    def tearDownClass(cls):
        """
        Clean up named temp files
        """
        os.unlink(cls.config_stdio)
        os.unlink(cls.config_ssh)
        os.unlink(cls.config_iomwin)
        os.unlink(cls.config_invalid)
        os.unlink(cls.config_empty)

    def tearDown(self):
        """
        Remove `sascfgfile` module after test.
        """
        if 'sascfgfile' in sys.modules:
            del sys.modules['sascfgfile']

    @mock.patch('os.name', 'nt')
    def test_raises_SASIONotSupportedError_stdio(self):
        """
        Test passing STDIO config option on Windows raises
        SASIONotSupportedError. Patch os.name to always return 'nt'
        even on non-Windows systems.
        """
        with self.assertRaises(saspy.SASIONotSupportedError):
            sas = saspy.SASsession(cfgfile=self.config_stdio)

    def test_raises_SASConfigNotValidError_invalid(self):
        """
        Test that passing an invalid config raises SASConfigNotValidError.
        """
        with self.assertRaises(saspy.SASConfigNotValidError):
            sas = saspy.SASsession(cfgfile=self.config_invalid)

    def test_raises_SASConfigNotValidError_empty(self):
        """
        Test that passing an empty config raises SASConfigNotValidError.
        """
        with self.assertRaises(saspy.SASConfigNotValidError):
            sas = saspy.SASsession(cfgfile=self.config_empty)

    def test_raises_SASConfigNotFoundError(self):
        """
        Test that an invalid config path raises SASConfigNotFoundError.
        """
        with self.assertRaises(saspy.SASConfigNotFoundError):
            sas = saspy.SASsession(cfgfile='path/to/nowhere.py')
