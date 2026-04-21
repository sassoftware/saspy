from unittest import mock
from unittest.mock import MagicMock, patch
import json
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


class TestSASsubmitTimeout(unittest.TestCase):
    """
    Tests for the submit_timeout kwarg added to sasiohttp.SASsessionHTTP.submit().

    These tests use unittest.mock to avoid requiring a live SAS Compute server.
    The HTTP polling loop is faked so that:
      - The job POST succeeds and returns a fake job descriptor.
      - The initial state GET returns b'running'.
      - time.monotonic() is controlled to simulate deadline expiry or non-expiry.
    """

    # Fake job descriptor returned by the POST /jobs endpoint.
    _FAKE_JOBID = {
        'links': [
            {'method': 'GET', 'rel': 'state',  'uri': '/jobs/1/state'},
            {'method': 'PUT', 'rel': 'cancel', 'uri': '/jobs/1/cancel'},
            {'method': 'GET', 'rel': 'log',    'uri': '/jobs/1/log'},
            {'method': 'GET', 'rel': 'listing', 'uri': '/jobs/1/listing'},
        ]
    }

    def _make_io(self, poll_read_values):
        """
        Return a SASsessionHTTP instance whose HTTP calls are fully mocked.

        poll_read_values: list of bytes that conn.getresponse().read() returns
        for the initial state GET and any subsequent polling calls, in order.
        A cancel PUT response (b'') is appended automatically.
        """
        from saspy.sasiohttp import SASsessionHTTP

        io = object.__new__(SASsessionHTTP)

        # --- sascfg mock ---
        sascfg = MagicMock()
        sascfg.output   = 'html'
        sascfg._token   = 'fake-token'
        sascfg.encoding = 'utf-8'
        sascfg.delay    = 0
        sascfg.excpcnt  = 5

        # --- sb (SASsession) mock ---
        sb = MagicMock()
        sb.HTML_Style = 'HTMLBlue'

        io.sascfg    = sascfg
        io._sb       = sb
        io._session  = {'id': 'fake-session-id'}
        io._uri_exe  = '/compute/sessions/fake/jobs'
        # Prevent __del__ from complaining when the mock object is garbage-collected.
        io._refthd   = MagicMock()

        # --- Build mock HTTP connection ---
        # POST response: job accepted (200)
        post_req = MagicMock()
        post_req.status = 200
        post_req.read.return_value = json.dumps(self._FAKE_JOBID).encode('utf-8')

        # Sequence of state responses (initial GET + any polling calls)
        state_reqs = []
        for raw in poll_read_values:
            m = MagicMock()
            m.read.return_value = raw
            m.getheader.return_value = '"etag-1"'
            state_reqs.append(m)

        # Cancel PUT response
        cancel_req = MagicMock()
        cancel_req.read.return_value = b''

        conn = MagicMock()
        conn.getresponse.side_effect = [post_req] + state_reqs + [cancel_req]
        sascfg.HTTPConn = conn

        return io

    def test_raises_SASsubmitTimeout_when_deadline_exceeded(self):
        """
        submit() raises SASsubmitTimeout when the job is still running and the
        wall-clock deadline has been exceeded.

        time.monotonic is patched so the deadline is immediately considered
        exceeded on the first iteration of the polling loop, keeping the test
        fast and deterministic.
        """
        from saspy.sasexceptions import SASsubmitTimeout

        io = self._make_io(poll_read_values=[b'running'])

        # First call to time.monotonic() sets _deadline = 0 + 10 = 10.
        # Second call (deadline check in the loop) returns 11 → deadline exceeded.
        with patch('saspy.sasiohttp.time.monotonic', side_effect=[0, 11]):
            with self.assertRaises(SASsubmitTimeout):
                io.submit('data _null_; run;', results='text', submit_timeout=10)

    def test_no_exception_when_job_completes_before_deadline(self):
        """
        submit() returns normally when the job completes before the deadline.

        The initial state GET returns b'completed', so done is set to True
        immediately and the polling loop is never entered. submit_timeout is
        set but should never cause a raise.
        """
        from saspy.sasexceptions import SASsubmitTimeout

        # Patch _getlog and _getlsttxt so the method can finish without HTTP calls
        # for log/listing retrieval.
        io = self._make_io(poll_read_values=[b'completed'])

        with patch.object(io, '_getlog',    return_value='NOTE: success'), \
             patch.object(io, '_getlsttxt', return_value=''):
            try:
                result = io.submit('data _null_; run;', results='text', submit_timeout=10)
            except SASsubmitTimeout:
                self.fail("SASsubmitTimeout was raised unexpectedly")

        self.assertIn('LOG', result)
        self.assertIn('LST', result)
