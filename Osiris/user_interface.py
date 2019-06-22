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

    def analyse(self):
        assert self._py_version in ['2.7', '3.4', '3.5', '3.6', '3.7']

        conda_env = None
        if self._py_version == '2.7':
            conda_env = 'python2'
        elif self._py_version == '3.4':
            conda_env = 'python34'
        elif self._py_version == '3.5':
            conda_env = 'python35'
        elif self._py_version == '3.6':
            conda_env = 'python36'
        else: #3.7
            conda_env = 'python37'

        CMD = ''
        CMD = combine_two_commands(CMD, 'conda activate '+conda_env)
        CMD = combine_two_commands(CMD, 'python auto_analysize_script.py -n '+self.nb_path)
        CMD = combine_two_commands(CMD, 'conda deactivate')
        subprocess.call(CMD, shell=True)
