import unittest
import saspy


class TestSASutil(unittest.TestCase):
    def setUp(self):
        # Use the first entry in the configuration list
        self.sas = saspy.SASsession(cfgname=saspy.SAScfg.SAS_config_names[0])
        self.assertIsInstance(self.sas, saspy.SASsession, msg="sas = saspy.SASsession(...) failed")
        procNeeded = ['hpimpute', 'hpbin', 'hpsample']
        if not self.procFound(procNeeded):
            self.skipTest("Not all of these procedures were found: %s" % str(procNeeded))

    def tearDown(self):
        if self.sas:
            self.sas._endsas()

    def procFound(self, plist: list) -> bool:
        assert isinstance(plist, list)
        for proc in plist:
            res = self.sas.submit("proc %s; run;" % proc)
            log = res['LOG'].splitlines()
            for line in log:
                if line == 'ERROR: Procedure %s not found.' % proc.upper():
                    return False
        return True

