import subprocess, os
from .analysizer import Analysizer
from .utils import combine_two_commands

class UserInterface():

    def __init__(self, path):
        # Store the path of the given notebook  
        self.nb_path = path 

        # Extract py_version
        self._py_version = None
        with open(self.nb_path, 'r', encoding='utf-8') as f:
            analysizer = Analysizer(f)
            self._py_version = analysizer.return_py_version()

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
    def analyse(self, verbose=True, store=False, analyze_strategy='OEC', strong_match=True):
        assert self._py_version in ['2.7', '3.4', '3.5', '3.6', '3.7']

        conda_env = None
        if self._py_version in ['2.7', '3.4']:
            print('We skip python 2.7/3.4 cases at this stage')
            return 
        elif self._py_version == '3.5':
            conda_env = 'py35'
        elif self._py_version == '3.6':
            conda_env = 'py36'
        else: #3.7
            conda_env = 'py37'

        CMD = ''

        path_split_lst = self.nb_path.split('/')
        cd_path = ''
        if len(path_split_lst) > 1:
            cd_path_lst, notebook_path = path_split_lst[:-1], path_split_lst[-1]
            cd_path = '/'.join(cd_path_lst)
            copy_script_path = cd_path+'/'+'auto_analysize_script.py'
           
            CMD = combine_two_commands(CMD, 'cp auto_analysize_script.py "'+copy_script_path+'"')
            CMD = combine_two_commands(CMD, 'cd '+cd_path)
            CMD = combine_two_commands(CMD, 'activate '+conda_env)
        
            execute_CMD = None
            if verbose and store:
                execute_CMD = 'python3 auto_analysize_script.py -s -n "'+notebook_path+'"'
            elif (not verbose) and store: 
                execute_CMD = 'python3 auto_analysize_script.py -v -s -n "'+notebook_path+'"'
            elif verbose and (not store):  
                execute_CMD = 'python3 auto_analysize_script.py -n "'+notebook_path+'"'
            else:
                execute_CMD = 'python3 auto_analysize_script.py -v -n "'+notebook_path+'"'

            if analyze_strategy == 'normal':
                execute_CMD = execute_CMD + ' -t'                  

            CMD = combine_two_commands(CMD, execute_CMD)
            
            CMD = combine_two_commands(CMD, 'deactivate')
        else:
            CMD = combine_two_commands(CMD, 'activate '+conda_env)
            CMD = combine_two_commands(CMD, 'python auto_analysize_script.py -n '+self.nb_path)
            CMD = combine_two_commands(CMD, 'deactivate')

        # print(CMD) # For DEBUG purpose 

        # DEVNULL is used to filter out all potential warning messages in Osiris' automatic execution
        DEVNULL = open(os.devnull, 'wb')
        return subprocess.call(CMD, shell=True, stderr=DEVNULL)
