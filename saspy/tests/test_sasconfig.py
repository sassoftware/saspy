import unittest
from unittest.mock import patch
import saspy

class TestSASconfigObject(unittest.TestCase):
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

    def test_SASconfig(self):
        # basic mock configuration
        bare_config = dict(
            saspath= '/fake/sas/path'
        )

        with patch.multiple('saspy.sasbase.SAScfg', default=bare_config):
            sascfg = saspy.sasiostdio.SASconfigSTDIO(sascfgname='default')

            self.assertEqual(sascfg.saspath, bare_config['saspath'], msg=u'saspath config was not used')
    
    def test_SASconfig_arguments(self):
        # test overrides with and without lock_down set
        locked = dict(lock_down=True)
        unlocked = dict(lock_down=False)

        unlocked_config = dict(
            saspath= '/some/fake/path'
        )

        with patch.multiple('saspy.sasbase.SAScfg', custom=unlocked_config, SAS_config_options=unlocked, create=True):
            overrides = dict(saspath= '/overridden/sas/path')
            sascfg = saspy.sasiostdio.SASconfigSTDIO(sascfgname='custom', **overrides)

            self.assertEqual(
                sascfg.saspath, 
                overrides['saspath'], 
                msg=u'override of config was disallowed with lock_down=False'
            )

        #test with lock_down enabled, should disallow override
        locked_config = dict(
            saspath= '/another/fake/path'
        )

        with patch.multiple('saspy.sasbase.SAScfg', custom=locked_config, SAS_config_options=locked, create=True):
            # prevent print() from logging warning in test console
            with patch('sys.stdout') as PrintMock:
                overrides = dict(saspath= '/another/overridden/sas/path')
                sascfg = saspy.sasiostdio.SASconfigSTDIO(sascfgname='custom', **overrides)

                self.assertEqual(
                    sascfg.saspath, 
                    locked_config['saspath'], 
                    msg=u'override of config was allowed with lock_down=True'
                )

    def test_ssh_config(self):
        # simple ssh mock configuration
        simple_ssh =dict(
            saspath= '/opt/sasinside/SASHome/SASFoundation/9.4/bin/sas_u8',
            ssh= '/bin/ssh',
            host= 'hostname',
        )

        with patch.multiple('saspy.sasbase.SAScfg', ssh=simple_ssh, SAS_config_names=['ssh'], create=True):
            sascfg = saspy.sasiostdio.SASconfigSTDIO(sascfgname='ssh')
            pgm, params = saspy.sasiostdio.SASsessionSTDIO._buildcommand({}, sascfg)

            self.assertEqual(pgm, simple_ssh['ssh'], msg=u'ssh config was not used')
            self.assertNotIn('-R', params, msg=u'ssh tunnel was used though not configured')
            self.assertNotIn('-p', params, msg=u'ssh alternate port was used though not configured')

        # mock ssh config with additional options
        ssh_config =dict(
            saspath= '/opt/sasinside/SASHome/SASFoundation/9.4/bin/sas_u8',
            ssh= '/bin/ssh-alt',
            host= 'hostname',
            port= 9922,
            tunnel= 9911,
            encoding= 'latin1'
        )

        with patch.multiple('saspy.sasbase.SAScfg', ssh=ssh_config, SAS_config_names=['ssh'], create=True):
            sascfg = saspy.sasiostdio.SASconfigSTDIO(sascfgname='ssh')
            pgm, params = saspy.sasiostdio.SASsessionSTDIO._buildcommand({}, sascfg)
            joined = ' '.join(params)

            self.assertEqual(pgm, ssh_config['ssh'], msg=u'ssh config was not used')
            self.assertIn('-R 9911:localhost:9911', joined, msg=u'ssh tunnel config was not used')
            self.assertIn('-p 9922', joined, msg=u'ssh port config was not used')

        # test that direct arguments are permitted 
        with patch.multiple(
            'saspy.sasbase.SAScfg', ssh=simple_ssh, SAS_config_names=['ssh'], create=True,
            SAS_config_options=dict(lock_down=False)
        ):
            sascfg = saspy.sasiostdio.SASconfigSTDIO(sascfgname='ssh', port=8888, tunnel=9999)
            pgm, params = saspy.sasiostdio.SASsessionSTDIO._buildcommand({}, sascfg)
            joined = ' '.join(params)

            self.assertIn('-R 9999:localhost:9999', joined, msg=u'ssh tunnel config argument was not used')
            self.assertIn('-p 8888', joined, msg=u'ssh port config argument was not used')

        # test that direct argument do not apply in lock_down mode
        with patch.multiple(
            'saspy.sasbase.SAScfg', ssh=simple_ssh, SAS_config_names=['ssh'], create=True,
            SAS_config_options=dict(lock_down=True)
        ):
            # prevent print() from logging warning in test console
            with patch('sys.stdout') as PrintMock:
                sascfg = saspy.sasiostdio.SASconfigSTDIO(sascfgname='ssh', port=8888, tunnel=9999)
                pgm, params = saspy.sasiostdio.SASsessionSTDIO._buildcommand({}, sascfg)
                joined = ' '.join(params)

                self.assertNotIn('-R', params, msg=u'ssh tunnel argument was allowed with lock_down=True')
                self.assertNotIn('-p', params, msg=u'ssh alternate port argument was allowed with lock_down=True')
