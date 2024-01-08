import unittest
import saspy


class TestSASViyaML(unittest.TestCase):

    def testSymgetOnDeadSession(self):
        sas = saspy.SASsession()
        
        sas.submit("endsas;")

        try:
            sas.SYSINFO()
        except ValueError as e:
            self.assertFalse(str(e) != "Failed to execute symexist. Your session may have prematurely terminated.")

if __name__ == '__main__':
    unittest.main()
