import unittest
import saspy
from saspy.sasexceptions import (SASIOConnectionTerminated,
                                 SASHTTPsubmissionError
                                )

class TestSASViyaML(unittest.TestCase):

    def testSymgetOnDeadSession(self):
        sas = saspy.SASsession()

        try:
           ll = sas.submit("endsas;")

           sas.SYSINFO()
        except ValueError as e:
            self.assertFalse(str(e) != "Failed to execute symexist. Your session may have prematurely terminated.")
        except (SASIOConnectionTerminated, SASHTTPsubmissionError) as e:
            print("Terminated as expected")

if __name__ == '__main__':
    unittest.main()
