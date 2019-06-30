import sys
import os
# sys.path.append('/home/dabao/Osiris')
sys.path.append('C://Users//User//Desktop//Osiris')
ROOT_FOR_TESTS = 'C://Users//User//Desktop//Osiris//tests//'

from Osiris.utils import * 
from Osiris.analysizer import Analysizer
import Osiris
import unittest
import warnings
import csv

image_IPythonDisplay_notebook_path = 'test_case_2.ipynb'
image_Matplotlib_notebook_path = 'test_case_3.ipynb'
relative_notebook_path = 'folder/test_case_4.ipynb'
analyze_strategy_notebook_path = 'test_case_5.ipynb'

class TestOsiris(unittest.TestCase):

    def setUp(self):
        warnings.simplefilter('ignore', category=ImportWarning)
        warnings.simplefilter('ignore', category=DeprecationWarning)
        warnings.simplefilter('ignore', category=ResourceWarning)

    # Conda environment required
    def test_relative_path(self):
        os.chdir(ROOT_FOR_TESTS)
        interface = Osiris.UserInterface(relative_notebook_path)
        is_executable = interface.analyse_executability(
            verbose=False, store=False, analyze_strategy='OEC')
        self.assertEqual(is_executable, True)

    def test_top_down_analyse_executability(self):
        os.chdir(ROOT_FOR_TESTS)
        interface = Osiris.UserInterface(analyze_strategy_notebook_path)
        is_executable = interface.analyse_executability(
            verbose=False, store=False, analyze_strategy='normal')
        self.assertEqual(is_executable, True)

    def test_OEC_analyse_executability(self):
        os.chdir(ROOT_FOR_TESTS)
        interface = Osiris.UserInterface(analyze_strategy_notebook_path)
        is_executable = interface.analyse_executability(
            verbose=False, store=False, analyze_strategy='OEC')
        self.assertEqual(is_executable, True)

    # PENDING
    @unittest.skip
    def test_dependency_analyse_executability(self):
        os.chdir(ROOT_FOR_TESTS)
        interface = Osiris.UserInterface(analyze_strategy_notebook_path)
        is_executable = interface.analyse_executability(
            verbose=False, store=False, analyze_strategy='dependency')
        self.assertEqual(is_executable, True)

    def test_top_down_analyse_strongly_matched_ouptut(self):
        os.chdir(ROOT_FOR_TESTS)
        interface = Osiris.UserInterface(analyze_strategy_notebook_path)
        num_of_reproductive_cells, num_of_cells, reproductivity_ratio, reproductive_cell_idx, source_code_from_non_reproductive_cells = interface.analyse_outputs(
            verbose=False, store=False, analyze_strategy='normal', strong_match=True)
        self.assertEqual(num_of_reproductive_cells, 1)
        self.assertEqual(num_of_cells, 3)

    def test_top_down_analyse_weakly_matched_ouptut(self):
        os.chdir(ROOT_FOR_TESTS)
        interface = Osiris.UserInterface(analyze_strategy_notebook_path)
        num_of_reproductive_cells, num_of_cells, reproductivity_ratio, reproductive_cell_idx, source_code_from_non_reproductive_cells = interface.analyse_outputs(
            verbose=False, store=False, analyze_strategy='normal', strong_match=False)
        self.assertEqual(num_of_reproductive_cells, 3)
        self.assertEqual(num_of_cells, 3)

    def test_OEC_analyse_strongly_matched_ouptut(self):
        os.chdir(ROOT_FOR_TESTS)
        interface = Osiris.UserInterface(analyze_strategy_notebook_path)
        num_of_reproductive_cells, num_of_cells, reproductivity_ratio, reproductive_cell_idx, source_code_from_non_reproductive_cells = interface.analyse_outputs(
            verbose=False, store=False, analyze_strategy='OEC', strong_match=True)
        self.assertEqual(num_of_reproductive_cells, 1)
        self.assertEqual(num_of_cells, 3)

    def test_OEC_analyse_weakly_matched_ouptut(self):
        os.chdir(ROOT_FOR_TESTS)
        interface = Osiris.UserInterface(analyze_strategy_notebook_path)
        num_of_reproductive_cells, num_of_cells, reproductivity_ratio, reproductive_cell_idx, source_code_from_non_reproductive_cells = interface.analyse_outputs(
            verbose=False, store=False, analyze_strategy='OEC', strong_match=False)
        self.assertEqual(num_of_reproductive_cells, 3)
        self.assertEqual(num_of_cells, 3)

    # PENDING
    @unittest.skip
    def test_dependency_analyse_strongly_matched_ouptut(self):
        pass

    # PENDING
    @unittest.skip
    def test_dependency_analyse_weakly_matched_ouptut(self):
        pass

    def test_OEC_analyse_weakly_matched_output_for_image_IPythonDisplay(self):
        os.chdir(ROOT_FOR_TESTS)
        interface = Osiris.UserInterface(image_IPythonDisplay_notebook_path)
        num_of_reproductive_cells, num_of_cells, reproductivity_ratio, reproductive_cell_idx, source_code_from_non_reproductive_cells = interface.analyse_outputs(
            verbose=False, store=False, analyze_strategy='OEC', strong_match=False)
        self.assertEqual(num_of_reproductive_cells, 1)
        self.assertEqual(num_of_cells, 1)

    def test_OEC_analyse_weakly_matched_output_for_image_Matplotlib(self):
        os.chdir(ROOT_FOR_TESTS)
        interface = Osiris.UserInterface(image_Matplotlib_notebook_path)
        num_of_reproductive_cells, num_of_cells, reproductivity_ratio, reproductive_cell_idx, source_code_from_non_reproductive_cells = interface.analyse_outputs(
            verbose=False, store=False, analyze_strategy='OEC', strong_match=False)
        self.assertEqual(num_of_reproductive_cells, 2)
        self.assertEqual(num_of_cells, 2)


if __name__ == '__main__':
    unittest.main()
