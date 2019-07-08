import sys
import os

import warnings
import unittest
import Osiris

test_executability_notebook_path = 'tests/test_executability.ipynb'
test_reproducibility_notebook_path = 'tests/test_reproducibility.ipynb'
test_self_reproducibility_notebook_path = 'tests/test_self_reproducibility.ipynb'
test_debug_for_a_cell_notebook_path = 'tests/test_debug_for_a_cell.ipynb'

test_IPythonDisplay_notebook_path = 'tests/test_IPythonDisplay.ipynb'
test_Matplotlib_notebook_path = 'tests/test_Matplotlib.ipynb'

# Global setting 
verbose = False
root_path = os.getcwd()

class TestOsiris(unittest.TestCase):

    def setUp(self):
        warnings.simplefilter('ignore', category=ImportWarning)
        warnings.simplefilter('ignore', category=DeprecationWarning)
        warnings.simplefilter('ignore', category=ResourceWarning)
        os.chdir(root_path)

    '''
    The following 3 unit tests focus executability
    '''
    def test_normal_executability(self):
        interface = Osiris.UserInterface(test_executability_notebook_path, verbose)
        is_executable = interface.analyse_executability('normal')
        self.assertEqual(is_executable, True)

    def test_OEC_executability(self):
        interface = Osiris.UserInterface(test_executability_notebook_path, verbose)
        is_executable = interface.analyse_executability('OEC')
        self.assertEqual(is_executable, True)

    def test_dependency_executability(self):
        interface = Osiris.UserInterface(test_executability_notebook_path, verbose)
        is_executable = interface.analyse_executability('dependency')
        self.assertEqual(is_executable, True)

    '''
    The following 6 unit tests focus reproducibility
    '''
    def test_top_down_strong_reproducibility(self):
        interface = Osiris.UserInterface(test_reproducibility_notebook_path, verbose)
        num_of_matched_cells, num_of_cells, match_ratio, matched_cell_idx, source_code_from_unmatched_cells = interface.analyse_reproducibility('normal', 'strong')
        self.assertEqual(num_of_matched_cells, 6)
        self.assertEqual(num_of_cells, 8)

    def test_top_down_weak_reproducibility(self):
        interface = Osiris.UserInterface(test_reproducibility_notebook_path, verbose)
        num_of_matched_cells, num_of_cells, match_ratio, matched_cell_idx, source_code_from_unmatched_cells = interface.analyse_reproducibility('normal', 'weak')
        self.assertEqual(num_of_matched_cells, 8)
        self.assertEqual(num_of_cells, 8)

    def test_OEC_strong_reproducibility(self):
        interface = Osiris.UserInterface(test_reproducibility_notebook_path, verbose)
        num_of_matched_cells, num_of_cells, match_ratio, matched_cell_idx, source_code_from_unmatched_cells = interface.analyse_reproducibility('OEC', 'strong')
        self.assertEqual(num_of_matched_cells, 8)
        self.assertEqual(num_of_cells, 8)

    def test_OEC_weak_reproducibility(self):
        interface = Osiris.UserInterface(test_reproducibility_notebook_path, verbose)
        num_of_matched_cells, num_of_cells, match_ratio, matched_cell_idx, source_code_from_unmatched_cells = interface.analyse_reproducibility('OEC', 'weak')
        self.assertEqual(num_of_matched_cells, 8)
        self.assertEqual(num_of_cells, 8)

    def test_dependency_strong_reproducibility(self):
        interface = Osiris.UserInterface(test_reproducibility_notebook_path, verbose)
        num_of_matched_cells, num_of_cells, match_ratio, matched_cell_idx, source_code_from_unmatched_cells = interface.analyse_reproducibility('dependency', 'strong')
        self.assertEqual(num_of_matched_cells, 7) # BUGGY STATEMENT 
        self.assertEqual(num_of_cells, 8)

    def test_dependency_weak_reproducibility(self):
        interface = Osiris.UserInterface(test_reproducibility_notebook_path, verbose)
        num_of_matched_cells, num_of_cells, match_ratio, matched_cell_idx, source_code_from_unmatched_cells = interface.analyse_reproducibility('dependency', 'weak')
        self.assertEqual(num_of_matched_cells, 8)
        self.assertEqual(num_of_cells, 8)

    '''
    The following 3 unit tests focus self-reproducibility
    '''
    def test_top_down_self_reproducibility(self):
        interface = Osiris.UserInterface(test_self_reproducibility_notebook_path, verbose)
        num_of_reproducible_cells, num_of_cells, reproducible_ratio, reproducible_cell_idx = interface.analyse_self_reproducibility('normal')
        self.assertEqual(num_of_reproducible_cells, 2)
        self.assertEqual(num_of_cells, 4)
        self.assertEqual(reproducible_cell_idx, [0, 3])

    def test_OEC_self_reproducibility(self):
        interface = Osiris.UserInterface(test_self_reproducibility_notebook_path, verbose)
        num_of_reproducible_cells, num_of_cells, reproducible_ratio, reproducible_cell_idx = interface.analyse_self_reproducibility('OEC')
        self.assertEqual(num_of_reproducible_cells, 2)
        self.assertEqual(num_of_cells, 4)
        self.assertEqual(reproducible_cell_idx, [0, 1])

    def test_dependency_self_reproducibility(self):
        interface = Osiris.UserInterface(test_self_reproducibility_notebook_path, verbose)
        num_of_reproducible_cells, num_of_cells, reproducible_ratio, reproducible_cell_idx = interface.analyse_self_reproducibility('dependency')
        self.assertEqual(num_of_reproducible_cells, 2)
        self.assertEqual(num_of_cells, 4)

    '''
    The following 3 unit tests focus status difference inspection
    '''
    def test_top_down_debug_for_a_cell(self):
        interface = Osiris.UserInterface(
            test_debug_for_a_cell_notebook_path, verbose)
        problematic_statement_index = interface.analyse_status_difference_for_a_cell('normal', cell_index=1)
        self.assertEqual(problematic_statement_index, 9)

    def test_OEC_debug_for_a_cell(self):
        interface = Osiris.UserInterface(test_debug_for_a_cell_notebook_path, verbose)
        problematic_statement_index = interface.analyse_status_difference_for_a_cell('OEC', 2)
        self.assertEqual(problematic_statement_index, 9)

    def test_dependency_debug_for_a_cell(self):
        interface = Osiris.UserInterface(test_debug_for_a_cell_notebook_path, verbose)
        problematic_statement_index = interface.analyse_status_difference_for_a_cell('dependency', 1)
        self.assertEqual(problematic_statement_index, 9)

    '''
    The following 2 unit tests focus on the correctness of Osiris for images 
    '''
    def test_image_IPythonDisplay(self):
        interface = Osiris.UserInterface(test_IPythonDisplay_notebook_path, verbose)
        num_of_matched_cells, num_of_cells, match_ratio, matched_cell_idx, source_code_from_unmatched_cells = interface.analyse_reproducibility('OEC', 'weak')
        self.assertEqual(num_of_matched_cells, 1)
        self.assertEqual(num_of_cells, 1)

    def test_image_Matplotlib(self):
        interface = Osiris.UserInterface(test_Matplotlib_notebook_path, verbose)
        num_of_matched_cells, num_of_cells, match_ratio, matched_cell_idx, source_code_from_unmatched_cells = interface.analyse_reproducibility('OEC', 'weak')
        self.assertEqual(num_of_matched_cells, 2)
        self.assertEqual(num_of_cells, 2)

if __name__ == '__main__':
    unittest.main()
