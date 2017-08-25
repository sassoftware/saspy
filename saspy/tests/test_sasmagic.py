import unittest
from unittest.mock import patch, MagicMock, PropertyMock
from saspy.sas_magic import SASMagic
from saspy import SASsession

class TestSASMagic(unittest.TestCase):
    @classmethod    
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_sas_magic_existing_session(self):
        # mocked with existing session (mva)
        # shape: {shell: {user_ns: []}, mva: {submit: func()}}
        mock = MagicMock()
        mva = MagicMock()
        shell = MagicMock()
        submit = MagicMock(return_value=dict(LOG='log', LST='list'))

        type(mva).submit = PropertyMock(return_value=submit)
        type(mock).mva = PropertyMock(return_value=mva)
        type(shell).user_ns = PropertyMock(return_value=[])
        type(mock).shell = PropertyMock(return_value=shell)

        test_cell = 'proc print data=work.test; run;'
        SASMagic.SAS(mock, '', test_cell)

        self.assertEqual(submit.call_count, 1, msg=u'sas code was not submitted')
        submit.assert_called_with(test_cell)

    def test_sas_magic_supplied_session(self):
        # mocked with session option existing in namespace
        # shape: {shell: {user_ns: [existing_session]}, mva: None}
        mock = MagicMock()
        shell = MagicMock()

        mva = MagicMock(spec=SASsession)
        submit = MagicMock(return_value=dict(LOG='log', LST='list'))
        type(mva).submit = PropertyMock(return_value=submit)

        # existing_session (mva) is in user namespace
        user_ns = dict(existing_session=mva)
        type(shell).user_ns = PropertyMock(return_value=user_ns)
        type(mock).shell = PropertyMock(return_value=shell)
        # no preset mva 
        type(mock).mva = PropertyMock(return_value=None)

        test_cell = 'proc datasets; run;'
        SASMagic.SAS(mock, 'existing_session', test_cell)

        self.assertEqual(submit.called, True, msg=u'sas code was not submitted')
        submit.assert_any_call(test_cell)

        # now test with non-existing session; expect error
        submit.reset_mock()
        output = SASMagic.SAS(mock, 'bad_session', test_cell)
        self.assertEqual(submit.called, False)
        self.assertIn('Invalid SAS Session', output)

