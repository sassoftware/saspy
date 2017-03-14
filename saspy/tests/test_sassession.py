import unittest
import saspy
import os
from IPython.utils.tempdir import TemporaryDirectory

class TestSASsessionObject(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.sas = saspy.SASsession() #cfgname='default')

    @classmethod
    def tearDownClass(cls):
        if cls.sas:
           cls.sas._endsas()


    def test_SASsession(self):
        self.assertIsInstance(self.sas, saspy.SASsession, msg="sas = saspy.SASsession(...) failed")

    def test_SASsession_exist(self):
        #test exist true
        exists = self.sas.exist('cars', libref='sashelp')
        self.assertTrue(exists, msg="exists = self.sas.exist(...) failed")

        #test exist false
        exists = self.sas.exist('notable', libref='sashelp')
        self.assertFalse(exists, msg="exists = self.sas.exist(...) failed")

    def test_SASsession_sasdata(self):
        #test sasdata existing
        cars = self.sas.sasdata('cars', libref='sashelp', results='text')
        self.assertIsInstance(cars, saspy.SASdata, msg="cars = sas.sasdata(...) failed")

        #test sasdata not existing
        notable = self.sas.sasdata('notable', results='text')
        self.assertIsInstance(notable, saspy.SASdata, msg="cars = sas.sasdata(...) failed")

        #test create non-existing table
        ll = self.sas.submit("data notable;x=1;run;")
        exists = self.sas.exist('notable')
        self.assertTrue(exists, msg="exists = self.sas.exist(...) failed")

    def test_SASsession_csv(self):
        # test write and read csv

        self.sas.set_batch(True)
        with TemporaryDirectory() as temppath:
            fname = os.path.join(temppath, 'sas_csv_test.csv')
            log = self.sas.write_csv(fname, 'cars', libref='sashelp')
            self.assertNotIn("ERROR", log, msg="sas.write_csv() failed")
            csvdata = self.sas.read_csv(fname, 'csvcars', results='text')
            ll = csvdata.head()
        expected = ['1', 'Acura', 'MDX', 'SUV', 'Asia', 'All', '$36,945', '$33,337', '3.5']
        rows = ll['LST'].splitlines()
        retrieved = []
        for i in range(len(rows)):
           retrieved.append(rows[i].split())
        self.assertIn(expected, retrieved, msg="csvcars.head() result didn't contain row 1")
        
    def test_SASsession_datasets(self):
        # test datasets()
        self.sas.set_batch(True)
        log = self.sas.datasets()
        expected = ['Libref', 'WORK']
        rows = log.splitlines()
        retrieved = []
        for i in range(len(rows)):
           retrieved.append(rows[i].split())
        self.assertIn(expected, retrieved, msg="cars.datasets() result didn't contain expected result")

        log = self.sas.datasets('sashelp')
        expected = ['Libref', 'SASHELP']
        rows = log.splitlines()
        retrieved = []
        for i in range(len(rows)):
           retrieved.append(rows[i].split())
           if i > 20:
              break  # it'll be in the first 20 rows for sure. don't need all of it
        self.assertIn(expected, retrieved, msg="cars.datasets(...) result didn't contain expected result")
        
    def test_SASsession_procobjs(self):
        # test stat
        stat = self.sas.sasstat()
        self.assertIsInstance(stat, saspy.SASstat, msg="stat = self.sas.sasstat() failed")

        # test ets
        ets = self.sas.sasets()
        self.assertIsInstance(ets, saspy.SASets, msg="ets = self.sas.sasets() failed")

        # test qc
        qc = self.sas.sasqc()
        self.assertIsInstance(qc, saspy.SASqc, msg="qc = self.sas.sasqc() failed")

        # test ml
        ml = self.sas.sasml()
        self.assertIsInstance(ml, saspy.SASml, msg="ml = self.sas.sasml() failed")

        # test util
        util = self.sas.sasutil()
        self.assertIsInstance(util, saspy.SASutil, msg="util = self.sas.sasutil() failed")

