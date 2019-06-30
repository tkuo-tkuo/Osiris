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
        analysizer = Analysizer(f)
        self._py_version = analysizer.return_py_version()

        # Set conda env indication for corresponding python version
        self._conda_env = None
        self._conda_env = self._get_conda_env_indication(self._py_version)
        
        # Set conda env according to the conda env indication 
        self._set_conda_env()

    def _get_conda_env_indication(self, py_version):
        if py_version is None:
            return None
        
        print(py_version, '!!!!!!!!')
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
    def analyse(self, verbose=True, store=False, analyze_strategy='OEC', strong_match=True):
        assert self._py_version in ['3.5', '3.6', '3.7']

        CMD = ''

        path_split_lst = self._nb_path.split('/')
        cd_path, notebook_name, execute_CMD = '', '', ''
        
        # We need to cd to the same directory as the notebook
        if len(path_split_lst) > 1:
            cd_path_lst, notebook_name = path_split_lst[:-1], path_split_lst[-1]
            cd_path = '/'.join(cd_path_lst)
            
            # Below two lines should removed # PENDING FOR BEING REMOVED
            # copy_script_path = cd_path+'/'+'auto_analysize_script.py'
            # CMD = combine_two_commands(CMD, 'cp auto_analysize_script.py "'+copy_script_path+'"')

            # CMD = combine_two_commands(CMD, 'cd '+cd_path) # PENDING FOR REPLACE 
            # print(os.getcwd())
            os.chdir(cd_path)
            # print(os.getcwd())
            
            # CMD = combine_two_commands(CMD, 'activate '+self._conda_env) # PENDING FOR REPLACE
            
            if verbose and store:
                execute_CMD = 'python3 auto_analysize_script.py -s -n "'+notebook_name+'"'
            elif (not verbose) and store: 
                execute_CMD = 'python3 auto_analysize_script.py -v -s -n "'+notebook_name+'"'
            elif verbose and (not store):  
                execute_CMD = 'python3 auto_analysize_script.py -n "'+notebook_name+'"'
            else:
                execute_CMD = 'python3 auto_analysize_script.py -v -n "'+notebook_name+'"'
        # no cd required  
        else:
            notebook_name = self._nb_path
            CMD = combine_two_commands(CMD, 'activate '+self._conda_env)
            execute_CMD = 'python3 auto_analysize_script.py -n "'+notebook_name+'"'

        if analyze_strategy == 'normal':
            execute_CMD = execute_CMD + ' --strategy normal'
        else:
            execute_CMD = execute_CMD + ' --strategy OEC'
        CMD = combine_two_commands(CMD, execute_CMD)
        
        CMD = combine_two_commands(CMD, 'deactivate')
           
        print(CMD) # For DEBUG purpose 

        # DEVNULL is used to filter out all potential warning messages in Osiris' automatic execution
        DEVNULL = open(os.devnull, 'wb')
        return subprocess.call(CMD, shell=True, stderr=DEVNULL)
