import unittest
from contextlib import redirect_stdout
from io import StringIO
from re import match
import pandas as pd
import saspy
from saspy.sastabulate import Tabulate, Class, Var, Statistic, Grouping

class TestSASTabulate(unittest.TestCase):
    def setUp(self):
        # Use the first entry in the configuration list
        self.sas = saspy.SASsession() #cfgname=saspy.SAScfg.SAS_config_names[0])
        self.assertIsInstance(self.sas, saspy.SASsession, msg="sas = saspy.SASsession(...) failed")
        # load a sas-help dataset
        self.cars = self.sas.sasdata('cars', libref='sashelp', results='text')

    def tearDown(self):
        if self.sas:
            self.sas._endsas()

    def test_tabulate(self):
        # check for tabulate being available on data set
        self.assertIsInstance(self.cars.tabulate, Tabulate, msg="tabulate should be available on data sets")
   
    def test_classes(self):        
        # extract a class with options
        by_drivetrain = self.cars.tabulate.as_class('drivetrain', label="Drive", all="Total")
        self.assertIsInstance(by_drivetrain, Class, msg=".as_class() method failed")
        self.assertEqual(by_drivetrain.label, "Drive", msg=".as_class() 'label' keyword not applied")
        self.assertEqual(by_drivetrain.all, "Total", msg=".as_class() 'all' keyword not applied")

        # test apply option functionally using .with_() 
        with_adjusted_label = by_drivetrain.with_(label="Train")
        self.assertEqual(with_adjusted_label.label, "Train", msg=".with_() method did not apply keyword")
        # should not mutate original; intended for composition
        self.assertEqual(by_drivetrain.label, "Drive", msg=".with_() should clone, not mutate")

        # test basic serialization
        self.assertEqual(str(by_drivetrain), "(drivetrain='Drive' ALL='Total')",
            msg="error with serialization of tabulation class with arguments")

        # test get multiple classes as tuple
        by_origin, by_type = self.cars.tabulate.classes('origin', 'type')
        self.assertIsInstance(by_origin, Class, msg=".classes() method failed")
        self.assertIsInstance(by_type, Class, msg=".classes() method failed")

    def test_vars(self):
        # extract a variable with options
        horsepower  = self.cars.tabulate.as_var('horsepower', label="Horse")
        self.assertIsInstance(horsepower, Var, msg=".as_var() method failed")
        self.assertEqual(horsepower.label, "Horse", msg=".as_var() 'label' keyword not applied")

        # test apply option functionally using .with_() 
        with_adjusted_label = horsepower.with_(label="Power")
        self.assertEqual(with_adjusted_label.label, "Power", msg=".with_() method did not apply keyword")
        # should not mutate original; intended for composition
        self.assertEqual(horsepower.label, "Horse", msg=".with_() should clone, not mutate")

        # test basic serialization
        self.assertEqual(str(horsepower), "horsepower='Horse'",
            msg="error with serialization of tabulation var with arguments")

        # test get multiple vars as tuple
        enginesize, cylinders  = self.cars.tabulate.vars('enginesize', 'cylinders')
        self.assertIsInstance(enginesize, Var, msg=".vars() method failed")
        self.assertIsInstance(cylinders, Var, msg=".vars() method failed")

    def test_stats(self):
        # create a statistic with options
        stdev = self.cars.tabulate.stat('std', label="StDev", format='5.2')
        self.assertIsInstance(stdev, Statistic, msg=".stat() method failed")
        self.assertEqual(stdev.label, "StDev", msg=".stat() 'label' keyword not applied")
        self.assertEqual(stdev.format, "5.2", msg=".stat() 'format' keyword not applied")

        # test apply option functionally using .with_() 
        with_adjusted_format = stdev.with_(format="6.2")
        self.assertEqual(with_adjusted_format.format, "6.2", msg=".with_() method did not apply keyword")
        # should not mutate original; intended for composition
        self.assertEqual(stdev.format, "5.2", msg=".with_() should clone, not mutate")

        # test basic serialization
        self.assertEqual(str(stdev), "std='StDev'*f=5.2",
            msg="error with serialization of tabulation statistic with arguments")

        # test get multiple stats as tuple
        mean, n = self.cars.tabulate.stats('mean', 'n')
        self.assertIsInstance(mean, Statistic, msg=".stats() method failed")
        self.assertIsInstance(n, Statistic, msg=".stats() method failed")

    def test_hierarchy(self):
        by_origin, by_type = self.cars.tabulate.classes('origin', 'type')
        enginesize, cylinders  = self.cars.tabulate.vars('enginesize', 'cylinders')
        mean, n = self.cars.tabulate.stats('mean', 'n')

        # test valid same-level concatenations
        concat_classes = by_origin | by_type
        self.assertIsInstance(concat_classes, Grouping, msg="concatenation of classes failed")
        concat_vars = enginesize | cylinders
        self.assertIsInstance(concat_vars, Grouping, msg="concatenation of vars failed")
        concat_stats = mean | n
        self.assertIsInstance(concat_stats, Grouping, msg="concatenation of stats failed")

        # test valid nestings; applies right side as child of left side
        nest_classes = by_origin * by_type
        self.assertIsInstance(nest_classes.child, Class, msg="nesting of classes failed")
        nest_class_var = by_origin * enginesize
        self.assertIsInstance(nest_class_var.child, Var, msg="nesting of var under class failed")
        nest_var_stat =  enginesize * mean
        self.assertIsInstance(nest_var_stat.child, Statistic, msg="nesting of statistic under var failed")

        # nesting of concatenations should work
        nest_concats = (by_origin | by_type) * (mean | n)
        self.assertIsInstance(nest_concats, Grouping, msg="nesting of concatenated elements failed")
        self.assertIsInstance(nest_concats.child, Grouping, msg="nesting of concatenated elements failed")
        
        # test invalid nestings for appropriate rejection 
        self.assertRaises(SyntaxError, lambda: enginesize * by_origin) # class under var
        self.assertRaises(SyntaxError, lambda: mean * enginesize) # var under stat
        self.assertRaises(SyntaxError, lambda: n * mean) # stat under stat
        self.assertRaises(SyntaxError, lambda: mean * by_origin) # class under stat

    def test_composition_serialization(self):
        by_origin, by_type, by_drivetrain = self.cars.tabulate.classes('origin', 'type', 'drivetrain')
        enginesize, cylinders  = self.cars.tabulate.vars('enginesize', 'cylinders')
        mean, n = self.cars.tabulate.stats('mean', 'n')

        # compoase a larger fragment using all options, check its serialization
        my_tabulation = (
            (by_origin | by_type) * by_drivetrain.with_(all="Total") * enginesize
            * (mean.with_(label="Average") | n)
        )
        self.assertEqual(
            str(my_tabulation), 
            "((origin type) * (drivetrain ALL='Total') * enginesize * (mean='Average' n))",
            msg="serialized table composition did not match expectation"
        )

    def test_procedure(self):
        by_origin, by_type, by_drivetrain = self.cars.tabulate.classes('origin', 'type', 'drivetrain')
        enginesize, cylinders  = self.cars.tabulate.vars('enginesize', 'cylinders')
        mean, n = self.cars.tabulate.stats('mean', 'n')

        # check the full generated syntax of a command
        def get_generated_code(method: str) -> dict:
            captured = StringIO()
            with redirect_stdout(captured):
                self.sas.teach_me_SAS(True)
                method()
                self.sas.teach_me_SAS(False)
            lines = captured.getvalue().split('\n')
            # break submitted code into statements for assertions
            match_keyword = '^\s*(\w+?)\s'
            return dict(
                (match(match_keyword, l).group(1), l) for l in lines if match(match_keyword, l)
            )

        invocation = lambda: \
            self.cars.tabulate.table(
                where="cylinders > 0",
                left= by_drivetrain.with_(all="Total") * by_type,
                top= by_origin * (enginesize | cylinders) * (mean | n),
            )
        
        statements = get_generated_code(invocation)

        self.assertIn("proc tabulate data=sashelp.cars", statements['proc'])

        # gathered all classes used?
        expected_classes = {"drivetrain", "origin", "type"}
        classes_sent = statements['class'].replace(';','').split(' ')
        self.assertTrue(expected_classes.issubset(set(classes_sent)), msg="classes were not gathered")

        # gathered all vars used?
        expected_vars = {"cylinders", "enginesize"}
        vars_sent = statements['var'].replace(';','').split(' ')
        self.assertTrue(expected_vars.issubset(set(vars_sent)), msg="vars were not gathered")

        # passed the additional valid "where" option?
        self.assertIn('where cylinders > 0', statements['where'], msg="additional options (where) failed")
        
        # check table statement
        self.assertIn(
            "table (drivetrain ALL='Total') * type, origin * ((enginesize cylinders) * (mean n))",
            statements['table'], 
            msg="generated table syntax did not match expectation"
        )

    def test_to_dataframe(self):
        by_origin, by_type, by_drivetrain = self.cars.tabulate.classes('origin', 'type', 'drivetrain')
        enginesize, cylinders  = self.cars.tabulate.vars('enginesize', 'cylinders')
        mean, n = self.cars.tabulate.stats('mean', 'n')

        # generate a MultiIndex DataFrame instead of printing results
        frame = self.cars.tabulate.to_dataframe(
            left= by_drivetrain.with_(all="Total") * by_type * 
                  by_origin * (enginesize | cylinders) * (mean | n),
        )

        # verify that the frame was generated correctly
        self.assertIsInstance(frame, pd.DataFrame, msg=".to_dataframe() method failed")
        self.assertEqual(set(frame.index.names), {'Type', 'Origin', 'DriveTrain'})
        self.assertEqual(set(frame.columns), {'Cylinders_N', 'Cylinders_Mean', 'EngineSize_Mean', 'EngineSize_N'})
