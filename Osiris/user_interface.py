import subprocess
import os
import sys
import csv
from .analysizer import Analysizer


class UserInterface():

    def __init__(self, path):
        # Store the path of the given notebook
        # Note the path is relative path
        self._nb_path = path

        # Extract python version
        self._py_version = None
        f = open(self._nb_path, 'r', encoding='utf-8')
        self.analysizer = Analysizer(path, f)
        self._py_version = self.analysizer.return_py_version()

        # Set conda env indication for corresponding python version
        self._conda_env = None
        self._conda_env = self._get_conda_env_indication(self._py_version)

        # Set conda env according to the conda env indication
        # self._set_conda_env()

    def _get_conda_env_indication(self, py_version):
        if py_version is None:
            return None

        if py_version == '3.5':
            return 'py35'
        elif py_version == '3.6':
            return 'py36'
        elif py_version == '3.7':
            return 'py37'
        elif py_version in ['2.7', '3.4']:
            print('Osiris currently is not implemented for python 2.7/3.4')
            return None
        else:
            return None

    def return_py_version(self):
        return self._py_version

    def _set_conda_env(self):
        # If Osiris can not realize which python version is used by a given notebook, Osiris configurates python 3.7
        if self._conda_env in ['py35', 'py36', 'py37']:
            os.environ['PATH'] = '/home/dabao/miniconda3/envs/' + \
                self._conda_env+'/bin'+os.pathsep+os.environ.get('PATH', '')
        else:
            os.environ['PATH'] = '/home/dabao/miniconda3/envs/py37/bin' + \
                os.pathsep+os.environ.get('PATH', '')

        print(os.environ['PATH']) # For Debug purpose 

    '''
    verbose: Whether the terminal will print out analyzing process on the terminal    
    store: Whether analysized results will be stored for a given notebook 
    analyze_strategy: Top-down (normal) / OEC (original execution count) / dependency
        - top-down (normal): execute Eells from the top one to the bottom one in a notebook 
        - OEC: Execute cells in increasing execution_count order 
        - dependency: Execute cells by depth-first order in cell-dependency graph
    strong_match: If True, we check whether individual cell is strongly matched. 
                  Otherwise, we check whether individual cell is weakly matched.  
    '''

    def analyse_executability(self, verbose=True, store=False, analyze_strategy='OEC'):
        assert self._py_version in ['3.5', '3.6', '3.7']

        path_split_lst = self._nb_path.split('/')
        # We need to cd to the same directory as the notebook
        if len(path_split_lst) > 1:
            cd_path_lst = path_split_lst[:-1]
            cd_path = '/'.join(cd_path_lst)
            os.chdir(cd_path)

        is_executable = self.analysizer.check_executability(
            verbose, analyze_strategy)

        if store:
            csv_name_for_storage = 'Saved_analyse_executability_results_'+analyze_strategy+'.csv'
            csv_file = open(csv_name_for_storage, 'a')
            writer = csv.writer(csv_file)

            row = []
            row.append(is_executable)
            writer.writerow(row)

        return is_executable

    def analyse_outputs(self, verbose=True, store=False, analyze_strategy='OEC', strong_match=True):
        assert self._py_version in ['3.5', '3.6', '3.7']

        path_split_lst = self._nb_path.split('/')
        # We need to cd to the same directory as the notebook
        if len(path_split_lst) > 1:
            cd_path_lst = path_split_lst[:-1]
            cd_path = '/'.join(cd_path_lst)
            os.chdir(cd_path)

        # Analysing & Return & Storing (optinal)
        assert analyze_strategy in ['OEC', 'normal', 'dependency']
        num_of_matched_cells, num_of_cells, match_ratio, match_cell_idx, source_code_from_unmatched_cells = self.analysizer.check_output(
            verbose, analyze_strategy, strong_match)

        if store:
            if strong_match:
                csv_name_for_storage = 'Saved_analyse_output_strong_match_results_' + \
                    analyze_strategy+'.csv'
            else:
                csv_name_for_storage = 'Saved_analyse_output_weak_match_results_'+analyze_strategy+'.csv'
            csv_file = open(csv_name_for_storage, 'a')
            writer = csv.writer(csv_file)

            row = []
            row.append(num_of_matched_cells)
            row.append(num_of_cells)
            row.append(match_ratio)
            row.append(match_cell_idx)
            writer.writerow(row)

        return num_of_matched_cells, num_of_cells, match_ratio, match_cell_idx, source_code_from_unmatched_cells

    def analyse_reproducibility(self, verbose=True, store=False, analyze_strategy='OEC'):
        assert self._py_version in ['3.5', '3.6', '3.7']

        path_split_lst = self._nb_path.split('/')
        # We need to cd to the same directory as the notebook
        if len(path_split_lst) > 1:
            cd_path_lst = path_split_lst[:-1]
            cd_path = '/'.join(cd_path_lst)
            os.chdir(cd_path)

        # Analysing & Return & Storing (optinal)
        assert analyze_strategy in ['OEC', 'normal', 'dependency']
        num_of_reproducible_cells, num_of_cells, reproducible_ratio, reproducible_cell_idx = self.analysizer.check_reproducibility(
            verbose, analyze_strategy)

        if store:
            csv_name_for_storage = 'Saved_analyse_reproducibility_results_'+analyze_strategy+'.csv'
            csv_file = open(csv_name_for_storage, 'a')
            writer = csv.writer(csv_file)

            row = []
            row.append(num_of_reproducible_cells)
            row.append(num_of_cells)
            row.append(reproducible_ratio)
            row.append(reproducible_cell_idx)
            writer.writerow(row)

        return num_of_reproducible_cells, num_of_cells, reproducible_ratio, reproducible_cell_idx

    def analyse_status_difference_for_a_cell(self, verbose=True, store=False, analyze_strategy='OEC', cell_index=None):
        if cell_index == None:
            raise ValueError('cell_index argument should not be empty (None), please indicate the cell_index.')
        
        assert self._py_version in ['3.5', '3.6', '3.7']

        path_split_lst = self._nb_path.split('/')
        # We need to cd to the same directory as the notebook
        if len(path_split_lst) > 1:
            cd_path_lst = path_split_lst[:-1]
            cd_path = '/'.join(cd_path_lst)
            os.chdir(cd_path)

        # Analysing & Return & Storing (optinal)
        assert analyze_strategy in ['OEC', 'normal', 'dependency']
        problematic_statement_index = self.analysizer.check_status_difference_for_a_cell(analyze_strategy, cell_index)
        
        if verbose:
            if problematic_statement_index is None:
                print('Statements in this cell did not cause any status difference of self-defined variables')
            elif problematic_statement_index is -1:
                print('Status difference of self-defined variables may occur before any execution of statements in this cell')
            else: 
                print('The potential statement for causing status difference is line', problematic_statement_index)
                print('(Note that 0 indicates for the first line and empty lines are also included)')

        if store:
            csv_name_for_storage = 'Saved_analyse_reproducibility_results_'+analyze_strategy+'_for_cell_'+str(cell_index)+'.csv'
            csv_file = open(csv_name_for_storage, 'a')
            writer = csv.writer(csv_file)

            row = []
            row.append(problematic_statement_index)
            row.append(-1)
            row.append(None)
            writer.writerow(row)
            
        return problematic_statement_index

        
