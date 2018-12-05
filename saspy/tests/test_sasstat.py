import unittest
import saspy

from saspy.tests.util import Utilities

class TestSASstat(unittest.TestCase):
    @classmethod    
    def setUpClass(cls):
        cls.sas = saspy.SASsession()
        util = Utilities(cls.sas)
        procNeeded=['reg', 'mixed', 'hpsplit', 'hplogistic', 'hpreg', 'glm', 'logistic', 'tpspline',
                    'hplogistic', 'hpreg', 'phreg', 'ttest', 'factor']
        if not util.procFound(procNeeded):
            cls.skipTest("Not all of these procedures were found: %s" % str(procNeeded))

    @classmethod    
    def tearDownClass(cls):
        if cls.sas:
           cls.sas._endsas()

    def defineData(self):
        self.sas.submit("""
                        data Myeloma;
        input Time VStatus LogBUN HGB Platelet Age LogWBC Frac
             LogPBM Protein SCalc;
        label Time='Survival Time'
             VStatus='0=Alive 1=Dead';
       datalines;
     1.25  1  2.2175   9.4  1  67  3.6628  1  1.9542  12  10
     1.25  1  1.9395  12.0  1  38  3.9868  1  1.9542  20  18
     2.00  1  1.5185   9.8  1  81  3.8751  1  2.0000   2  15
     2.00  1  1.7482  11.3  0  75  3.8062  1  1.2553   0  12
     2.00  1  1.3010   5.1  0  57  3.7243  1  2.0000   3   9
     3.00  1  1.5441   6.7  1  46  4.4757  0  1.9345  12  10
     5.00  1  2.2355  10.1  1  50  4.9542  1  1.6628   4   9
     5.00  1  1.6812   6.5  1  74  3.7324  0  1.7324   5   9
     6.00  1  1.3617   9.0  1  77  3.5441  0  1.4624   1   8
     6.00  1  2.1139  10.2  0  70  3.5441  1  1.3617   1   8
     6.00  1  1.1139   9.7  1  60  3.5185  1  1.3979   0  10
     6.00  1  1.4150  10.4  1  67  3.9294  1  1.6902   0   8
     7.00  1  1.9777   9.5  1  48  3.3617  1  1.5682   5  10
     7.00  1  1.0414   5.1  0  61  3.7324  1  2.0000   1  10
     7.00  1  1.1761  11.4  1  53  3.7243  1  1.5185   1  13
     9.00  1  1.7243   8.2  1  55  3.7993  1  1.7404   0  12
    11.00  1  1.1139  14.0  1  61  3.8808  1  1.2788   0  10
    11.00  1  1.2304  12.0  1  43  3.7709  1  1.1761   1   9
    11.00  1  1.3010  13.2  1  65  3.7993  1  1.8195   1  10
    11.00  1  1.5682   7.5  1  70  3.8865  0  1.6721   0  12
    11.00  1  1.0792   9.6  1  51  3.5051  1  1.9031   0   9
    13.00  1  0.7782   5.5  0  60  3.5798  1  1.3979   2  10
    14.00  1  1.3979  14.6  1  66  3.7243  1  1.2553   2  10
    15.00  1  1.6021  10.6  1  70  3.6902  1  1.4314   0  11
    16.00  1  1.3424   9.0  1  48  3.9345  1  2.0000   0  10
    16.00  1  1.3222   8.8  1  62  3.6990  1  0.6990  17  10
    17.00  1  1.2304  10.0  1  53  3.8808  1  1.4472   4   9
    17.00  1  1.5911  11.2  1  68  3.4314  0  1.6128   1  10
    18.00  1  1.4472   7.5  1  65  3.5682  0  0.9031   7   8
    19.00  1  1.0792  14.4  1  51  3.9191  1  2.0000   6  15
    19.00  1  1.2553   7.5  0  60  3.7924  1  1.9294   5   9
    24.00  1  1.3010  14.6  1  56  4.0899  1  0.4771   0   9
    25.00  1  1.0000  12.4  1  67  3.8195  1  1.6435   0  10
    26.00  1  1.2304  11.2  1  49  3.6021  1  2.0000  27  11
    32.00  1  1.3222  10.6  1  46  3.6990  1  1.6335   1   9
    35.00  1  1.1139   7.0  0  48  3.6532  1  1.1761   4  10
    37.00  1  1.6021  11.0  1  63  3.9542  0  1.2041   7   9
    41.00  1  1.0000  10.2  1  69  3.4771  1  1.4771   6  10
    41.00  1  1.1461   5.0  1  70  3.5185  1  1.3424   0   9
    51.00  1  1.5682   7.7  0  74  3.4150  1  1.0414   4  13
    52.00  1  1.0000  10.1  1  60  3.8573  1  1.6532   4  10
    54.00  1  1.2553   9.0  1  49  3.7243  1  1.6990   2  10
    58.00  1  1.2041  12.1  1  42  3.6990  1  1.5798  22  10
    66.00  1  1.4472   6.6  1  59  3.7853  1  1.8195   0   9
    67.00  1  1.3222  12.8  1  52  3.6435  1  1.0414   1  10
    88.00  1  1.1761  10.6  1  47  3.5563  0  1.7559  21   9
    89.00  1  1.3222  14.0  1  63  3.6532  1  1.6232   1   9
    92.00  1  1.4314  11.0  1  58  4.0755  1  1.4150   4  11
     4.00  0  1.9542  10.2  1  59  4.0453  0  0.7782  12  10
     4.00  0  1.9243  10.0  1  49  3.9590  0  1.6232   0  13
     7.00  0  1.1139  12.4  1  48  3.7993  1  1.8573   0  10
     7.00  0  1.5315  10.2  1  81  3.5911  0  1.8808   0  11
     8.00  0  1.0792   9.9  1  57  3.8325  1  1.6532   0   8
    12.00  0  1.1461  11.6  1  46  3.6435  0  1.1461   0   7
    11.00  0  1.6128  14.0  1  60  3.7324  1  1.8451   3   9
    12.00  0  1.3979   8.8  1  66  3.8388  1  1.3617   0   9
    13.00  0  1.6628   4.9  0  71  3.6435  0  1.7924   0   9
    16.00  0  1.1461  13.0  1  55  3.8573  0  0.9031   0   9
    19.00  0  1.3222  13.0  1  59  3.7709  1  2.0000   1  10
    19.00  0  1.3222  10.8  1  69  3.8808  1  1.5185   0  10
    28.00  0  1.2304   7.3  1  82  3.7482  1  1.6721   0   9
    41.00  0  1.7559  12.8  1  72  3.7243  1  1.4472   1   9
    53.00  0  1.1139  12.0  1  66  3.6128  1  2.0000   1  11
    57.00  0  1.2553  12.5  1  66  3.9685  0  1.9542   0  11
    77.00  0  1.0792  14.0  1  60  3.6812  0  0.9542   0  12
    ;;
    run;
    data SocioEconomics;
   input Population School Employment Services HouseValue;
   datalines;
    5700     12.8      2500      270       25000
    1000     10.9      600       10        10000
    3400     8.8       1000      10        9000
    3800     13.6      1700      140       25000
    4000     12.8      1600      140       25000
    8200     8.3       2600      60        12000
    1200     11.4      400       10        16000
    9100     11.5      3300      60        14000
    9900     12.5      3400      180       18000
    9600     13.7      3600      390       25000
    9600     9.6       3300      80        12000
    9400     11.4      4000      100       13000
    ;;
    run;
    
    data time;
   input time @@;
   datalines;
    43  90  84  87  116   95  86   99   93  92
    121  71  66  98   79  102  60  112  105  98
    ;;
    run;
    
    data pressure;
   input SBPbefore SBPafter @@;
   datalines;
    120 128   124 131   130 131   118 127
    140 132   128 125   140 141   135 137
    126 118   130 132   126 129   127 135
    ;;
    run;
    """)


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
        self.assertIsInstance(b, saspy.sasresults.SASresults, msg="correct return type")

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
        self.assertFalse('ERROR_LOG' in b.__dir__(), msg=u"logistic had errors in the log")

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
        self.assertFalse('ERROR_LOG' in b.__dir__(), msg=u"hplogistic had errors in the log")

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
    """
    def test_extraStmt(self):
        # Extra Statements are ignored
        stat = self.sas.sasstat()
        d = self.sas.sasdata('cars', 'sashelp')
        b = stat.hpsplit(data=d, target='MSRP / level=interval', architecture='MLP', hidden=100, input='enginesize--length', train='', procopts='maxdepth=3')
        a = stat.hpsplit(data=d, target='MSRP / level=interval', input='enginesize--length', procopts='maxdepth=3' )
        self.assertEqual(a.__dir__(), b.__dir__(), msg=u"Extra Statements not being ignored expected:{0:s}  returned:{1:s}".format(str(a), str(b)))
    """

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
        self.assertIsInstance(tsave, saspy.sasdata.SASdata, msg="out= dataset not created properly")

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

    def phregResult1(self):
        stat = self.sas.sasstat()
        self.defineData()
        tr = self.sas.sasdata("melanoma", "work")
        b = stat.reg(data=tr, model="""Time*VStatus(0)=LogBUN HGB Platelet Age LogWBC
                         Frac LogPBM Protein SCalc / selection=stepwise slentry=0.25 slstay=0.15 details""")
        self.assertIsInstance(b, saspy.SASresults, msg="correct return type")

    def factorResult1(self):
        stat = self.sas.sasstat()
        self.defineData()
        tr = self.sas.sasdata("SocioEconomics", "work")
        b = stat.reg(data=tr, procopts='simple corr')
        self.assertIsInstance(b, saspy.SASresults, msg="correct return type")

    def factorResult2(self):
        stat = self.sas.sasstat()
        self.defineData()
        tr = self.sas.sasdata("SocioEconomics", "work")
        b = stat.reg(data=tr,
                     procopts='priors=smc msa residual rotate=promax reorder outstat=fact_all',
                     var = ['population', 'school']
                     )
        self.assertIsInstance(b, saspy.SASresults, msg="correct return type")

    def ttestResult1(self):
        stat = self.sas.sasstat()
        self.defineData()
        tr = self.sas.sasdata("time", "work")
        b = stat.reg(data=tr, var='time', procopts='h0=80 alpha=0.1')
        self.assertIsInstance(b, saspy.SASresults, msg="correct return type")

    def ttestResult2(self):
        stat = self.sas.sasstat()
        self.defineData()
        tr = self.sas.sasdata("pressure", "work")
        b = stat.reg(data=tr,  paired="SBPbefore*SBPafter")
        self.assertIsInstance(b, saspy.SASresults, msg="correct return type")

    def strdset1(self):
        stat = self.sas.sasstat()
        tr = self.sas.sasdata("class", "sashelp")
        s = stat.reg(data='sashelp.class', model='weight=height')
        ds = stat.reg(data=tr, model='weight=height')
        self.assertEqual(s, ds, msg="string sasdata mismatch")

    def strdset2(self):
        stat = self.sas.sasstat()
        tr = self.sas.sasdata("class", "sashelp")
        s = stat.reg(data='sashelp.class', model='weight=height')
        self.assertRaises(AssertionError,s, msg="bad dataset fails")



