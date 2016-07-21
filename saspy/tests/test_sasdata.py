import unittest
import saspy


class TestSASdataObject(unittest.TestCase):
    @classmethod    
    def setUpClass(cls):
        cls.sas = saspy.SASsession() #cfgname='default')
        #cls.assertIsInstance(cls.sas, saspy.SASsession, msg="sas = saspy.SASsession(...) failed")

    @classmethod
    def tearDownClass(cls):
        if cls.sas:
           cls.sas._endsas()

    def test_SASdata(self):
        #test sasdata method
        cars = self.sas.sasdata('cars', libref='sashelp', results='text')
        self.assertIsInstance(cars, saspy.SASdata, msg="cars = sas.sasdata(...) failed")

    def test_SASdata_batch(self):
        #test set_batch()
        cars = self.sas.sasdata('cars', libref='sashelp', results='text')
        self.sas.set_batch(True)
        ll = cars.head()
        self.assertIsInstance(ll, dict, msg="set_batch(True) didn't return dict")

    def test_SASdata_head(self):
        #test head()
        cars = self.sas.sasdata('cars', libref='sashelp', results='text')
        self.sas.set_batch(True)
        ll = cars.head()
        expected = ['1', 'Acura', 'MDX', 'SUV', 'Asia', 'All', '$36,945', '$33,337',
                    '3.5', '6', '265', '17', '23', '4451', '106', '189']
        rows = ll['LST'].splitlines()
        retrieved = []
        for i in range(len(rows)):
           retrieved.append(rows[i].split())
        self.assertIn(expected, retrieved, msg="cars.head() result didn't contain row 1")

    def test_SASdata_tail(self):
        #test tail()
        cars = self.sas.sasdata('cars', libref='sashelp', results='text')
        self.sas.set_batch(True)
        ll = cars.tail()
        expected = ['424', 'Volvo', 'C70', 'LPT', 'convertible', '2dr', 'Sedan', 'Europe', 'Front',
                    '$40,565', '$38,203', '2.4', '5', '197', '21', '28', '3450', '105', '186']
        rows = ll['LST'].splitlines()
        retrieved = []
        for i in range(len(rows)):
           retrieved.append(rows[i].split())
        self.assertIn(expected, retrieved, msg="cars.tail() result didn't contain row 1")

    def test_SASdata_contents(self):
        #test contents()
        cars = self.sas.sasdata('cars', libref='sashelp', results='text')
        self.sas.set_batch(True)
        ll = cars.contents()
        expected = ['Data', 'Set', 'Name', 'SASHELP.CARS', 'Observations', '428']
        rows = ll['LST'].splitlines()
        retrieved = []
        for i in range(len(rows)):
           retrieved.append(rows[i].split())
        self.assertIn(expected, retrieved, msg="cars.contents() result didn't contain expected result")
        
    def test_SASdata_describe(self):
        #test describe()
        cars = self.sas.sasdata('cars', libref='sashelp', results='text')
        self.sas.set_batch(True)
        ll = cars.describe()
        expected = ['MSRP', '428', '32774.86', '19431.72', '10280.00', '20329.50', '27635.00', '39215.00', '192465.00']
        rows = ll['LST'].splitlines()
        retrieved = []
        for i in range(len(rows)):
           retrieved.append(rows[i].split())
        self.assertIn(expected, retrieved, msg="cars.contents() result didn't contain expected result")
        
    def test_SASdata_results(self):
        #test set_results()
        cars = self.sas.sasdata('cars', libref='sashelp', results='text')
        self.sas.set_batch(True)
        cars.set_results('HTML')
        ll = cars.describe()
        expected = '<!DOCTYPE html>'
        row1 = ll['LST'].splitlines()[0]
        self.assertEqual(expected, row1, msg="cars.set_results() result weren't HTML")
        
        cars.set_results('TEXT')
        ll = cars.describe()
        row1 = ll['LST'].splitlines()[0]
        self.assertNotEqual(expected, row1, msg="cars.set_results() result weren't TEXT")

    def test_SASdata_hist(self):
        #test hist()
        cars = self.sas.sasdata('cars', libref='sashelp', results='text')
        self.sas.set_batch(True)
        cars.set_results('TEXT')
        ll = cars.hist('MSRP')
        expected = 'alt="The SGPlot Procedure" src="data:image/png;base64'
        self.assertIsInstance(ll, dict, msg="cars.hist(...) didn't return dict")
        self.assertGreater(len(ll['LST']), 40000, msg="cars.hist(...) result were too short")
        self.assertIn(expected, ll['LST'], msg="cars.hist(...) result weren't what was expected")
        cars.set_results('HTML')
        
    def test_SASdata_series(self):
        #test series()
        self.sas.set_batch(True)
        ll = self.sas.submit('''proc sql; 
                                create table sales as 
                                select month, sum(actual) as tot_sales, sum(predict) as predicted_sales 
                                from sashelp.prdsale 
                                group by 1 
                                order by month ;quit;
                             ''')
        sales = self.sas.sasdata('sales') 
        ll = sales.series(y=['tot_sales','predicted_sales'], x='month', title='total vs. predicted sales')
        expected = 'alt="The SGPlot Procedure" src="data:image/png;base64'
        self.assertIsInstance(ll, dict, msg="cars.series(...) didn't return dict")
        self.assertGreater(len(ll['LST']), 70000, msg="cars.series(...) result were too short")
        self.assertIn(expected, ll['LST'], msg="cars.series(...) result weren't what was expected")
        
    def test_SASdata_heatmap(self):
        #test heatmap()
        cars = self.sas.sasdata('cars', libref='sashelp', results='text')
        self.sas.set_batch(True)
        ll = cars.heatmap('MSRP','horsepower')
        expected = 'alt="The SGPlot Procedure" src="data:image/png;base64'
        self.assertIsInstance(ll, dict, msg="cars.heatmap(...) didn't return dict")
        self.assertGreater(len(ll['LST']), 30000, msg="cars.heatmap(...) result were too short")
        self.assertIn(expected, ll['LST'], msg="cars.heatmap(...) result weren't what was expected")
        
    def test_SASdata_sort1(self):
        # Create dataset in WORK
        self.sas.submit("data cars; set sashelp.cars; id=_n_;run;")
        wkcars = self.sas.sasdata('cars')
        # Sort data in place by one variable
        wkcars.sort('type')
        self.assertIsInstance(wkcars, saspy.SASdata, msg="Sort didn't return SASdata Object")
        
    def test_SASdata_sort2(self):
        # Create dataset in WORK
        self.sas.submit("data cars; set sashelp.cars; id=_n_;run;")
        wkcars = self.sas.sasdata('cars')
        # Sort data in plce by multiple variables
        wkcars.sort('type descending origin')
        self.assertIsInstance(wkcars, saspy.SASdata, msg="Sort didn't return SASdata Object")
        
    def test_SASdata_sort3(self):
        # Create dataset in WORK
        self.sas.submit("data cars; set sashelp.cars; id=_n_;run;")
        wkcars = self.sas.sasdata('cars')
        # create a second object pointing to the same data set
        dup=wkcars.sort('type')
        self.assertEqual(wkcars, dup, msg="Sort objects are not equal but should be")
        
    def test_SASdata_sort4(self):
        # Create dataset in WORK
        self.sas.submit("data cars; set sashelp.cars; id=_n_;run;")
        wkcars = self.sas.sasdata('cars')
        # create a second object with a different sort order
        diff=self.sas.sasdata('diff')
        diff=wkcars.sort('origin',diff)
        self.assertNotEqual(wkcars, diff, msg="Sort objects are equal but should not be")
        
    def test_SASdata_sort5(self):
        # Create dataset in WORK
        self.sas.submit("data cars; set sashelp.cars; id=_n_;run;")
        wkcars = self.sas.sasdata('cars')
        # create object within call
        wkcars.sort('type')
        out1=wkcars.sort('origin', self.sas.sasdata('out1'))
        self.assertIsInstance(out1, saspy.SASdata, msg="Sort didn't return new SASdata Object")
        self.assertNotEqual(wkcars, out1, msg="Sort objects are equal but should not be")
        
    def test_SASdata_sort6(self):
        # Create dataset in WORK
        self.sas.submit("data cars; set sashelp.cars; id=_n_;run;")
        wkcars = self.sas.sasdata('cars')
        # sort by missing variable
        self.assertRaises(RuntimeError, lambda: wkcars.sort('foobar'))
        
        
        
        