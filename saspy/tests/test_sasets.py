import unittest

import saspy
from saspy.tests.util import Utilities


class TestSASets(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.sas = saspy.SASsession()
        util = Utilities()
        procNeeded = ['arima', 'timeseries', 'ucm', 'esm', 'timeid', 'timedata']
        if not util.procFound(procNeeded):
            cls.skipTest("Not all of these procedures were found: %s" % str(procNeeded))

    @classmethod
    def tearDownClass(cls):
        if cls.sas:
            cls.sas._endsas()

    def test_smokeTimeseries(self):
        # Basic model returns objects
        ets = self.sas.sasets()
        self.sas.submit("""
        data work.seriesG;
            set sashelp.air;
            logair = log( air );
        run;
        """)
        air = self.sas.sasdata('seriesG', 'work')
        b = ets.timeseries(data=air, id='date interval=month', var='logair')
        a = ['ACFNORMPLOT', 'ACFPLOT', 'CYCLECOMPONENTPLOT', 'CYCLEPLOT', 'DATASET', 'IACFNORMPLOT', 'IACFPLOT',
             'IRREGULARCOMPONENTPLOT', 'LOG', 'PACFNORMPLOT', 'PACFPLOT', 'PERCENTCHANGEADJUSTEDPLOT', 'PERIODOGRAM',
             'SEASONALCOMPONENTPLOT', 'SEASONALIRREGULARCOMPONENTPLOT', 'SEASONALLYADJUSTEDPLOT', 'SERIESHISTOGRAM',
             'SERIESPLOT', 'SPECTRALDENSITYPLOT', 'SSARESULTSPLOT', 'SSARESULTSVECTORPLOT', 'SSASINGULARVALUESPLOT',
             'TRENDCOMPONENTPLOT', 'TRENDCYCLECOMPONENTPLOT', 'TRENDCYCLESEASONALPLOT', 'VARIABLE',
             'WHITENOISELOGPROBABILITYPLOT', 'WHITENOISEPROBABILITYPLOT']
        self.assertEqual(sorted(a), sorted(b.__dir__()),
                         msg=u"model failed to return correct objects expected:{0:s}  returned:{1:s}".format(
                             str(a), str(b)))

    def test_smokeArima(self):
        # Basic model returns objects
        ets = self.sas.sasets()
        air = self.sas.sasdata('air', 'sashelp')
        b = ets.arima(data=air, identify='var=air(1,12)')
        a = ['CHISQAUTO', 'DESCSTATS', 'LOG', 'SERIESCORRPANEL']
        self.assertEqual(sorted(a), sorted(b.__dir__()),
                         msg=u"model failed to return correct objects expected:{0:s}  returned:{1:s}".format(
                             str(a), str(b)))

    def test_smokeUCM(self):
        # Basic model returns objects
        ets = self.sas.sasets()
        self.sas.submit("""
                data work.seriesG;
                    set sashelp.air;
                    logair = log( air );
                run;
                """)
        air = self.sas.sasdata('seriesG', 'work')
        b = ets.ucm(data=air, id='date interval=month', model='logair',
                    irregular='',
                    level='',
                    slope='',
                    season='length=12 type=trig print=smooth',
                    estimate='',
                    forecast='lead=24 print=decomp')
        a = ['ANNUALSEASONPLOT', 'COMPONENTSIGNIFICANCE', 'CONVERGENCESTATUS', 'CUSUMPLOT', 'CUSUMSQPLOT',
             'DATASET', 'ERRORPLOT', 'ERRORWHITENOISELOGPROBPLOT', 'ESTIMATIONSPAN',
             'FILTEREDALLEXCEPTIRREGPLOT', 'FILTEREDALLEXCEPTIRREGVARPLOT', 'FILTEREDSEASONPLOT', 'FITSTATISTICS',
             'FITSUMMARY', 'FORECASTS', 'FORECASTSONLYPLOT', 'FORECASTSPAN', 'FORECASTSPLOT', 'INITIALPARAMETERS',
             'LOG', 'MODELPLOT', 'OUTLIERSUMMARY', 'PANELRESIDUALPLOT', 'PARAMETERESTIMATES', 'RESIDUALLOESSPLOT',
             'SEASONDESCRIPTION', 'SMOOTHEDALLEXCEPTIRREG', 'SMOOTHEDALLEXCEPTIRREGPLOT',
             'SMOOTHEDALLEXCEPTIRREGVARPLOT',
             'SMOOTHEDSEASON', 'SMOOTHEDSEASONPLOT']
        self.assertTrue(set(a) < set(b.__dir__()),
                        msg=u" model failed to return correct objects expected:{0:s}  returned:{1:s}".format(str(a),
                                                                                                             str(b)))

    def test_smokeUCM2(self):
        # Basic model returns objects
        ets = self.sas.sasets()
        self.sas.submit("""
                data work.seriesG;
                    set sashelp.air;
                    logair = log( air );
                run;
                """)
        air = self.sas.sasdata('seriesG', 'work')
        b = ets.ucm(data=air, id='date interval=month', model='logair',
                    irregular='',
                    level=True,
                    slope=True,
                    season='length=12 type=trig print=smooth',
                    estimate='',
                    forecast='lead=24 print=decomp')
        a = ['ANNUALSEASONPLOT', 'COMPONENTSIGNIFICANCE', 'CONVERGENCESTATUS', 'CUSUMPLOT', 'CUSUMSQPLOT',
             'DATASET', 'ERRORPLOT', 'ERRORWHITENOISELOGPROBPLOT', 'ESTIMATIONSPAN',
             'FILTEREDALLEXCEPTIRREGPLOT', 'FILTEREDALLEXCEPTIRREGVARPLOT', 'FILTEREDSEASONPLOT', 'FITSTATISTICS',
             'FITSUMMARY', 'FORECASTS', 'FORECASTSONLYPLOT', 'FORECASTSPAN', 'FORECASTSPLOT', 'INITIALPARAMETERS',
             'LOG', 'MODELPLOT', 'OUTLIERSUMMARY', 'PANELRESIDUALPLOT', 'PARAMETERESTIMATES', 'RESIDUALLOESSPLOT',
             'SEASONDESCRIPTION', 'SMOOTHEDALLEXCEPTIRREG', 'SMOOTHEDALLEXCEPTIRREGPLOT',
             'SMOOTHEDALLEXCEPTIRREGVARPLOT',
             'SMOOTHEDSEASON', 'SMOOTHEDSEASONPLOT']
        self.assertTrue(set(a) < set(b.__dir__()),
                        msg=u" model failed to return correct objects expected:{0:s}  returned:{1:s}".format(str(a),
                                                                                                             str(b)))

    def test_UCM2(self):
        # Basic model returns objects
        ets = self.sas.sasets()
        self.sas.submit("""
                data work.seriesG;
                    set sashelp.air;
                    logair = log( air );
                run;
                """)
        air = self.sas.sasdata('seriesG', 'work')
        b = ets.ucm(data=air, id='date interval=month', model='logair',
                    irregular=True,
                    level=True,
                    slope=True,
                    season='length=12 type=trig print=smooth',
                    estimate=True,
                    forecast='lead=24 print=decomp')
        a = ['ANNUALSEASONPLOT', 'COMPONENTSIGNIFICANCE', 'CONVERGENCESTATUS', 'CUSUMPLOT', 'CUSUMSQPLOT',
             'DATASET', 'ERRORPLOT', 'ERRORWHITENOISELOGPROBPLOT', 'ESTIMATIONSPAN',
             'FILTEREDALLEXCEPTIRREGPLOT', 'FILTEREDALLEXCEPTIRREGVARPLOT', 'FILTEREDSEASONPLOT', 'FITSTATISTICS',
             'FITSUMMARY', 'FORECASTS', 'FORECASTSONLYPLOT', 'FORECASTSPAN', 'FORECASTSPLOT', 'INITIALPARAMETERS',
             'LOG', 'MODELPLOT', 'OUTLIERSUMMARY', 'PANELRESIDUALPLOT', 'PARAMETERESTIMATES', 'RESIDUALLOESSPLOT',
             'SEASONDESCRIPTION', 'SMOOTHEDALLEXCEPTIRREG', 'SMOOTHEDALLEXCEPTIRREGPLOT',
             'SMOOTHEDALLEXCEPTIRREGVARPLOT',
             'SMOOTHEDSEASON', 'SMOOTHEDSEASONPLOT']
        self.assertTrue(set(a) < set(b.__dir__()),
                        msg=u"model failed to return correct objects expected:{0:s}  returned:{1:s}".format(
                            str(a), str(b)))

    def test_smokeESM(self):
        # Basic model returns objects
        ets = self.sas.sasets()
        self.sas.submit("""
                data work.seriesG;
                    set sashelp.air;
                    logair = log( air );
                run;
                """)
        air = self.sas.sasdata('seriesG', 'work')
        b = ets.esm(data=air, id='date interval=daily', forecast='_numeric_')
        a = ['DATASET', 'ERRORACFNORMPLOT', 'ERRORACFPLOT', 'ERRORHISTOGRAM', 'ERRORIACFNORMPLOT', 'ERRORIACFPLOT',
             'ERRORPACFNORMPLOT', 'ERRORPACFPLOT', 'ERRORPERIODOGRAM', 'ERRORPLOT', 'ERRORSPECTRALDENSITYPLOT',
             'ERRORWHITENOISELOGPROBPLOT', 'ERRORWHITENOISEPROBPLOT', 'FORECASTSONLYPLOT', 'FORECASTSPLOT',
             'LEVELSTATEPLOT',
             'LOG', 'MODELFORECASTSPLOT', 'MODELPLOT', 'VARIABLE']
        self.assertEqual(sorted(a), sorted(b.__dir__()),
                         msg=u"model failed to return correct objects expected:{0:s}  returned:{1:s}".format(
                             str(a), str(b)))

    def test_smokeTimeID(self):
        # Basic model returns objects
        ets = self.sas.sasets()
        self.sas.submit("""
                data work.workdays;
                   format day weekdate.;
                   input day : date. @@;
                   datalines;
                01AUG09 06AUG09 11AUG09 14AUG09 19AUG09 22AUG09
                27AUG09 01SEP09 04SEP09 09SEP09 12SEP09 17SEP09
                ;
                run;
                """)
        air = self.sas.sasdata('workdays', 'work')
        b = ets.timeid(data=air, id='day')
        a = ['DECOMPOSITIONPLOT', 'INTERVALCOUNTSCOMPONENTPLOT', 'LOG', 'OFFSETCOMPONENTPLOT',
             'SPANCOMPONENTPLOT', 'VALUESPLOT']
        self.assertEqual(sorted(a), sorted(b.__dir__()),
                         msg=u"model failed to return correct objects expected:{0:s}  returned:{1:s}".format(
                             str(a), str(b)))

    def test_smokeTimedata(self):
        # Basic model returns objects
        ets = self.sas.sasets()
        self.sas.submit("""
                proc fcmp outlib=work.timefnc.funcs;
                   subroutine mylog(actual[*], transform[*]);
                   outargs transform;
                   actlen  = DIM(actual);
                   do t = 1 to actlen;
                      transform[t] = log(actual[t]);
                   end;
                   endsub;

                   function mymean(actual[*]);
                   actlen  = DIM(actual);
                   sum = 0;
                   do t = 1 to actlen;
                      sum = sum + actual[t];
                   end;
                   return( sum / actlen );
                   endsub;
                run;
                quit;
                options cmplib = work.timefnc;
                """)
        air = self.sas.sasdata('air', 'sashelp')
        b = ets.timedata(data=air,
                         procopts='out=work.air print=(scalars arrays)',
                         id='date interval=qtr acc=t format=yymmdd.',
                         var='air',
                         outarrays=' logair myair',
                         outscalars='mystats',
                         prog_stmts="""
                                   call mylog(air,logair);
                                   do t = 1 to dim(air);
                                   myair[t] = air[t] - logair[t];
                                   end;
                                   mystats= mymean(air);
                                 """)
        a = ['ARRAYPLOT', 'ARRAYS', 'LOG', 'SCALARS']
        self.assertEqual(sorted(a), sorted(b.__dir__()),
                         msg=u"model failed to return correct objects expected:{0:s}  returned:{1:s}".format(
                             str(a), str(b)))

    def test_missingVar(self):
        ets = self.sas.sasets()
        d = self.sas.sasdata('air', 'sashelp')
        b = ets.arima(data=d, by='novar', identify='var=air(1,12)')
        a = ['ERROR_LOG']
        self.assertEqual(a, b.__dir__(),
                         msg=u"arima model failed to return correct objects expected:{0:s}  returned:{1:s}".format(
                             str(a), str(b)))

    def test_extraStmt(self):
        # Extra Statements are ignored
        ets = self.sas.sasets()
        d = self.sas.sasdata('air', 'sashelp')
        b = ets.arima(data=d, by='novar', identify='var=air(1,12)', crosscorr='date', decomp='air')
        a = ets.arima(data=d, by='novar', identify='var=air(1,12)')
        self.assertEqual(a.__dir__(), b.__dir__(),
                         msg=u"Extra Statements not being ignored expected:{0:s}  returned:{1:s}".format(
                             str(a), str(b)))

    def test_outputDset(self):
        ets = self.sas.sasets()
        air = self.sas.sasdata('air', 'sashelp')
        outAir = self.sas.sasdata('air')
        ets.arima(data=air, identify='var=air(1,12)', out=outAir)
        self.assertIsInstance(outAir, saspy.sasdata.SASdata, msg="out= dataset not created properly")

    def test_overridePlot(self):
        # Test that user can override plot options
        ets = self.sas.sasets()
        air = self.sas.sasdata('air', 'sashelp')
        outAir = self.sas.sasdata('air')
        b = ets.arima(data=air, identify='var=air(1,12)', out=outAir, procopts='plots=none')
        a = ['CHISQAUTO', 'DESCSTATS', 'LOG']
        self.assertEqual(sorted(a), sorted(b.__dir__()),
                         msg=u"plots overridden and disabled expected:{0:s}  returned:{1:s}".format(
                             str(a), str(b)))
