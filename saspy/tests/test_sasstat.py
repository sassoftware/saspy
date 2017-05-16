import unittest
import saspy
import pandas as pd


class TestSASstat(unittest.TestCase):
    def setUp(self):
        # Use the first entry in the configuration list
        self.sas = saspy.SASsession() #cfgname=saspy.SAScfg.SAS_config_names[0])
        self.assertIsInstance(self.sas, saspy.SASsession, msg="sas = saspy.SASsession(...) failed")
        procNeeded=['reg', 'mixed', 'hpsplit', 'hplogistic', 'hpreg', 'glm', 'logistic', 'tpspline']
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
                if line=='ERROR: Procedure %s not found.' % proc.upper():
                    return False
        return True

    def test_smokeReg(self):
        # Basic model returns objects
        stat = self.sas.sasstat()
        tr = self.sas.sasdata("class", "sashelp")
        # REG
        b = stat.reg(data=tr, model='weight=height')
        a = ['ANOVA', 'COOKSDPLOT', 'DFBETASPANEL', 'DFFITSPLOT', 'DIAGNOSTICSPANEL', 'FITPLOT', 'FITSTATISTICS',
             'LOG', 'NOBS', 'OBSERVEDBYPREDICTED', 'PARAMETERESTIMATES', 'QQPLOT', 'RESIDUALBOXPLOT',
             'RESIDUALBYPREDICTED',
             'RESIDUALHISTOGRAM', 'RESIDUALPLOT', 'RFPLOT', 'RSTUDENTBYLEVERAGE', 'RSTUDENTBYPREDICTED']
        self.assertEqual(sorted(a), sorted(b.__dir__()),
                         msg=u"Simple Regession (reg) model failed to return correct objects expected:{0:s}  returned:{1:s}".format(
                             str(a), str(b)))

    def regResult1(self):
        stat = self.sas.sasstat()
        tr = self.sas.sasdata("class", "sashelp")
        b = stat.reg(data=tr, model='weight=height')
        self.assertIsInstance(b, saspy.SASresults, msg="correct return type")

    def regResult2(self):
        stat = self.sas.sasstat()
        tr = self.sas.sasdata("class", "sashelp")
        tr.set_results('PANDAS')
        b = stat.reg(data=tr, model='weight=height')
        self.assertIsInstance(b.ANOVA, pandas.core.frame.DataFrame, msg="correct return type")

    def regResult3(self):
        stat = self.sas.sasstat()
        tr = self.sas.sasdata("class", "sashelp")
        tr.set_results('PANDAS')
        b = stat.reg(data=tr, model='weight=height')
        self.assertIsInstance(b.LOG, IPython.core.display.HTML, msg="correct return type")

    def regResult4(self):
        stat = self.sas.sasstat()
        tr = self.sas.sasdata("class", "sashelp")
        tr.set_results('PANDAS')
        b = stat.reg(data=tr, model='weight=height')
        self.assertIsInstance(b.RESIDUALHISTOGRAM, IPython.core.display.HTML, msg="correct return type")


    def test_smokeMixed(self):
        # Basic model returns objects
        stat = self.sas.sasstat()
        tr = self.sas.sasdata("class", "sashelp")
        b = stat.mixed(data=tr, model='weight=height')
        a = ['COVPARMS', 'DIMENSIONS', 'FITSTATISTICS', 'LOG', 'MODELINFO', 'NOBS', 'PEARSONPANEL',
             'RESIDUALPANEL', 'STUDENTPANEL', 'TESTS3']
        self.assertEqual(sorted(a), sorted(b.__dir__()),
                         msg=u" model failed to return correct objects expected:{0:s}  returned:{1:s}".format(
                             str(a), str(b)))

    def test_smokeGLM(self):
        # Basic model returns objects
        stat = self.sas.sasstat()
        tr = self.sas.sasdata("class", "sashelp")
        b = stat.glm(data=tr, model='weight=height')
        a = ['DIAGNOSTICSPANEL', 'FITPLOT', 'FITSTATISTICS', 'LOG', 'MODELANOVA', 'NOBS', 'OVERALLANOVA',
             'PARAMETERESTIMATES', 'RESIDUALPLOTS']
        self.assertEqual(sorted(a), sorted(b.__dir__()),
                         msg=u" model failed to return correct objects expected:{0:s}  returned:{1:s}".format(
                             str(a), str(b)))

    def test_smokeLogistic(self):
        # Basic model returns objects
        stat = self.sas.sasstat()
        tr = self.sas.sasdata("class", "sashelp")
        b = stat.logistic(data=tr, model='sex=height weight')
        a = ['ASSOCIATION', 'CONVERGENCESTATUS', 'DFBETASPLOT', 'DPCPLOT', 'EFFECTPLOT', 'FITSTATISTICS',
             'GLOBALTESTS', 'INFLUENCEPLOTS', 'LEVERAGEPLOTS', 'LOG', 'MODELINFO', 'NOBS', 'ODDSRATIOS',
             'ORPLOT', 'PARAMETERESTIMATES', 'PHATPLOTS', 'RESPONSEPROFILE', 'ROCCURVE']
        self.assertEqual(sorted(a), sorted(b.__dir__()),
                         msg=u" model failed to return correct objects expected:{0:s}  returned:{1:s}".format(
                             str(a), str(b)))

    def test_smokeTpspline(self):
        # Basic model returns objects
        stat = self.sas.sasstat()
        self.sas.submit("""
                data work.melanoma;
                   input  year incidences @@;
                   datalines;
                1936    0.9   1937   0.8  1938   0.8  1939   1.3
                1940    1.4   1941   1.2  1942   1.7  1943   1.8
                1944    1.6   1945   1.5  1946   1.5  1947   2.0
                1948    2.5   1949   2.7  1950   2.9  1951   2.5
                1952    3.1   1953   2.4  1954   2.2  1955   2.9
                1956    2.5   1957   2.6  1958   3.2  1959   3.8
                1960    4.2   1961   3.9  1962   3.7  1963   3.3
                1964    3.7   1965   3.9  1966   4.1  1967   3.8
                1968    4.7   1969   4.4  1970   4.8  1971   4.8
                1972    4.8
                ;;
                run;
                """)

        tr = self.sas.sasdata("melanoma", "work")
        b = stat.tpspline(data=tr, model='incidences = (year) /alpha = 0.1', output='out = result pred uclm lclm')
        a = ['CRITERIONPLOT', 'DATASUMMARY', 'DIAGNOSTICSPANEL', 'FITPLOT', 'FITSTATISTICS', 'FITSUMMARY', 'LOG',
             'OBSERVEDBYPREDICTED', 'QQPLOT', 'RESIDPANEL', 'RESIDUALBYPREDICTED', 'RESIDUALHISTOGRAM', 'RFPLOT']
        self.assertEqual(sorted(a), sorted(b.__dir__()),
                         msg=u" model failed to return correct objects expected:{0:s}  returned:{1:s}".format(
                             str(a), str(b)))

    def test_tpspline2(self):
        # Basic model returns objects
        stat = self.sas.sasstat()
        self.sas.submit("""
        data work.melanoma;
           input  year incidences @@;
           datalines;
        1936    0.9   1937   0.8  1938   0.8  1939   1.3
        1940    1.4   1941   1.2  1942   1.7  1943   1.8
        1944    1.6   1945   1.5  1946   1.5  1947   2.0
        1948    2.5   1949   2.7  1950   2.9  1951   2.5
        1952    3.1   1953   2.4  1954   2.2  1955   2.9
        1956    2.5   1957   2.6  1958   3.2  1959   3.8
        1960    4.2   1961   3.9  1962   3.7  1963   3.3
        1964    3.7   1965   3.9  1966   4.1  1967   3.8
        1968    4.7   1969   4.4  1970   4.8  1971   4.8
        1972    4.8
        ;;
        run;
        """)

        tr = self.sas.sasdata("melanoma", "work")
        ds = self.sas.sasdata("result", "work")
        b = stat.tpspline(data=tr, model='incidences = (year) /alpha = 0.1', score=ds)
        a = ['CRITERIONPLOT', 'DATASUMMARY', 'DIAGNOSTICSPANEL', 'FITPLOT', 'FITSTATISTICS', 'FITSUMMARY', 'LOG',
             'OBSERVEDBYPREDICTED', 'QQPLOT', 'RESIDPANEL', 'RESIDUALBYPREDICTED', 'RESIDUALHISTOGRAM', 'RFPLOT',
             'SCOREPLOT']
        self.assertEqual(sorted(a), sorted(b.__dir__()),
                         msg=u" model failed to return correct objects expected:{0:s}  returned:{1:s}".format(
                             str(a), str(b)))

    def test_smokeHPLogistic(self):
        # Basic model returns objects
        stat = self.sas.sasstat()
        tr = self.sas.sasdata("class", "sashelp")
        b = stat.hplogistic(data=tr, model='sex=height weight')
        a = ['CONVERGENCESTATUS', 'DATAACCESSINFO', 'DIMENSIONS', 'FITSTATISTICS', 'GLOBALTESTS', 'ITERHISTORY',
             'LOG', 'MODELINFO', 'NOBS', 'PARAMETERESTIMATES', 'PERFORMANCEINFO', 'RESPONSEPROFILE']
        self.assertEqual(sorted(a), sorted(b.__dir__()),
                         msg=u" model failed to return correct objects expected:{0:s}  returned:{1:s}".format(
                             str(a), str(b)))

    def test_smokeHPReg(self):
        # Basic model returns objects
        stat = self.sas.sasstat()
        tr = self.sas.sasdata("class", "sashelp")
        # REG
        b = stat.hpreg(data=tr, model='weight=height')
        a = ['ANOVA', 'DATAACCESSINFO', 'DIMENSIONS', 'FITSTATISTICS', 'LOG', 'MODELINFO', 'NOBS',
             'PARAMETERESTIMATES', 'PERFORMANCEINFO']
        self.assertEqual(sorted(a), sorted(b.__dir__()),
                         msg=u"Simple Regession (reg) model failed to return correct objects expected:{0:s}  returned:{1:s}".format(
                             str(a), str(b)))

    def test_selectionDict(self):
        # Basic model returns objects
        stat = self.sas.sasstat()
        tr = self.sas.sasdata("class", "sashelp")
        selDict = {'method':'stepwise'}
        b = stat.hpreg(data=tr, model='weight=height', selection= selDict)
        a = ['ANOVA', 'DATAACCESSINFO', 'DIMENSIONS', 'FITSTATISTICS', 'LOG', 'MODELINFO', 'NOBS',
             'PARAMETERESTIMATES', 'PERFORMANCEINFO', 'SELECTEDEFFECTS', 'SELECTIONINFO', 'SELECTIONREASON', 
             'SELECTIONSUMMARY', 'STOPREASON']
        self.assertEqual(sorted(a), sorted(b.__dir__()),
                         msg=u"Simple Regession (HPREG) model failed to return correct objects expected:{0:s}  returned:{1:s}".format(
                             str(a), str(b)))

    def test_selectionDict2(self):
        # Basic model returns objects
        stat = self.sas.sasstat()
        tr = self.sas.sasdata("class", "sashelp")
        # DETAILS=NONE | SUMMARY | ALL
        selDict = {'method':'forward', 'details':'ALL', 'maxeffects':'0'}
        b = stat.hpreg(data=tr, model='weight=height', selection= selDict)
        a = ['ANOVA', 'DATAACCESSINFO', 'DIMENSIONS', 'ENTRYCANDIDATES', 'FITSTATISTICS', 'LOG', 
             'MODELINFO', 'NOBS', 'PARAMETERESTIMATES', 'PERFORMANCEINFO', 'SELECTEDEFFECTS', 
             'SELECTIONINFO', 'SELECTIONREASON', 'SELECTIONSUMMARY', 'STOPREASON']
        self.assertEqual(sorted(a), sorted(b.__dir__()),
                         msg=u"Simple Regession (HPREG) model failed to return correct objects expected:{0:s}  returned:{1:s}".format(
                             str(a), str(b)))

    def test_selectionDict3(self):
        # Basic model returns objects
        stat = self.sas.sasstat()
        tr = self.sas.sasdata("class", "sashelp")
        # DETAILS=NONE | SUMMARY | ALL
        selDict = {'stop': 'aic', 'method': 'backward', 'select': 'aic', 'choose': 'aic', 'maxeffects':'3'}
        b = stat.hpreg(data=tr, model='weight=height', selection= selDict)
        a = ['ANOVA', 'DATAACCESSINFO', 'DIMENSIONS', 'FITSTATISTICS', 'LOG', 'MODELINFO', 'NOBS',
             'PARAMETERESTIMATES', 'PERFORMANCEINFO', 'SELECTEDEFFECTS', 'SELECTIONINFO', 'SELECTIONREASON',
             'SELECTIONSUMMARY', 'STOPREASON']
        self.assertEqual(sorted(a), sorted(b.__dir__()),
                         msg=u"Simple Regession (HPREG) model failed to return correct objects expected:{0:s}  returned:{1:s}".format(
                             str(a), str(b)))

    def test_selectionDictError(self):
        # Basic model returns objects
        stat = self.sas.sasstat()
        tr = self.sas.sasdata("class", "sashelp")
        # DETAILS=NONE | SUMMARY | ALL
        selDict = {'method': 'stepwise', 'sl': '0.05'}
        b = stat.hpreg(data=tr, model='weight=height', selection=selDict)
        a = ['ERROR_LOG']
        self.assertEqual(sorted(a), sorted(b.__dir__()),
                         msg=u"Simple Regession (HPREG) model failed to return correct objects expected:{0:s}  returned:{1:s}".format(
                             str(a), str(b)))

    def test_missingVar(self):
        stat = self.sas.sasstat()
        tr = self.sas.sasdata("class", "sashelp")
        b = stat.mixed(data=tr, weight='novar', model='weight=height')
        a = ['ERROR_LOG']
        self.assertEqual(a, b.__dir__(),
                         msg=u"Simple Regession (mixed) model failed to return correct objects expected:{0:s}  returned:{1:s}".format(
                             str(a), str(b)))

    def test_extraStmt(self):
        # Extra Statements are ignored
        stat = self.sas.sasstat()
        d = self.sas.sasdata('cars', 'sashelp')
        b = stat.hpsplit(data=d, target='MSRP / level=interval', architecture='MLP', hidden=100, input='enginesize--length', train='', procopts='maxdepth=3')
        a = stat.hpsplit(data=d, target='MSRP / level=interval', input='enginesize--length', procopts='maxdepth=3' )
        self.assertEqual(a.__dir__(), b.__dir__(), msg=u"Extra Statements not being ignored expected:{0:s}  returned:{1:s}".format(str(a), str(b)))

    def test_multiTarget(self):
        # multiple target variables
        stat = self.sas.sasstat()
        nnin = self.sas.sasdata('cars', 'sashelp')
        # Need to change this assert; the exception isn't raised - I think the code changed
        x =  stat.hpsplit(data=nnin, target='MSRP origin', input='enginesize--length')
        a = ['ERROR_LOG']
        self.assertEqual(a, x.__dir__(), msg=u"Multiple target variables didn't fail in stat.hpsplit")
  
    def test_outputDset(self):
        stat = self.sas.sasstat()
        tsave = self.sas.sasdata('tsave')
        tr = self.sas.sasdata("class", "sashelp")
        stat.mixed(data=tr, weight='novar', model='weight=height', out=tsave)
        self.assertIsInstance(tsave, saspy.SASdata, msg="out= dataset not created properly")

    def test_target_input_syntax1(self):
        stat = self.sas.sasstat()
        c = self.sas.sasdata("class", "sashelp")
        t1 = 'weight'
        t2 = {'interval': 'weight'}
        t3 = ['weight']
        i1 = {'interval': ['height'],
              'nominal' : ['sex']}
        i2 = {'interval': ['height']}
        i3 = ['height']
        m = stat.glm(data=c, cls='sex', model='weight = height sex');
        ti1 = stat.glm(data=c, target=t1, input=i1)
        self.assertEqual(m.__dir__(), ti1.__dir__())
        ti2 = stat.glm(data=c, target=t2, input=i1)
        self.assertEqual(m.__dir__(), ti2.__dir__())
        ti3 = stat.glm(data=c, target=t3, input=i1)
        self.assertEqual(m.__dir__(), ti3.__dir__())
        m2 = stat.glm(data=c, model='weight = height');
        ti4 = stat.glm(data=c, target=t2, input=i2)
        self.assertEqual(m2.__dir__(), ti4.__dir__())
        ti5 = stat.glm(data=c, target=t1, input=i3)
        self.assertEqual(m2.__dir__(), ti5.__dir__())





