import sys
import os

import warnings
import unittest
import Osiris
from Osiris.utils import get_dependency_matrix

test_execute_in_normal_strategy_nb_path = 'benchbook/test_execute_in_normal_strategy.ipynb'
test_execute_in_OEC_strategy_nb_path = 'benchbook/test_execute_in_OEC_strategy.ipynb'
test_on_case_require_executing_a_cell_twice_nb_path = 'benchbook/test_on_case_require_executing_a_cell_twice.ipynb'

test_on_magic_function_nb_path = 'benchbook/test_on_magic_function.ipynb'

test_reproducibility_with_strong_match_pattern_nb_path = 'benchbook/test_reproducibility_with_strong_match_pattern.ipynb'
test_dict_issue_nb_path = 'benchbook/test_dict_issue.ipynb'
test_random_nb_path = 'benchbook/test_random.ipynb'
test_time_nb_path = 'benchbook/test_time.ipynb'
test_tiny_float_difference_nb_path = 'benchbook/test_tiny_float_difference.ipynb'
test_warning_nb_path = 'benchbook/test_warning.ipynb'
test_exclaimation_mark_nb_path = 'benchbook/test_exclaimation_mark.ipynb'

# Case 1: ipynb file in the same directory as Osiris; image in the same directory as ipynb file
test_relative_path_1_nb_path = 'test_relative_path_1.ipynb' 
# Case 2: ipynb file in the same directory as Osiris; image NOT in the same directory as ipynb file
test_relative_path_2_nb_path = 'test_relative_path_2.ipynb'
# Case 3: ipynb file NOT in the same directory as Osiris; image in the same directory as ipynb file
test_relative_path_3_nb_path = 'benchbook/test_relative_path_3.ipynb'
# Case 4: ipynb file NOT in the same directory as Osiris; image NOT in the same directory as ipynb file
test_relative_path_4_nb_path = 'benchbook/test_relative_path_4.ipynb'

# compound_assignment_operators refer to operators like +=, -=, *=, ...
test_compound_assignment_operators_nb_path = 'benchbook/test_compound_assignment_operators.ipynb'
test_package_dependency_nb_path = 'benchbook/test_package_dependency.ipynb'
test_irrational_path_nb_path = 'benchbook/test_irrational_path.ipynb'
test_implicit_var_definition_nb_path = 'benchbook/test_implicit_var_definition.ipynb'


# Global setting
verbose = True
root_path = os.getcwd()

class Benchbook(unittest.TestCase):

    def setUp(self):
        warnings.simplefilter('ignore', category=ImportWarning)
        warnings.simplefilter('ignore', category=DeprecationWarning)
        warnings.simplefilter('ignore', category=ResourceWarning)
        os.chdir(root_path)

    def test_execute_in_normal_strategy(self):
        interface = Osiris.UserInterface(test_execute_in_normal_strategy_nb_path, 'normal', verbose)
        is_executable = interface.analyse_executability()
        self.assertEqual(is_executable, True)

    def test_execute_in_OEC_strategy(self):
        interface = Osiris.UserInterface(test_execute_in_OEC_strategy_nb_path, 'OEC', verbose)
        is_executable = interface.analyse_executability()
        self.assertEqual(is_executable, True)

    def test_on_case_require_executing_a_cell_twice(self):
        interface = Osiris.UserInterface(test_on_case_require_executing_a_cell_twice_nb_path, 'OEC', verbose)
        is_executable = interface.analyse_executability()
        self.assertEqual(is_executable, False)

    def test_on_magic_function(self):
        interface = Osiris.UserInterface(test_on_magic_function_nb_path, 'dependency', verbose)
        num_of_matched_cells, num_of_cells, match_ratio, matched_cell_idx, source_code_from_unmatched_cells = interface.analyse_reproducibility('strong')
        self.assertEqual(num_of_cells, 2)

    '''
    The following 7 unit tests aim to test on reproducibility, which may cause challenges for Osiris to reproduce outputs 
    '''
    def test_reproducibility_with_strong_match_pattern(self):
        interface = Osiris.UserInterface(test_reproducibility_with_strong_match_pattern_nb_path, 'normal', verbose)
        num_of_matched_cells, num_of_cells, match_ratio, matched_cell_idx, source_code_from_unmatched_cells = interface.analyse_reproducibility('strong')
        self.assertEqual(match_ratio, 1.0)

    def test_dict_issue(self):
        interface = Osiris.UserInterface(test_dict_issue_nb_path, 'normal', verbose)
        num_of_matched_cells, num_of_cells, match_ratio, matched_cell_idx, source_code_from_unmatched_cells = interface.analyse_reproducibility('weak')
        self.assertEqual(match_ratio, 1.0)

    # Involves some issue 
    # Wait for Jarix to solve the issue 
    # Also, think about how this utils function can be leverged in Osiris 
    @unittest.skip 
    def test_random(self):
        interface = Osiris.UserInterface(test_random_nb_path, 'normal', verbose)
        num_of_matched_cells, num_of_cells, match_ratio, matched_cell_idx, source_code_from_unmatched_cells = interface.analyse_reproducibility('weak')

    def test_time(self):
        interface = Osiris.UserInterface(test_time_nb_path, 'normal', verbose)
        num_of_matched_cells, num_of_cells, match_ratio, matched_cell_idx, source_code_from_unmatched_cells = interface.analyse_reproducibility('weak')
        self.assertEqual(num_of_matched_cells, 0)

    def test_tiny_float_difference(self):
        interface = Osiris.UserInterface(test_tiny_float_difference_nb_path, 'normal', verbose)
        num_of_matched_cells, num_of_cells, match_ratio, matched_cell_idx, source_code_from_unmatched_cells = interface.analyse_reproducibility('strong')
        self.assertEqual(match_ratio, 1.0)

    def test_warning(self):
        interface = Osiris.UserInterface(test_warning_nb_path, 'normal', verbose)
        num_of_matched_cells, num_of_cells, match_ratio, matched_cell_idx, source_code_from_unmatched_cells = interface.analyse_reproducibility('weak')
        self.assertEqual(match_ratio, 1.0)

    # Involves some issue
    # Wait for Jarix to solve the issue
    # Also, think about how this utils function can be leverged in Osiris
    @unittest.skip
    def test_exclaimation_mark(self):
        pass

    '''
    The following 4 unit tests aim to test on relative path issues 
    '''
    def test_relative_path_1(self):
        interface = Osiris.UserInterface(test_relative_path_1_nb_path, 'normal', verbose)
        is_executable = interface.analyse_executability()
        self.assertEqual(is_executable, True)

    def test_relative_path_2(self):
        interface = Osiris.UserInterface(test_relative_path_2_nb_path, 'normal', verbose)
        is_executable = interface.analyse_executability()
        self.assertEqual(is_executable, True)

    def test_relative_path_3(self):
        interface = Osiris.UserInterface(test_relative_path_3_nb_path, 'normal', verbose)
        is_executable = interface.analyse_executability()
        self.assertEqual(is_executable, True)

    def test_relative_path_4(self):
        interface = Osiris.UserInterface(test_relative_path_3_nb_path, 'normal', verbose)
        is_executable = interface.analyse_executability()
        self.assertEqual(is_executable, True)


    '''
    The following 4 unit tests aim to test on potential challenges related to dependency 
    '''
    def test_compound_assignment_operators(self):
        dep_matrix = get_dependency_matrix(test_compound_assignment_operators_nb_path)
        self.assertEqual(dep_matrix[0][1], 1.0)

    def test_package_dependency(self):
        dep_matrix = get_dependency_matrix(test_package_dependency_nb_path)
        self.assertEqual(dep_matrix[0][1], 1.0)

    def test_irrational_path(self):
        dep_matrix = get_dependency_matrix(test_irrational_path_nb_path)
        self.assertEqual(dep_matrix[1][4], 1.0)
        self.assertEqual(dep_matrix[3][4], 1.0)
        self.assertEqual(dep_matrix[3][2], 0.0)

    def test_implicit_var_definition(self):
        dep_matrix = get_dependency_matrix(test_implicit_var_definition_nb_path)
        self.assertEqual(dep_matrix[2][3], 0.0)

if __name__ == '__main__':
    unittest.main()