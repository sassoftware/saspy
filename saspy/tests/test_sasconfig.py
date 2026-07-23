from unittest import mock
import unittest
import saspy
import builtins
import importlib
import inspect
import os
import shutil
import sys
import tempfile


_real_import =  builtins.__import__
_real_import_module = importlib.import_module

def _patch_import_none(name, globals=None, locals=None, fromlist=(), level=0):
    """
    Patch the __import__ function to always raise an exception for any
    `sascfg_personal` imports
    """
    if name in ('saspy.sascfg_personal', 'sascfg_personal'):
        raise ImportError
    else:
        return _real_import(name, globals=globals, locals=locals, fromlist=fromlist, level=level)

def _patch_import_module_none(name, package=None):
    """
    Patch the importlib.import_module function to always raise an exception
    for any `sascfg_personal` imports
    """
    if name in ('saspy.sascfg_personal', 'sascfg_personal'):
        raise ImportError
    else:
        return _real_import_module(name, package=package)

class TestSASConfig(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """
        Store the install path for the library
        """
        home = os.path.expanduser('~/.config/saspy')
        install = os.path.dirname(inspect.getfile(saspy))

        cls.cfg_global_standard_path = os.path.join(install, 'sascfg.py')
        cls.cfg_global_personal_path = os.path.join(install, 'sascfg_personal.py')
        cls.cfg_home_path = os.path.join(home, 'sascfg_personal.py')

    def _backup_paths(self, paths:dict[str,bool]):
        """
        Backup the paths in the dictionary, where each key is the original path and the value is a boolean indicating whether or not it should be 'restored'
        """
        for path, _ in paths.items():
            if os.path.isfile(path):
                # If the file exists, rename it to a backup file
                backup_path = path + '.bak'
                os.rename(path, backup_path)
                print(f"Backed up {path} to {backup_path}")
                paths[path] = True
            else:
                # If the file does not exist mark it as not needing to be restored
                paths[path] = False

    def _restore_paths(self, paths:dict[str,bool]):
        """
        Restore the paths in the dictionary, where each key is the original path and the value is a boolean indicating whether or not it should be 'restored'
        """
        for path, should_restore in paths.items():
            if should_restore:
                # If the file was backed up, restore it
                backup_path = path + '.bak'
                os.rename(backup_path, path)
                print(f"Restored {backup_path} to {path}")

    def _reset_config_modules(self):
        """Remove cached config modules to force fresh import on next access"""
        for mod in ['sascfg', 'sascfg_personal']:
            sys.modules.pop(mod, None)
        # Reload the saspy module to ensure that any cached config modules are cleared
        importlib.reload(saspy)


    @mock.patch('builtins.__import__', _patch_import_none)
    @mock.patch('importlib.import_module', _patch_import_module_none)
    def test_config_find_config_global_sascfg(self):
        """
        Test that the global `sascfg.py` file is read if no other configuration
        path is satisfied.
        """
        importlib.reload(saspy)
        cfg_manager = saspy.SASconfig()
        cfg_module = cfg_manager._find_config()

        cfg_src = inspect.getfile(cfg_module)

        self.assertEqual(cfg_src, self.cfg_global_standard_path)

    def test_config_find_config_global_sascfg_personal(self):
        """
        Test that the global `sascfg_personal.py` file is read if no other configuration
        path is satisfied.
        """
        importlib.reload(saspy)
        cfg_manager = saspy.SASconfig()
        cfg_module = cfg_manager._find_config()

        # Set up a dummy `sascfg_personal.py` file in the current working directory to test that it is not used
        temp_cfg = os.path.join(os.getcwd(), 'sascfg_personal.py')
        # Also check and see if the home directory has a `sascfg_personal.py` file, and if not create a temporary one for the test
        if not os.path.isfile(self.cfg_home_path):
            shutil.copy(self.cfg_global_standard_path, self.cfg_home_path)
            # Ensure the copied file is removed after the test
            self.addCleanup(lambda: os.remove(self.cfg_home_path))

        # Make the dummy file a copy of the global `sascfg_personal.py` file to ensure it is valid
        shutil.copy(self.cfg_global_standard_path, temp_cfg)
        # Ensure the copied file is removed after the test
        self.addCleanup(lambda: os.remove(temp_cfg))

        cfg_src = inspect.getfile(cfg_module)

        # Ensure that the global `sascfg_personal.py` file is used, not the local ones in the current working directory or home directory
        self.assertEqual(cfg_src, self.cfg_global_personal_path)

    def test_config_find_config_parameter_exists(self):
        """
        Test that the config file passed as a parameter to `_find_config`
        is used.
        """
        PATHS = (self.cfg_global_standard_path,
            self.cfg_global_personal_path,
            self.cfg_home_path)

        tmpdir = tempfile.TemporaryDirectory()
        tmpcfg = os.path.join(tmpdir.name, 'saspy_test_config.py')

        shutil.copy(self.cfg_global_standard_path, tmpcfg)

        cfg_manager = saspy.SASconfig()
        cfg_module = cfg_manager._find_config(tmpcfg)

        cfg_src = inspect.getfile(cfg_module)

        tmpdir.cleanup()

        self.assertNotIn(cfg_src, PATHS)

    def test_config_find_config_parameter_noexists(self):
        """
        Test that a n invalid config file path passed to `_find_config`
        raises a SASConfigFileNotFoundError.
        """
        with self.assertRaises(saspy.SASConfigNotFoundError):
            cfg_manager = saspy.SASconfig()
            cfg_module = cfg_manager._find_config('/not/a/valid/config.py')

    def test_config_find_config_parameter_notfile(self):
        """
        Test that a config file path passed to `_find_config` that is not a file
        raises a SASConfigFileNotFoundError.
        """
        with self.assertRaises(saspy.SASConfigNotFoundError):
            cfg_manager = saspy.SASconfig()
            cfg_module = cfg_manager._find_config(os.path.dirname(self.cfg_global_standard_path))

    def test_config_find_config_parameter_notpy(self):
        """
        Test that a config file path passed to `_find_config` that is not a .py file
        raises a SASConfigFileNotFoundError.
        """
        with self.assertRaises(saspy.SASConfigNotFoundError):
            cfg_manager = saspy.SASconfig()
            cfg_module = cfg_manager._find_config(os.path.join(os.path.dirname(self.cfg_global_standard_path), 'not_a_python_file.txt'))
    
    def test_config_find_config_parameter_notpy_but_exists(self):
        """
        Test that a config file path passed to `_find_config` that is not a .py file
        but does exist raises a SASConfigFileNotFoundError.
        """
        tmpdir = tempfile.TemporaryDirectory()
        tmpcfg = os.path.join(tmpdir.name, 'not_a_python_file.txt')

        with open(tmpcfg, 'w') as f:
            f.write('This is not a python file.')

        with self.assertRaises(saspy.SASConfigNotFoundError):
            cfg_manager = saspy.SASconfig()
            cfg_module = cfg_manager._find_config(tmpcfg)

        tmpdir.cleanup()

    def test_config_find_config_order_of_inclusion(self):
        """
        Test that the order of inclusion for config files is as follows:
        1. Config file passed as a parameter to `_find_config`
        2. Global `sascfg_personal.py` file in the saspy library path
        3. 'Local scope' sascfg_personal.py file
        4. Home directory `sascfg_personal.py` file
        5. Global `sascfg.py` file
        """
        local_scope_path = os.path.join(sys.path[0], 'sascfg_personal.py')
        PATHS:dict[str,bool] = {
            self.cfg_global_standard_path: False,
            self.cfg_global_personal_path: False,
            self.cfg_home_path: False,
            local_scope_path: False,
        }

        # To test the order of inclusion, we will have to work 'backwards' through the list of paths,
        # and ensure that the correct one is found at each step.

        # To simulate this, any existing config files will have to be temporarily moved/hidden.
        #   In the cases where a file already exists in one of the locations, 
        #   we will rename it to a backup file and then restore it at the end of the test.

        #   If a file did not exist at one of the locations, we will create a temporary file to 
        #   simulate the presence of a config file at that location and then remove it at the end of the test.

        # This will be tracked in a list of tuples, where each tuple contains the original path and whether or not it should be 'restored'

        dummy_config_content = '# This is a temporary config file to simulate the presence of a config file at a specific location.\n' \
                               'SAS_config_names = ["dummy"]\n' \
                               'SAS_config_options = {"lock_down": False, "verbose": True}\n' \
                               'dummy = {"saspath": "/dummy/path/to/sas", "options": ["-dummy", "-options"]}\n'

        self.addCleanup(lambda: self._reset_config_modules())
        self._backup_paths(PATHS)
        self.addCleanup(lambda: self._restore_paths(PATHS))

        # Test that nothing is found if no config files are present
        self._reset_config_modules()
        with self.assertRaises(ImportError):
            cfg_manager = saspy.SASconfig()
            cfg_module = cfg_manager._find_config()

        # Test Option 5: Global `sascfg.py` file
        # Create a temporary config file to simulate the presence of a config file at the global `sascfg.py` location
        with open(self.cfg_global_standard_path, 'w') as f:
            f.write(dummy_config_content)
        self.addCleanup(lambda: os.remove(self.cfg_global_standard_path))
        self._reset_config_modules()
        cfg_manager = saspy.SASconfig()
        cfg_module = cfg_manager._find_config()

        cfg_src = inspect.getfile(cfg_module)

        self.assertEqual(cfg_src, self.cfg_global_standard_path)

        # Test Option 4: Home directory `sascfg_personal.py` file
        # Create a temporary config file to simulate the presence of a config file at the home directory `sascfg_personal.py` location
        with open(self.cfg_home_path, 'w') as f:
            f.write(dummy_config_content)
        self.addCleanup(lambda: os.remove(self.cfg_home_path))
        self._reset_config_modules()
        cfg_manager = saspy.SASconfig()
        cfg_module = cfg_manager._find_config()

        cfg_src = inspect.getfile(cfg_module)

        self.assertEqual(cfg_src, self.cfg_home_path)

        # Test Option 3: 'Local scope' sascfg_personal.py file
        # Create a temporary config file to simulate the presence of a config file at the 'local scope' sascfg_personal.py location
        with open(local_scope_path, 'w') as f:
            f.write(dummy_config_content)
        self.addCleanup(lambda: os.remove(local_scope_path))
        self._reset_config_modules()
        cfg_manager = saspy.SASconfig()
        cfg_module = cfg_manager._find_config() 

        cfg_src = inspect.getfile(cfg_module)
        
        self.assertEqual(cfg_src, local_scope_path)

        # Test Option 2: Global `sascfg_personal.py` file
        # Create a temporary config file to simulate the presence of a config file at the global `sascfg_personal.py` location
        with open(self.cfg_global_personal_path, 'w') as f:
            f.write(dummy_config_content)
        self.addCleanup(lambda: os.remove(self.cfg_global_personal_path))
        
        self._reset_config_modules()
        cfg_manager = saspy.SASconfig()
        cfg_module = cfg_manager._find_config()

        cfg_src = inspect.getfile(cfg_module)

        self.assertEqual(cfg_src, self.cfg_global_personal_path)

        # Test Option 1: Config file passed as a parameter to `_find_config`
        # Create a temporary config file to simulate the presence of a config file at a custom location
        tmpdir = tempfile.TemporaryDirectory()
        tmpcfg = os.path.join(tmpdir.name, 'saspy_test_config.py')
        with open(tmpcfg, 'w') as f:
            f.write(dummy_config_content)
        self.addCleanup(lambda: tmpdir.cleanup())
        
        self._reset_config_modules()
        cfg_manager = saspy.SASconfig()
        cfg_module = cfg_manager._find_config(tmpcfg)

        cfg_src = inspect.getfile(cfg_module)

        # This is a special case where the cfg_src will be a copy of the temp file due to the 
        #  way the _find_config function works, so we will check cfg_manager.origin instead of the file.
        self.assertEqual(cfg_manager.origin, tmpcfg)

        # Now that the tests are complete, the cleanup functions will be called to 
        # remove any temporary config files that were created and restore any original 
        # config files that were moved/hidden.


    