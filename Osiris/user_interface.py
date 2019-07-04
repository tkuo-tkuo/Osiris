import subprocess
import os
import sys
import csv
from .analysizer import Analysizer


class UserInterface():

    def __init__(self, path, verbose):
        # Store the path of the given notebook
        # Note the path is relative path
        self._nb_path = path
        self._verbose = verbose

        # Extract python version
        self._py_version = None
        f = open(self._nb_path, 'r', encoding='utf-8')
        self.analysizer = Analysizer(path, f)
        self._py_version = self.analysizer.return_py_version()

        self._root_path = os.getcwd()
 
    def return_py_version(self):
        return self._py_version

    def analyse_executability(self, analyse_strategy):
        assert self._py_version in ['3.5', '3.6', '3.7']

        path_split_lst = self._nb_path.split('/')
        # We need to cd to the same directory as the notebook
        if len(path_split_lst) > 1:
            cd_path_lst = path_split_lst[:-1]
            cd_path = '/'.join(cd_path_lst)
            os.chdir(self._root_path)
            os.chdir(cd_path)

        assert analyse_strategy in ['OEC', 'normal', 'dependency']
        is_executable = self.analysizer.check_executability(
            self._verbose, analyse_strategy)

        return is_executable

    def analyse_reproducibility(self, analyse_strategy, match_pattern):
        assert self._py_version in ['3.5', '3.6', '3.7']

        path_split_lst = self._nb_path.split('/')
        # We need to cd to the same directory as the notebook
        if len(path_split_lst) > 1:
            cd_path_lst = path_split_lst[:-1]
            cd_path = '/'.join(cd_path_lst)
            os.chdir(self._root_path)
            os.chdir(cd_path)

        # Analysing & Return & Storing (optinal)
        assert analyse_strategy in ['OEC', 'normal', 'dependency']
        assert match_pattern in ['strong', 'weak', 'best_effort']
        num_of_matched_cells, num_of_cells, match_ratio, match_cell_idx, source_code_from_unmatched_cells = self.analysizer.check_reproducibility(
            self._verbose, analyse_strategy, match_pattern)

        return num_of_matched_cells, num_of_cells, match_ratio, match_cell_idx, source_code_from_unmatched_cells

    def analyse_self_reproducibility(self, analyse_strategy):
        assert self._py_version in ['3.5', '3.6', '3.7']

        path_split_lst = self._nb_path.split('/')
        # We need to cd to the same directory as the notebook
        if len(path_split_lst) > 1:
            cd_path_lst = path_split_lst[:-1]
            cd_path = '/'.join(cd_path_lst)
            os.chdir(self._root_path)
            os.chdir(cd_path)

        # Analysing & Return & Storing (optinal)
        assert analyse_strategy in ['OEC', 'normal', 'dependency']
        num_of_reproducible_cells, num_of_cells, reproducible_ratio, reproducible_cell_idx = self.analysizer.check_self_reproducibility(
            self._verbose, analyse_strategy)

        return num_of_reproducible_cells, num_of_cells, reproducible_ratio, reproducible_cell_idx

    def analyse_status_difference_for_a_cell(self, analyse_strategy, cell_index):
        if cell_index == None:
            raise ValueError('cell_index argument should not be empty (None), please indicate the cell_index.')
        
        assert self._py_version in ['3.5', '3.6', '3.7']

        path_split_lst = self._nb_path.split('/')
        # We need to cd to the same directory as the notebook
        if len(path_split_lst) > 1:
            cd_path_lst = path_split_lst[:-1]
            cd_path = '/'.join(cd_path_lst)
            os.chdir(self._root_path)
            os.chdir(cd_path)

        # Analysing & Return & Storing (optinal)
        assert analyse_strategy in ['OEC', 'normal', 'dependency']
        problematic_statement_index = self.analysizer.check_status_difference_for_a_cell(analyse_strategy, cell_index)
        
        if problematic_statement_index is None:
            print('Statements in this cell did not cause any status difference of self-defined variables')
        elif problematic_statement_index is -1:
            print('Status difference of self-defined variables may occur before any execution of statements in this cell')
        else: 
            print('The potential statement for causing status difference is line', problematic_statement_index)
            print('(Note that 0 indicates for the first line and empty lines are also included)')
        
        return problematic_statement_index

        
