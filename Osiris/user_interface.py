import subprocess, os, sys
from .analysizer import Analysizer
from .utils import combine_two_commands

class UserInterface():

    def __init__(self, path):
        # Store the path of the given notebook  
        # Note the path is relative path 
        self._nb_path = path 

        # Extract python version
        self._py_version = None
        f = open(self._nb_path, 'r', encoding='utf-8')
        self.analysizer = Analysizer(f)
        self._py_version = self.analysizer.return_py_version()

        # Set conda env indication for corresponding python version
        self._conda_env = None
        self._conda_env = self._get_conda_env_indication(self._py_version)
        
        # Set conda env according to the conda env indication 
        self._set_conda_env()

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

    def _set_conda_env(self):
        # If Osiris can not realize which python version is used by a given notebook, Osiris configurates python 3.7
        if self._conda_env in ['py35', 'py36', 'py37']:
           os.environ['PATH'] = '/home/dabao/miniconda3/envs/'+self._conda_env+'/bin'+os.pathsep+os.environ.get('PATH', '')
        else:
           os.environ['PATH'] = '/home/dabao/miniconda3/envs/py37/bin'+os.pathsep+os.environ.get('PATH', '')  

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
       
        is_executable = self.analysizer.check_executability(verbose, analyze_strategy)
        if store:
            # OPEN CSV FILE FOR STORAGE
            csv_name_for_storage = 'Saved_analyse_executability_results_'+analyze_strategy+'.csv'
            csv_file = open(csv_name_for_storage, 'a')
            writer = csv.writer(csv_file)

            # RUN SOMETHING IN CSV FILE
            pass 

        

        '''
        num_of_reproductive_cells, num_of_cells, reproductivity_ratio, reproductive_cell_idx, source_code_from_non_reproductive_cells = self.analysizer.check_reproductivity(verbose, analyze_strategy)

        if store:
            if analyze_strategy == 'OEC':
                csv_path_for_storing_analyzed_results = 'analyzed_results_OEC.csv'
            else:
                csv_path_for_storing_analyzed_results = 'analyzed_results_normal.csv'
            
            csv_file_for_storing_analyzed_results = open(csv_path_for_storing_analyzed_results, 'a')
            writer_for_storing_analyzed_results = csv.writer(csv_file_for_storing_analyzed_results)
        
            if analyze_strategy == 'OEC':
                csv_path_for_storing_source_code_of_non_reproductive_cells = 'source_code_of_non_reproductive_cells_OEC.csv'
                csv_file_for_storing_source_code_of_non_reproductive_cells = open(csv_path_for_storing_source_code_of_non_reproductive_cells, 'a') 
                writer_for_storing_source_code_of_non_reproductive_cells = csv.writer(csv_file_for_storing_source_code_of_non_reproductive_cells)

            row = []
            row.append(is_executable)
            row.append(num_of_reproductive_cells)
            row.append(num_of_cells)
            row.append(reproductivity_ratio)
            row.append(reproductive_cell_idx)
            # print('Results:', row)
            
            writer_for_storing_analyzed_results.writerow(row) 

            if analyze_strategy == 'OEC':
                for source_code in source_code_from_non_reproductive_cells:
                    writer_for_storing_source_code_of_non_reproductive_cells.writerow([source_code])   
        '''

    def analyse_outputs(self, verbose=True, store=False, analyze_strategy='OEC', strong_match=True):
        pass
















