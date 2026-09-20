import unittest
from unittest.mock import MagicMock, patch, create_autospec
import polars as pl
import io
import json
from saspy.sasioiom import SASsessionIOM
from saspy.sasiohttp import SASsessionHTTP

class TestPolarsIOMIntegration(unittest.TestCase):
    @patch('saspy.sasioiom.socks.socket')
    def test_sasdata2polars_iom_native_stream(self, mock_socket):
        mock_sb = MagicMock()
        mock_sb.sas_date_fmts = []
        mock_sb.sas_time_fmts = []
        mock_sb.sas_datetime_fmts = []
        
        io_obj = create_autospec(SASsessionIOM)
        io_obj._sb = mock_sb
        io_obj.sascfg = MagicMock()
        io_obj.sascfg.encoding = 'utf-8'
        io_obj.sascfg.lrecl = 32767
        io_obj._tomods1 = b'_tomods1'
        io_obj._logcnt.return_value = '1'
        
        # Add stdin for IOM
        mock_stdin = MagicMock()
        io_obj.stdin = [mock_stdin]
        
        log_meta = "LRECL= 80\nVARNUMS= 1\nVARLIST=\ncol1\n\nVARTYPE=\nN\n"
        log_fmt = "FMT_CATS=\nbest32.\n"
        
        io_obj.submit.side_effect = [
            {'LOG': log_meta, 'LST': ''},
            {'LOG': log_fmt, 'LST': ''}
        ]
        io_obj._asubmit.return_value = {'LOG': '', 'LST': ''}
        
        mock_sock_inst = MagicMock()
        mock_socket.return_value = mock_sock_inst
        
        csv_data = "1\x01\n2\x01\n3\x01\n"
        with patch('saspy.sasioiom._read_sock') as mock_read_sock:
            mock_read_sock.return_value = io.StringIO(csv_data)
            
            df = SASsessionIOM.sasdata2polars(io_obj, 'test_table', method='STREAM')
            
            self.assertIsInstance(df, pl.DataFrame)
            self.assertEqual(df.shape, (3, 1))
            self.assertEqual(df.columns, ['col1'])

    @patch('saspy.sasioiom.socks.socket')
    def test_polars2sasdata_iom_native_stream(self, mock_socket):
        mock_sb = MagicMock()
        mock_sb.sascei = 'utf-8'
        io_obj = create_autospec(SASsessionIOM)
        io_obj._sb = mock_sb
        io_obj.sascfg = MagicMock()
        io_obj.sascfg.encoding = 'utf-8'
        io_obj._tomods1 = b'_tomods1'

        df = pl.DataFrame({'a': [1, 2]})

        # Native STREAM path uses _asubmit and submit for datalines transfer
        io_obj._asubmit.return_value = {'LOG': '', 'LST': ''}
        io_obj.submit.return_value = {'LOG': '', 'LST': ''}

        res = SASsessionIOM.polars2sasdata(io_obj, df, 'table_a', method='STREAM')

        # IOM returns None on success; sasbase.py creates the SASdata object
        self.assertIsNone(res)
        self.assertTrue(io_obj._asubmit.called)
        # Verify datalines terminator was sent
        calls = [str(c) for c in io_obj._asubmit.call_args_list]
        self.assertTrue(any(';;;;' in c for c in calls))

class TestPolarsHTTPIntegration(unittest.TestCase):
    def test_sasdata2polars_http_native_stream(self):
        mock_sb = MagicMock()
        mock_sb.sas_date_fmts = []
        mock_sb.sas_time_fmts = []
        mock_sb.sas_datetime_fmts = []
        mock_sb.workpath = '/tmp/'
        
        io_obj = create_autospec(SASsessionHTTP)
        io_obj._sb = mock_sb
        io_obj.pid = '123'
        io_obj._uri_files = '/files'
        io_obj.sascfg = MagicMock()
        io_obj.sascfg.encoding = 'utf-8'
        io_obj.sascfg.lrecl = 32767
        io_obj.sascfg.HTTPConn = MagicMock()
        
        meta_js = {
            'count': 1,
            'items': [{'name': 'col1', 'type': 'FLOAT'}]
        }
        mock_resp = MagicMock()
        mock_resp.read.return_value = json.dumps(meta_js).encode('utf-8')
        io_obj.sascfg.HTTPConn.getresponse.return_value = mock_resp
        
        # Provide enough side effects for all submit calls
        io_obj.submit.side_effect = [
            {'LOG': 'success', 'LST': ''}, # for metadata code
            {'LOG': 'FMT_CATS=\nbest32.\n', 'LST': ''}, # for format info
            {'LOG': 'export success', 'LST': ''}, # for proc export
            {'LOG': 'cleanup success', 'LST': ''}, # for cleanup in finally block
            {'LOG': 'extra', 'LST': ''},
            {'LOG': 'extra', 'LST': ''}
        ]
        io_obj._asubmit.return_value = 'job_id'
        io_obj._getlog.return_value = 'log'
        
        data_resp = MagicMock()
        data_resp.read.side_effect = [b"col1\n1\n2\n3\n", b""]
        io_obj.sascfg.HTTPConn.getresponse.side_effect = [mock_resp, data_resp]
        
        with patch('polars.read_csv') as mock_pl_read:
            mock_pl_read.return_value = pl.DataFrame({'col1': [1, 2, 3]})
            
            df = SASsessionHTTP.sasdata2polars(io_obj, 'test_table', method='STREAM')
            
            self.assertIsInstance(df, pl.DataFrame)
            self.assertEqual(df.shape, (3, 1))

if __name__ == '__main__':
    unittest.main()
