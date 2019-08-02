import sys
import os

import warnings
import unittest
import Osiris

test_executability_notebook_path = 'tests/test_executability.ipynb'
test_reproducibility_notebook_path = 'tests/test_reproducibility.ipynb'
test_best_effort_notebook_path = 'tests/test_best_effort.ipynb' # It's for sub testset among reproducibility test set 
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
        interface = Osiris.UserInterface(test_executability_notebook_path, 'normal', verbose)
        is_executable = interface.analyse_executability()
        self.assertEqual(is_executable, True)

    def test_OEC_executability(self):
        interface = Osiris.UserInterface(test_executability_notebook_path, 'OEC', verbose)
        is_executable = interface.analyse_executability()
        self.assertEqual(is_executable, True)

    def test_dependency_executability(self):
        interface = Osiris.UserInterface(test_executability_notebook_path, 'dependency', verbose)
        is_executable = interface.analyse_executability()
        self.assertEqual(is_executable, True)

    '''
    The following 9 unit tests focus reproducibility
    '''
    def test_top_down_strong_reproducibility(self):
        interface = Osiris.UserInterface(test_reproducibility_notebook_path, 'normal', verbose)
        num_of_matched_cells, num_of_cells, _, _, _ = interface.analyse_reproducibility('strong')
        self.assertEqual(num_of_matched_cells, 6)
        self.assertEqual(num_of_cells, 8)

    def test_top_down_weak_reproducibility(self):
        interface = Osiris.UserInterface(test_reproducibility_notebook_path, 'normal', verbose)
        num_of_matched_cells, num_of_cells, _, _, _ = interface.analyse_reproducibility('weak')
        self.assertEqual(num_of_matched_cells, 8)
        self.assertEqual(num_of_cells, 8)

    def test_OEC_strong_reproducibility(self):
        interface = Osiris.UserInterface(test_reproducibility_notebook_path, 'OEC', verbose)
        num_of_matched_cells, num_of_cells, _, _, _ = interface.analyse_reproducibility('strong')
        self.assertEqual(num_of_matched_cells, 8)
        self.assertEqual(num_of_cells, 8)

    def test_OEC_weak_reproducibility(self):
        interface = Osiris.UserInterface(test_reproducibility_notebook_path, 'OEC', verbose)
        num_of_matched_cells, num_of_cells, _, _, _ = interface.analyse_reproducibility('weak')
        self.assertEqual(num_of_matched_cells, 8)
        self.assertEqual(num_of_cells, 8)

    def test_dependency_strong_reproducibility(self):
        interface = Osiris.UserInterface(test_reproducibility_notebook_path, 'dependency', verbose)
        num_of_matched_cells, num_of_cells, _, _, _ = interface.analyse_reproducibility('strong')
        self.assertEqual(num_of_matched_cells, 7) # BUGGY STATEMENT 
        self.assertEqual(num_of_cells, 8)

    def test_dependency_weak_reproducibility(self):
        interface = Osiris.UserInterface(test_reproducibility_notebook_path, 'dependency', verbose)
        num_of_matched_cells, num_of_cells, _, _, _ = interface.analyse_reproducibility('weak')
        self.assertEqual(num_of_matched_cells, 8)
        self.assertEqual(num_of_cells, 8)

    # For best_effort match pattern, we carefully crafted a notebook for testing best_effort match pattern 
    def test_top_down_best_effort_reproducibility(self):
        interface = Osiris.UserInterface(test_best_effort_notebook_path, 'normal', verbose)
        num_of_matched_cells, num_of_cells, _, _, _ = interface.analyse_reproducibility('best_effort')
        self.assertEqual(num_of_matched_cells, 7)
        self.assertEqual(num_of_cells, 7)

    def test_OEC_best_effort_reproducibility(self):
        interface = Osiris.UserInterface(test_best_effort_notebook_path, 'OEC', verbose)
        num_of_matched_cells, num_of_cells, _, _, _ = interface.analyse_reproducibility('best_effort')
        self.assertEqual(num_of_matched_cells, 7)
        self.assertEqual(num_of_cells, 7)
        
    def test_dependency_best_effort_reproducibility(self):
        interface = Osiris.UserInterface(test_best_effort_notebook_path, 'dependency', verbose)
        num_of_matched_cells, num_of_cells, _, _, _ = interface.analyse_reproducibility('best_effort')
        self.assertEqual(num_of_matched_cells, 7)
        self.assertEqual(num_of_cells, 7)

    '''
    The following 3 unit tests focus self-reproducibility
    '''
    def test_top_down_self_reproducibility(self):
        interface = Osiris.UserInterface(test_self_reproducibility_notebook_path, 'normal', verbose)
        num_of_reproducible_cells, num_of_cells, _, reproducible_cell_idx = interface.analyse_self_reproducibility()
        self.assertEqual(num_of_reproducible_cells, 2)
        self.assertEqual(num_of_cells, 4)
        self.assertEqual(reproducible_cell_idx, [0, 3])

    def test_OEC_self_reproducibility(self):
        interface = Osiris.UserInterface(test_self_reproducibility_notebook_path, 'OEC', verbose)
        num_of_reproducible_cells, num_of_cells, _, reproducible_cell_idx = interface.analyse_self_reproducibility()
        self.assertEqual(num_of_reproducible_cells, 2)
        self.assertEqual(num_of_cells, 4)
        self.assertEqual(reproducible_cell_idx, [0, 1])

    def test_dependency_self_reproducibility(self):
        interface = Osiris.UserInterface(test_self_reproducibility_notebook_path, 'dependency', verbose)
        num_of_reproducible_cells, num_of_cells, _, _ = interface.analyse_self_reproducibility()
        self.assertEqual(num_of_reproducible_cells, 2)
        self.assertEqual(num_of_cells, 4)

    '''
    The following 3 unit tests focus status difference inspection
    '''
    def test_top_down_debug_for_a_cell(self):
        interface = Osiris.UserInterface(test_debug_for_a_cell_notebook_path, 'normal', verbose)
        problematic_statement_index = interface.analyse_status_difference_for_a_cell(1)
        self.assertEqual(problematic_statement_index, 9)

    def test_OEC_debug_for_a_cell(self):
        interface = Osiris.UserInterface(test_debug_for_a_cell_notebook_path, 'OEC', verbose)
        problematic_statement_index = interface.analyse_status_difference_for_a_cell(2)
        self.assertEqual(problematic_statement_index, 9)

    def test_dependency_debug_for_a_cell(self):
        interface = Osiris.UserInterface(test_debug_for_a_cell_notebook_path, 'dependency', verbose)
        problematic_statement_index = interface.analyse_status_difference_for_a_cell(1)
        self.assertEqual(problematic_statement_index, 9)

    '''
    The following 2 unit tests focus on the correctness of Osiris for images 
    '''
    def test_image_IPythonDisplay(self):
        interface = Osiris.UserInterface(test_IPythonDisplay_notebook_path, 'OEC', verbose)
        num_of_matched_cells, num_of_cells, _, _, _ = interface.analyse_reproducibility('weak')
        self.assertEqual(num_of_matched_cells, 1)
        self.assertEqual(num_of_cells, 1)

    def test_image_Matplotlib(self):
        interface = Osiris.UserInterface(test_Matplotlib_notebook_path, 'OEC', verbose)
        num_of_matched_cells, num_of_cells, _, _, _ = interface.analyse_reproducibility('weak')
        self.assertEqual(num_of_matched_cells, 2)
        self.assertEqual(num_of_cells, 2)

if __name__ == '__main__':
    unittest.main()
