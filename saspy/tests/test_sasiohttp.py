import unittest
from unittest.mock import MagicMock


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


if __name__ == "__main__":
    unittest.main()
