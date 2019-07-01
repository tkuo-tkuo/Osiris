import sys
import os
sys.path.append('/home/dabao/Osiris')
# sys.path.append('C://Users//User//Desktop//Osiris')
ROOT_FOR_TESTS = '/home/dabao/Osiris/tests'
# ROOT_FOR_TESTS = 'C://Users//User//Desktop//Osiris//tests//'

from Osiris.utils import *
import csv
import warnings
import unittest
import Osiris
from Osiris.analysizer import Analysizer


naive_notebook_path = 'test_case_1.ipynb'
image_IPythonDisplay_notebook_path = 'test_case_2.ipynb'
image_Matplotlib_notebook_path = 'test_case_3.ipynb'
relative_notebook_path = 'folder/test_case_4.ipynb'
analyze_strategy_notebook_path = 'test_case_5.ipynb'
status_inspection_for_a_cell_notebook_path = 'test_case_6.ipynb'


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
        num_of_matched_cells, num_of_cells, match_ratio, matched_cell_idx, source_code_from_unmatched_cells = interface.analyse_outputs(
            verbose=False, store=False, analyze_strategy='normal', strong_match=True)
        self.assertEqual(num_of_matched_cells, 1)
        self.assertEqual(num_of_cells, 3)

    def test_top_down_analyse_weakly_matched_ouptut(self):
        os.chdir(ROOT_FOR_TESTS)
        interface = Osiris.UserInterface(analyze_strategy_notebook_path)
        num_of_matched_cells, num_of_cells, match_ratio, matched_cell_idx, source_code_from_unmatched_cells = interface.analyse_outputs(
            verbose=False, store=False, analyze_strategy='normal', strong_match=False)
        self.assertEqual(num_of_matched_cells, 3)
        self.assertEqual(num_of_cells, 3)

    def test_OEC_analyse_strongly_matched_ouptut(self):
        os.chdir(ROOT_FOR_TESTS)
        interface = Osiris.UserInterface(analyze_strategy_notebook_path)
        num_of_matched_cells, num_of_cells, match_ratio, matched_cell_idx, source_code_from_unmatched_cells = interface.analyse_outputs(
            verbose=False, store=False, analyze_strategy='OEC', strong_match=True)
        self.assertEqual(num_of_matched_cells, 1)
        self.assertEqual(num_of_cells, 3)

    def test_OEC_analyse_weakly_matched_ouptut(self):
        os.chdir(ROOT_FOR_TESTS)
        interface = Osiris.UserInterface(analyze_strategy_notebook_path)
        num_of_matched_cells, num_of_cells, match_ratio, matched_cell_idx, source_code_from_unmatched_cells = interface.analyse_outputs(
            verbose=False, store=False, analyze_strategy='OEC', strong_match=False)
        self.assertEqual(num_of_matched_cells, 3)
        self.assertEqual(num_of_cells, 3)

    # PENDING
    @unittest.skip
    def test_dependency_analyse_strongly_matched_ouptut(self):
        pass

    # PENDING
    @unittest.skip
    def test_dependency_analyse_weakly_matched_ouptut(self):
        pass

    def test_top_down_analyse_reproducibility(self):
        os.chdir(ROOT_FOR_TESTS)
        interface = Osiris.UserInterface(naive_notebook_path)
        num_of_reproducible_cells, num_of_cells, reproducible_ratio, reproducible_cell_idx = interface.analyse_reproducibility(
            verbose=False, store=False, analyze_strategy='normal')
        self.assertEqual(num_of_reproducible_cells, 2)
        self.assertEqual(num_of_cells, 4)
        self.assertEqual(reproducible_cell_idx, [0, 3])

    def test_OEC_analyse_reproducibility(self):
        os.chdir(ROOT_FOR_TESTS)
        interface = Osiris.UserInterface(naive_notebook_path)
        num_of_reproducible_cells, num_of_cells, reproducible_ratio, reproducible_cell_idx = interface.analyse_reproducibility(
            verbose=False, store=False, analyze_strategy='OEC')
        self.assertEqual(num_of_reproducible_cells, 2)
        self.assertEqual(num_of_cells, 4)
        self.assertEqual(reproducible_cell_idx, [0, 1])

    # PENDING
    @unittest.skip
    def test_dependency_analyse_reproducibility(self):
        pass

    # WORKING
    def test_top_down_analyse_reproducibility_for_a_cell_line_by_line(self):
        os.chdir(ROOT_FOR_TESTS)
        interface = Osiris.UserInterface(
            status_inspection_for_a_cell_notebook_path)
        problematic_statement_index = interface.analyse_reproducibility_for_a_cell_line_by_line(
            verbose=False, store=False, analyze_strategy='normal', cell_index=1)
        self.assertEqual(problematic_statement_index, 9)

    def test_OEC_analyse_reproducibility_for_a_cell_line_by_line(self):
        os.chdir(ROOT_FOR_TESTS)
        interface = Osiris.UserInterface(
            status_inspection_for_a_cell_notebook_path)
        problematic_statement_index = interface.analyse_reproducibility_for_a_cell_line_by_line(
            verbose=False, store=False, analyze_strategy='OEC', cell_index=2)
        self.assertEqual(problematic_statement_index, 9)

    # PENDING
    @unittest.skip
    def test_dependency_analyse_reproducibility_for_a_cell_line_by_line(self):
        pass

    def test_OEC_analyse_weakly_matched_output_for_image_IPythonDisplay(self):
        os.chdir(ROOT_FOR_TESTS)
        interface = Osiris.UserInterface(image_IPythonDisplay_notebook_path)
        num_of_matched_cells, num_of_cells, match_ratio, matched_cell_idx, source_code_from_unmatched_cells = interface.analyse_outputs(
            verbose=False, store=False, analyze_strategy='OEC', strong_match=False)
        self.assertEqual(num_of_matched_cells, 1)
        self.assertEqual(num_of_cells, 1)

    def test_OEC_analyse_weakly_matched_output_for_image_Matplotlib(self):
        os.chdir(ROOT_FOR_TESTS)
        interface = Osiris.UserInterface(image_Matplotlib_notebook_path)
        num_of_matched_cells, num_of_cells, match_ratio, matched_cell_idx, source_code_from_unmatched_cells = interface.analyse_outputs(
            verbose=False, store=False, analyze_strategy='OEC', strong_match=False)
        self.assertEqual(num_of_matched_cells, 2)
        self.assertEqual(num_of_cells, 2)


if __name__ == '__main__':
    unittest.main()
