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

def _patch_import_nolocal(name, globals=None, locals=None, fromlist=(), level=0):
    """
    Patch the __import__ function to always raise an exception for any
    local `sascfg_personal` imports
    """
    if name in ('sascfg_personal'):
        raise ImportError
    else:
        return _real_import(name, globals=globals, locals=locals, fromlist=fromlist, level=level)

def _patch_import_module_nolocal(name, package=None):
    """
    Patch the importlib.import_module function to always raise an exception
    for any local `sascfg_personal` imports
    """
    if name in ('sascfg_personal'):
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

    @mock.patch('builtins.__import__', _patch_import_nolocal)
    @mock.patch('importlib.import_module', _patch_import_module_nolocal)
    def test_config_find_config_global_sascfg_personal(self):
        """
        Test that the global `sascfg_personal.py` file is read if no other configuration
        path is satisfied.
        """
        importlib.reload(saspy)
        cfg_manager = saspy.SASconfig()
        cfg_module = cfg_manager._find_config()

        cfg_src = inspect.getfile(cfg_module)

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

        shutil.copy(inspect.getfile(saspy.sascfg), tmpcfg)

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
