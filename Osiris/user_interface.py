import subprocess
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

    def analyse(self, verbose=True):
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
        
            if verbose:
                CMD = combine_two_commands(CMD, 'python auto_analysize_script.py -n "'+notebook_path+'"')
            else:
                CMD = combine_two_commands(CMD, 'python auto_analysize_script.py -v -n "'+notebook_path+'"')
           
            CMD = combine_two_commands(CMD, 'deactivate')
        else:
            CMD = combine_two_commands(CMD, 'activate '+conda_env)
            CMD = combine_two_commands(CMD, 'python auto_analysize_script.py -n '+self.nb_path)
            CMD = combine_two_commands(CMD, 'deactivate')

        # print(CMD)
        return subprocess.call(CMD, shell=True)
