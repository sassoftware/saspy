import unittest
from unittest.mock import MagicMock, patch
import json


class TestEndsasDeletesSession(unittest.TestCase):
    def _make_session(self, sess_started: bool):
        """Build a minimal SASsessionHTTP-like object with _endsas wired up."""
        from saspy.sasiohttp import SASsessionHTTP

        obj = object.__new__(SASsessionHTTP)  # skip __init__

        # Minimal state expected by _endsas
        mock_conn = MagicMock()
        mock_resp = MagicMock()
        mock_resp.read.return_value = b""
        mock_conn.getresponse.return_value = mock_resp

        mock_cfg = MagicMock()
        mock_cfg.HTTPConn = mock_conn
        mock_cfg._token = "fake-token"
        mock_cfg.verbose = False
        mock_cfg.sess_started = False  # mirrors SASconfigHTTP.__init__; never updated

        obj.sascfg = mock_cfg
        obj._session = {"id": "abc123"}  # pretend a session exists
        obj._uri_del = "/compute/sessions/abc123"
        obj._refthd = MagicMock()
        obj.pid = "abc123"
        obj._sb = MagicMock()
        obj.sess_started = sess_started  # the attribute under test

        return obj, mock_conn

    def test_new_session_issues_delete(self):
        """When sess_started=True, _endsas() must issue a DELETE request."""
        obj, mock_conn = self._make_session(sess_started=True)
        obj._endsas()
        mock_conn.request.assert_called_once()
        method, uri, *_ = mock_conn.request.call_args[0]
        self.assertEqual(method, "DELETE")
        self.assertEqual(uri, "/compute/sessions/abc123")

    def test_reused_session_skips_delete(self):
        """When sess_started=False (reuse), _endsas() must NOT issue a DELETE."""
        obj, mock_conn = self._make_session(sess_started=False)
        obj._endsas()
        mock_conn.request.assert_not_called()


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
        "links": [
            {"method": "GET", "rel": "state", "uri": "/jobs/1/state"},
            {"method": "PUT", "rel": "cancel", "uri": "/jobs/1/cancel"},
            {"method": "GET", "rel": "log", "uri": "/jobs/1/log"},
            {"method": "GET", "rel": "listing", "uri": "/jobs/1/listing"},
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
        sascfg.output = "html"
        sascfg._token = "fake-token"
        sascfg.encoding = "utf-8"
        sascfg.delay = 0
        sascfg.excpcnt = 5

        # --- sb (SASsession) mock ---
        sb = MagicMock()
        sb.HTML_Style = "HTMLBlue"

        io.sascfg = sascfg
        io._sb = sb
        io._session = {"id": "fake-session-id"}
        io._uri_exe = "/compute/sessions/fake/jobs"
        # Prevent __del__ from complaining when the mock object is garbage-collected.
        io._refthd = MagicMock()

        # --- Build mock HTTP connection ---
        # POST response: job accepted (200)
        post_req = MagicMock()
        post_req.status = 200
        post_req.read.return_value = json.dumps(self._FAKE_JOBID).encode("utf-8")

        # Sequence of state responses (initial GET + any polling calls)
        state_reqs = []
        for raw in poll_read_values:
            m = MagicMock()
            m.read.return_value = raw
            m.getheader.return_value = '"etag-1"'
            state_reqs.append(m)

        # Cancel PUT response
        cancel_req = MagicMock()
        cancel_req.read.return_value = b""

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

        io = self._make_io(poll_read_values=[b"running"])

        # First call to time.monotonic() sets _deadline = 0 + 10 = 10.
        # Second call (deadline check in the loop) returns 11 → deadline exceeded.
        with patch("saspy.sasiohttp.time.monotonic", side_effect=[0, 11]):
            with self.assertRaises(SASsubmitTimeout):
                io.submit("data _null_; run;", results="text", submit_timeout=10)

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
        io = self._make_io(poll_read_values=[b"completed"])

        with (
            patch.object(io, "_getlog", return_value="NOTE: success"),
            patch.object(io, "_getlsttxt", return_value=""),
        ):
            try:
                result = io.submit(
                    "data _null_; run;", results="text", submit_timeout=10
                )
            except SASsubmitTimeout:
                self.fail("SASsubmitTimeout was raised unexpectedly")

        self.assertIn("LOG", result)
        self.assertIn("LST", result)


if __name__ == "__main__":
    unittest.main()
