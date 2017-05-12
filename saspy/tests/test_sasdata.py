import unittest
import saspy
import os
import pandas as pd
from IPython.utils.tempdir import TemporaryDirectory
from pandas.util.testing import assert_frame_equal


class TestSASdataObject(unittest.TestCase):
    @classmethod    
    def setUpClass(cls):
        cls.sas = saspy.SASsession(results='HTML') #cfgname='default')
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

    @unittest.skip("Test failes with extra header info")
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

    def test_SASdata_tailPD(self):
        #test tail()
        cars = self.sas.sasdata('cars', libref='sashelp', results='pandas')
        self.sas.set_batch(True)
        ll = cars.tail()
        self.assertEqual(ll.shape, (5,15), msg="wrong shape returned")
        self.assertIsInstance(ll, pd.DataFrame, "Is return type correct")

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
        expected = ['MSRP', '428', '0', '27635', '32775', '19432', '10280', '20330', '27635']
        rows = ll['LST'].splitlines()
        retrieved = []
        for i in range(len(rows)):
           retrieved.append(rows[i].split())
        self.assertIn(expected, retrieved, msg="cars.describe() result didn't contain expected result")
        
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

    def test_SASdata_score1(self):
        # Create dataset in WORK
        self.sas.submit("data cars; set sashelp.cars; id=_n_;run;")
        wkcars = self.sas.sasdata('cars')
        a = wkcars.columnInfo()
        wkcars.score(code='P_originUSA = origin;')
        b = wkcars.columnInfo()
        self.assertNotEqual(a, b, msg="B should have an extra column P_originUSA")

    def test_SASdata_score2(self):
        # Create dataset in WORK
        self.sas.submit("data cars; set sashelp.cars; id=_n_;run;")
        wkcars = self.sas.sasdata('cars')
        wkcars.set_results('PANDAS')
        wkcars2 = self.sas.sasdata('cars2', 'work')
        wkcars2.set_results('PANDAS')
        a = wkcars.columnInfo()
        wkcars.score(code='P_originUSA = origin;', out=wkcars2)
        b = wkcars.columnInfo()
        self.assertFalse(assert_frame_equal(a, b), msg="B should be identical to a")
        self.assertIsInstance(wkcars2, saspy.sasbase.SASdata, "Does out dataset exist")

    def test_SASdata_score3(self):
        with TemporaryDirectory() as temppath:
            with open(os.path.join(temppath, 'score.sas'), 'w') as f:
                f.write('P_originUSA = origin;')
        # Create dataset in WORK
        self.sas.submit("data cars; set sashelp.cars; id=_n_;run;")
        wkcars = self.sas.sasdata('cars')
        wkcars.set_results('PANDAS')
        wkcars2 = self.sas.sasdata('cars2', 'work')
        wkcars2.set_results('PANDAS')
        a = wkcars.columnInfo()
        wkcars.score(file=f.name, out=wkcars2)
        b = wkcars.columnInfo()
        self.assertFalse(assert_frame_equal(a, b), msg="B should be identical to a")
        self.assertIsInstance(wkcars2, saspy.sasbase.SASdata, "Does out dataset exist")

    def test_SASdata_score4(self):
        with TemporaryDirectory() as temppath:
            with open(os.path.join(temppath, 'score.sas'), 'w') as f:
                f.write('P_originUSA = origin;')
        # Create dataset in WORK
        self.sas.submit("data cars; set sashelp.cars; id=_n_;run;")
        wkcars = self.sas.sasdata('cars')
        a = wkcars.columnInfo()
        wkcars.score(file=f.name)
        b = wkcars.columnInfo()
        self.assertNotEqual(a, b, msg="B should have an extra column P_originUSA")

    def test_regScoreAssess(self):
        stat = self.sas.sasstat()
        self.sas.submit("""
        data work.class;
            set sashelp.class;
        run;
        """)
        tr = self.sas.sasdata("class", "work")
        tr.set_results('PANDAS')
        with TemporaryDirectory() as temppath:
            fname = os.path.join(temppath, 'hpreg_code.sas')
            b = stat.hpreg(data=tr, model='weight=height', code=fname)
            tr.score(file=os.path.join(temppath, 'hpreg_code.sas'))
            # check that p_weight is in columnInfo
            self.assertTrue('P_Weight ' in tr.columnInfo()['Variable'].values, msg="Prediction Column not found")

        res1 = tr.assessModel(target = 'weight', prediction='P_weight', nominal=False)
        a = ['ASSESSMENTBINSTATISTICS', 'ASSESSMENTSTATISTICS', 'LOG']
        self.assertEqual(sorted(a), sorted(res1.__dir__()),
                         msg=u" model failed to return correct objects expected:{0:s}  returned:{1:s}".format(
                             str(a), str(b)))
        self.assertIsInstance(res1, saspy.SASresults, "Is return type correct")

    def test_regScoreAssess2(self):
        stat = self.sas.sasstat()
        self.sas.submit("""
        data work.class;
            set sashelp.class;
        run;
        """)
        tr = self.sas.sasdata("class", "work")
        tr.set_results('PANDAS')
        with TemporaryDirectory() as temppath:
            fname = os.path.join(temppath, 'hplogistic_code.sas')
            b = stat.hplogistic(data=tr, model='sex = weight height', code=fname)
            tr.score(file=fname)
            # check that p_weight is in columnInfo
            self.assertTrue('P_SexF ' in tr.columnInfo()['Variable'].values, msg="Prediction Column not found")

        res1 = tr.assessModel(target = 'sex', prediction='P_SexF', nominal=True, event='F')
        a = ['ASSESSMENTBINSTATISTICS', 'ASSESSMENTSTATISTICS', 'LOG', 'SGPLOT']
        self.assertEqual(sorted(a), sorted(res1.__dir__()),
                         msg=u" model failed to return correct objects expected:{0:s}  returned:{1:s}".format(
                             str(a), str(b)))
        self.assertIsInstance(res1, saspy.SASresults, "Is return type correct")

    def test_partition1(self):
        self.sas.submit("""
                data work.class;
                    set sashelp.class;
                run;
                """)
        tr = self.sas.sasdata("class", "work")
        tr.set_results('PANDAS')
        tr.partition(var='sex', fraction = .5, kfold=1, out=None, singleOut=True)
        self.assertTrue('_PartInd_ ' in tr.columnInfo()['Variable'].values, msg="Partition Column not found")

    def test_partition2(self):
        self.sas.submit("""
                data work.class;
                    set sashelp.class;
                run;
                """)
        tr = self.sas.sasdata("class", "work")
        tr.set_results('PANDAS')
        tr.partition(var='sex', fraction = .5, kfold=2, out=None, singleOut=True)
        self.assertTrue('_cvfold2 ' in tr.columnInfo()['Variable'].values, msg="Partition Column not found")

    def test_partition3(self):
        self.sas.submit("""
                data work.class;
                    set sashelp.class;
                run;
                """)
        tr = self.sas.sasdata("class", "work")
        out = self.sas.sasdata("class2", "work")
        tr.set_results('PANDAS')
        out.set_results('PANDAS')
        tr.partition(var='sex', fraction = .5, kfold=2, out=out, singleOut=True)
        self.assertFalse('_cvfold1 ' in tr.columnInfo()['Variable'].values, msg="Writing to wrong table")
        self.assertFalse('_PartInd_ ' in tr.columnInfo()['Variable'].values, msg="Writing to wrong table")
        self.assertTrue('_cvfold2 ' in out.columnInfo()['Variable'].values, msg="Partition Column not found")

    def test_partition4(self):
        self.sas.submit("""
                data work.class;
                    set sashelp.class;
                run;
                """)
        tr = self.sas.sasdata("class", "work")
        out = self.sas.sasdata("class2", "work")
        tr.set_results('PANDAS')
        out.set_results('PANDAS')
        res1 = tr.partition(var='sex', fraction = .5, kfold=2, out=out, singleOut=False)
        self.assertFalse('_cvfold1 ' in tr.columnInfo()['Variable'].values, msg="Writing to wrong table")
        self.assertFalse('_PartInd_ ' in tr.columnInfo()['Variable'].values, msg="Writing to wrong table")
        self.assertTrue('_cvfold2 ' in out.columnInfo()['Variable'].values, msg="Partition Column not found")
        self.assertIsInstance(res1, list, "Is return type correct")
        self.assertIsInstance(res1[0], tuple, "Is return type correct")
        self.assertIsInstance(res1[0][1], saspy.SASdata, "Is return type correct")

    def test_partition5(self):
        self.sas.submit("""
                data work.class;
                    set sashelp.class;
                run;
                """)
        tr = self.sas.sasdata("class", "work")
        tr.set_results('PANDAS')
        tr.partition(fraction = .5, kfold=1, out=None, singleOut=True)
        self.assertTrue('_PartInd_ ' in tr.columnInfo()['Variable'].values, msg="Partition Column not found")
        
    def test_info1(self):
        tr = self.sas.sasdata("class", "sashelp")
        tr.set_results('Pandas')
        res = tr.info()
        self.assertIsInstance(res, pd.DataFrame, msg= 'Data frame not returned')
        self.assertEqual(res.shape, (5, 4), msg="wrong shape returned")

    def test_info2(self):
        tr = self.sas.sasdata("class", "sashelp")
        tr.set_results('text')
        res = tr.info()
        self.assertIsNone(res, msg = "only works with Pandas" )

    def test_info3(self):
        tr = self.sas.sasdata("class", "sashelp")
        tr.set_results('html')
        res = tr.info()
        self.assertIsNone(res, msg="only works with Pandas")
