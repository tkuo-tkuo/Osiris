import sys
import os

from Osiris.utils import *
import csv
import warnings
import unittest
import Osiris
from Osiris.analysizer import Analysizer

naive_notebook_path = 'tests/test_case_1.ipynb'
image_IPythonDisplay_notebook_path = 'tests/test_case_2.ipynb'
image_Matplotlib_notebook_path = 'tests/test_case_3.ipynb'
relative_notebook_path = 'tests/folder/test_case_4.ipynb'
analyze_strategy_notebook_path = 'tests/test_case_5.ipynb'
status_inspection_for_a_cell_notebook_path = 'tests/test_case_6.ipynb'
variables_dependency_notebook_path = 'tests/test_case_7.ipynb'
packages_dependency_notebook_path = 'tests/test_case_8.ipynb'
output_matching_analyse_via_dependency_strategy_notebook_path = 'tests/test_case_9.ipynb'

verbose = False
root_path = os.getcwd()

class TestOsiris(unittest.TestCase):

    def setUp(self):
        warnings.simplefilter('ignore', category=ImportWarning)
        warnings.simplefilter('ignore', category=DeprecationWarning)
        warnings.simplefilter('ignore', category=ResourceWarning)
        os.chdir(root_path)

    # Conda environment required
    def test_relative_path(self):
        interface = Osiris.UserInterface(relative_notebook_path, verbose)
        is_executable = interface.analyse_executability('OEC')
        self.assertEqual(is_executable, True)

    def test_top_down_analyse_executability(self):
        interface = Osiris.UserInterface(analyze_strategy_notebook_path, verbose)
        is_executable = interface.analyse_executability('normal')
        self.assertEqual(is_executable, True)

    def test_OEC_analyse_executability(self):
        interface = Osiris.UserInterface(analyze_strategy_notebook_path, verbose)
        is_executable = interface.analyse_executability('OEC')
        self.assertEqual(is_executable, True)

    def test_dependency_analyse_executability_case_1(self):
        interface = Osiris.UserInterface(variables_dependency_notebook_path, verbose)
        is_executable = interface.analyse_executability('dependency')
        self.assertEqual(is_executable, True)

    def test_dependency_analyse_executability_case_2(self):
        interface = Osiris.UserInterface(packages_dependency_notebook_path, verbose)
        is_executable = interface.analyse_executability('dependency')
        self.assertEqual(is_executable, True)

    def test_top_down_analyse_strongly_matched_ouptut(self):
        interface = Osiris.UserInterface(analyze_strategy_notebook_path, verbose)
        num_of_matched_cells, num_of_cells, match_ratio, matched_cell_idx, source_code_from_unmatched_cells = interface.analyse_reproducibility('normal', 'strong')
        self.assertEqual(num_of_matched_cells, 1)
        self.assertEqual(num_of_cells, 3)

    def test_top_down_analyse_weakly_matched_ouptut(self):
        interface = Osiris.UserInterface(analyze_strategy_notebook_path, verbose)
        num_of_matched_cells, num_of_cells, match_ratio, matched_cell_idx, source_code_from_unmatched_cells = interface.analyse_reproducibility('normal', 'weak')
        self.assertEqual(num_of_matched_cells, 3)
        self.assertEqual(num_of_cells, 3)

    def test_OEC_analyse_strongly_matched_ouptut(self):
        interface = Osiris.UserInterface(analyze_strategy_notebook_path, verbose)
        num_of_matched_cells, num_of_cells, match_ratio, matched_cell_idx, source_code_from_unmatched_cells = interface.analyse_reproducibility('OEC', 'strong')
        self.assertEqual(num_of_matched_cells, 1)
        self.assertEqual(num_of_cells, 3)

    def test_OEC_analyse_weakly_matched_ouptut(self):
        interface = Osiris.UserInterface(analyze_strategy_notebook_path, verbose)
        num_of_matched_cells, num_of_cells, match_ratio, matched_cell_idx, source_code_from_unmatched_cells = interface.analyse_reproducibility('OEC', 'weak')
        self.assertEqual(num_of_matched_cells, 3)
        self.assertEqual(num_of_cells, 3)

    def test_dependency_analyse_strongly_matched_ouptut(self):
        interface = Osiris.UserInterface(output_matching_analyse_via_dependency_strategy_notebook_path, verbose)
        num_of_matched_cells, num_of_cells, match_ratio, matched_cell_idx, source_code_from_unmatched_cells = interface.analyse_reproducibility('dependency', 'strong')
        self.assertEqual(num_of_matched_cells, 6)
        self.assertEqual(num_of_cells, 8)

    def test_dependency_analyse_weakly_matched_ouptut(self):
        interface = Osiris.UserInterface(output_matching_analyse_via_dependency_strategy_notebook_path, verbose)
        num_of_matched_cells, num_of_cells, match_ratio, matched_cell_idx, source_code_from_unmatched_cells = interface.analyse_reproducibility('dependency', 'weak')
        self.assertEqual(num_of_matched_cells, 8)
        self.assertEqual(num_of_cells, 8)

    def test_top_down_analyse_self_reproducibility(self):
        interface = Osiris.UserInterface(naive_notebook_path, verbose)
        num_of_reproducible_cells, num_of_cells, reproducible_ratio, reproducible_cell_idx = interface.analyse_self_reproducibility('normal')
        self.assertEqual(num_of_reproducible_cells, 2)
        self.assertEqual(num_of_cells, 4)
        self.assertEqual(reproducible_cell_idx, [0, 3])

    def test_OEC_analyse_self_reproducibility(self):
        interface = Osiris.UserInterface(naive_notebook_path, verbose)
        num_of_reproducible_cells, num_of_cells, reproducible_ratio, reproducible_cell_idx = interface.analyse_self_reproducibility('OEC')
        self.assertEqual(num_of_reproducible_cells, 2)
        self.assertEqual(num_of_cells, 4)
        self.assertEqual(reproducible_cell_idx, [0, 1])

    def test_dependency_analyse_self_reproducibility(self):
        interface = Osiris.UserInterface(naive_notebook_path, verbose)
        num_of_reproducible_cells, num_of_cells, reproducible_ratio, reproducible_cell_idx = interface.analyse_self_reproducibility('dependency')
        self.assertEqual(num_of_reproducible_cells, 2)
        self.assertEqual(num_of_cells, 4)

    def test_top_down_analyse_status_difference_for_a_cell(self):
        interface = Osiris.UserInterface(status_inspection_for_a_cell_notebook_path, verbose)
        problematic_statement_index = interface.analyse_status_difference_for_a_cell('normal', cell_index=1)
        self.assertEqual(problematic_statement_index, 9)

    def test_OEC_analyse_status_difference_for_a_cell(self):
        interface = Osiris.UserInterface(status_inspection_for_a_cell_notebook_path, verbose)
        problematic_statement_index = interface.analyse_status_difference_for_a_cell('OEC', 2)
        self.assertEqual(problematic_statement_index, 9)

    def test_dependency_analyse_status_difference_for_a_cell(self):
        interface = Osiris.UserInterface(status_inspection_for_a_cell_notebook_path, verbose)
        problematic_statement_index = interface.analyse_status_difference_for_a_cell('dependency', 1)
        self.assertEqual(problematic_statement_index, 9)

    def test_OEC_analyse_weakly_matched_output_for_image_IPythonDisplay(self):
        interface = Osiris.UserInterface(image_IPythonDisplay_notebook_path, verbose)
        num_of_matched_cells, num_of_cells, match_ratio, matched_cell_idx, source_code_from_unmatched_cells = interface.analyse_reproducibility('OEC', 'weak')
        self.assertEqual(num_of_matched_cells, 1)
        self.assertEqual(num_of_cells, 1)

    def test_OEC_analyse_weakly_matched_output_for_image_Matplotlib(self):
        interface = Osiris.UserInterface(image_Matplotlib_notebook_path, verbose)
        num_of_matched_cells, num_of_cells, match_ratio, matched_cell_idx, source_code_from_unmatched_cells = interface.analyse_reproducibility('OEC', 'weak')
        self.assertEqual(num_of_matched_cells, 2)
        self.assertEqual(num_of_cells, 2)

if __name__ == '__main__':
    unittest.main()
