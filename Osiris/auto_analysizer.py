import csv
import subprocess
from AutoExeInterface import JupyterAutoExecuteInterface
import argparse

def combine_two_CMD(CMD1, CMD2):
    return CMD1 + ' && ' + CMD2

'''
Meta hyperparameters setting 
'''

parser = argparse.ArgumentParser(
    description='analysize Jupyter Notebook files')
parser.add_argument('--start-index', type=int, required=True)
parser.add_argument('--end-index', type=int, required=True)
args = parser.parse_args()

start_index_notebook_execution = args.start_index
num_of_notebooks_be_analysized = args.end_index
is_actual_executable = True
is_print_CMD = True

start_index_notebook_execution -= 1
AUTO_EXECUTOR_LOCATION = 'C:/Users/User/Desktop/Monash University Summer Research/JupiterUsagePatternMining/JupNB_AutoExecuter/JupyterAutoExecutor.py'
ROOT_PATH = 'C:/Users/User/Desktop/Monash University Summer Research/JupiterUsagePatternMining/JupNB_AutoExecuter'


'''
Initialization
'''
# Read the csv for traversing among files 
f = open('executable_Jup_NBs/downloaded_notebooks.csv', 'r', encoding='utf-8')
reader = csv.reader(f)

# Create an interface for automatic execution 
interface = None 
num_of_candidates = 0

'''
Executability/Reproductivity/Idempotent analysis
'''
for i, row in enumerate(reader):
    if i < num_of_notebooks_be_analysized and i >= start_index_notebook_execution:
        print()
        print()
        print('-----------------------------------------------------------------------')
        print("{i} th Jupyter Notebook file is being anlaysized...".format(i=i+1))
        repo, notebook_path = row[0], row[1]
        repo_lst = repo.split('/')
        folder_name = repo_lst[0] + '@' + repo_lst[1]
        path = 'executable_Jup_NBs/'+folder_name+'/'+notebook_path
        CMD = ''

        try:
            # 1. Extract meta information (Done)
            interface = JupyterAutoExecuteInterface(path)
            meta_info = interface.extract_meta_info()
            kernal = meta_info['kernelspec']['name']
            py_version_lst = meta_info['language_info']['version'].split('.')
            py_version = py_version_lst[0]+'.'+py_version_lst[1]
            print('Python version'.ljust(40), ':', py_version)

            if not py_version in ['2.7', '3.4', '3.5', '3.6', '3.7']:
                print(py_version, 'is uninstalled python version')
                continue

            # 2. According to the extracted meta information, we set different CMD so as to activate different conda environments
            if py_version == '2.7':
                CMD = 'conda activate python2'
            elif py_version == '3.4':
                CMD = 'conda activate python34'
            elif py_version == '3.5':
                CMD = 'conda activate python35'
            elif py_version == '3.6':
                CMD = 'conda activate python36'
            elif py_version == '3.7':
                CMD = 'conda activate python37'
            else:
                # if we can not obtain the exact python, we simply use python36
                CMD = 'conda activate python36'

            if py_version == '2.7':
                continue

            # CD
            cd_CMD_str = 'cd ' + 'executable_Jup_NBs/'+folder_name+'/'
            CMD = combine_two_CMD(CMD, cd_CMD_str)

            # 3. According to the missing modules, we filter out packages should be installed before execution. 
            missing_modules = interface.return_missing_modules()
            additional_installation_required_modules = ['sympy', 'requests']
            should_installed_modules = [module for module in missing_modules if (module in additional_installation_required_modules)]
            print('Packages used in the notebook'.ljust(40), ':', missing_modules)
            print('Packages will be additionally installed'.ljust(40), ':', should_installed_modules)

            for package in should_installed_modules:
                install_CMD_str = 'python -m pip -q install ' + package + ' --user'
                CMD = combine_two_CMD(CMD, install_CMD_str)

            # 4. Analysis: we set CMD for checking the executability/reproductivity/idempotent
            print()
            # execute_install_str = 'python "' + AUTO_EXECUTOR_LOCATION + '" -n "' + notebook_path + '" --check-executability' 
            execute_install_str = 'python "' + AUTO_EXECUTOR_LOCATION + '" -n "' + notebook_path + '" -r' 

            CMD = combine_two_CMD(CMD, execute_install_str)

            # execute_install_str = 'python JupyterAutoExecutor.py -n "' + path + '" --check-executability' 
            # CMD = combine_two_CMD(CMD, execute_install_str)

            # execute_install_str = 'python "' + AUTO_EXECUTOR_LOCATION + '" -n "' + notebook_path + '" --check-reproductivity' 
            # CMD = combine_two_CMD(CMD, execute_install_str)
            
            # execute_install_str = 'python JupyterAutoExecutor.py -n "' + path + '" --check-idempotent' 
            # CMD = combine_two_CMD(CMD, execute_install_str)
            
            back_to_root_CMD = 'cd "' + ROOT_PATH + '"'
            CMD = combine_two_CMD(CMD, back_to_root_CMD)

            CMD = combine_two_CMD(CMD, 'conda deactivate')
            if is_print_CMD:
                print(CMD)  
                num_of_candidates += 1
        except Exception as e:
            print(e)
            pass

        # 5. After all preparation works, at the final stage, we actuaclly notebooks by using subprocess.call
        try:
            if is_actual_executable:
                # subprocess.call(CMD, shell=True)
                pass 
        except:
            pass 

print(num_of_candidates)
f.close()






