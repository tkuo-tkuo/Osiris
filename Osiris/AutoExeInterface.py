import argparse
import nbformat
import subprocess
from nbconvert.preprocessors import ExecutePreprocessor


class TruncateExecutePreprocessor(ExecutePreprocessor):

    def __init__(self, start_index, end_index):
        super(ExecutePreprocessor, self).__init__()
        self.start_index = start_index
        self.end_index = end_index

    def preprocess(self, nb, resources):
        nb.cells = nb.cells[self.start_index:self.end_index]
        return super().preprocess(nb, resources)


'''
Customized ExecutePreprocessor 2, Skip mode
- A user needs to specify the cell indexes should be omitted

- Users should be able to omit by a given list (pass)
- If no list is given, work as normal mode (pass)
'''


class SkipExecutePreprocessor(ExecutePreprocessor):

    def __init__(self, skip_idx_list):
        super(ExecutePreprocessor, self).__init__()
        self.skip_idx_list = skip_idx_list

    def preprocess(self, nb, resources):
        copy_nb_cells = nb.cells
        parsed_nb_cells = [item for (idx, item) in enumerate(
            copy_nb_cells) if idx not in self.skip_idx_list]
        nb.cells = parsed_nb_cells
        return super().preprocess(nb, resources)


'''
Customized ExecutePreprocessor 3, Link mode
- A user needs to specify the order of cells should be executed

- Users should be able to execute by a given list (pass)
- If no list is given, should give a empty notebook (pass)
'''


class LinkExecutePreprocessor(ExecutePreprocessor):

    def __init__(self, link_idx_list):
        super(ExecutePreprocessor, self).__init__()
        self.link_idx_list = link_idx_list

    def preprocess(self, nb, resources):
        copy_nb_cells = nb.cells
        parsed_nb_cells = [copy_nb_cells[idx] for idx in self.link_idx_list]
        nb.cells = parsed_nb_cells
        return super().preprocess(nb, resources)


'''
Customized ExecutePreprocessor 4, OEO(Original Execution Order) mode
- This mode is used under the assumption that the target Jupyter Notebook has been executed

- Users should see the Jupyter Notebook re-executed according to OEO (pass)
- What if the notebook has not been executed? It should just raise some errors (pass)
'''


class OEOPreprocessor(ExecutePreprocessor):

    def __init__(self):
        super(ExecutePreprocessor, self).__init__()

    def preprocess(self, nb, resources):
        copy_nb_cells = nb.cells

        execution_count_lst = [cell.execution_count for cell in copy_nb_cells]
        OEO = sorted(range(len(execution_count_lst)),
                     key=lambda k: execution_count_lst[k])
        parsed_nb_cells = [copy_nb_cells[idx] for idx in OEO]

        nb.cells = parsed_nb_cells
        return super().preprocess(nb, resources)


'''
Idempotent analysis should achieve 4 objectives during execution:
1. Follow OEO execution path (Completed)
2. Insert variables extracttion functions at the beginning of the nb (Completed)
3. Check whether a cell is idempotent for every cell (waiting)
    a. First, check the first cell
        i. grab the result from SavedTargetNotebook (execute once)
        ii. store the result (execute once)
        iii. try to execute twice
        iv. grab the result from SavedTargetNotebook (execute twice)
        v. store the result (execute twice)
4. return (or print) the results (waiting)
'''


class IdempotentCheckPreprocessor(ExecutePreprocessor):

    def __init__(self, check_cell_idx, is_duplicate):
        super(ExecutePreprocessor, self).__init__()
        self.check_cell_idx = check_cell_idx
        self.is_duplicate = is_duplicate

    def preprocess(self, nb, resources):
        copy_nb_cells = nb.cells

        # Requirement 1
        execution_count_lst = [cell.execution_count for cell in copy_nb_cells]
        OEO = sorted(range(len(execution_count_lst)),
                     key=lambda k: execution_count_lst[k])
        parsed_nb_cells = [copy_nb_cells[idx] for idx in OEO]

        # Requirement 2
        extractVar_fun_str = "def extractVars():\n    variables_set = {}\n    tmp = globals().copy()\n    for k, v in tmp.items():\n        con_1 = not k.startswith('_')\n        con_2 = not k in ['In', 'Out', 'get_ipython', 'exit', 'quit']\n        con_3 = type(v) in [int, float, str, list, set, dict]\n        if con_1 and con_2 and con_3:\n            variables_set[k] = v\n    \n    return variables_set"
        var_extract_fun_cell = parsed_nb_cells[0].copy()
        var_extract_fun_cell.source = extractVar_fun_str
        parsed_nb_cells.insert(0, var_extract_fun_cell)

        if self.is_duplicate:
            copy_cell = parsed_nb_cells.copy()[self.check_cell_idx]
            parsed_nb_cells.insert(self.check_cell_idx+1, copy_cell)
        else:
            parsed_nb_cells[self.check_cell_idx].source += "\nextractVars()"

        nb.cells = parsed_nb_cells
        return super().preprocess(nb, resources)


class JupyterAutoExecuteInterface():

    def __init__(self, target_nb_name):
        self.nb = None
        self.ep = None
        self.target_nb_name = target_nb_name
        pass

    def load_nb(self):
        # Open and load the target Jupyter Notebook
        with open(self.target_nb_name, 'r', encoding='utf-8') as f:
            self.nb = nbformat.read(f, as_version=4)

        # Here we should clean nb before doing anything
        # For instance, raw cells & markdown cells & unexecuted cells
        self.clean_nb()
        # self.import_modules()

    def clean_nb(self):
        invalid_cells_idx = []
        for (idx, cell) in enumerate(self.nb.cells):
            if not (cell.cell_type == 'code'):
                invalid_cells_idx.append(idx)
                continue
            elif cell.execution_count == None:
                invalid_cells_idx.append(idx)
                continue
            else:
                pass
        parsed_nb_cells = [item for (idx, item) in enumerate(
            self.nb.cells) if idx not in invalid_cells_idx]

        self.nb.cells = parsed_nb_cells

    def import_modules(self):
        packages_should_be_installed = []
        for cell in self.nb.cells:
            codes = cell.source.split('\n')
            for code in codes:
                if 'import' in code:
                    words = code.split()
                    if words[0] == 'import':
                        package = words[1].split('.')[0]
                        packages_should_be_installed.append(package)
                    elif words[0] == 'from':
                        package = words[1].split('.')[0]
                        packages_should_be_installed.append(package)

        # print(packages_should_be_installed) # duplicate packages in this list should be removed

        for package in packages_should_be_installed:
            CMD = 'python -m pip install ' + package + ' --user'
            # subprocess.run(CMD, shell=True)

        # print(self.nb.metadata)

    def return_missing_modules(self):
        packages_should_be_installed = []
        for cell in self.nb.cells:
            codes = cell.source.split('\n')
            for code in codes:
                if 'import' in code:
                    words = code.split()
                    if words[0] == 'import':
                        package = words[1].split('.')[0]
                        packages_should_be_installed.append(package)
                    elif words[0] == 'from':
                        package = words[1].split('.')[0]
                        packages_should_be_installed.append(package)

        return list(set(packages_should_be_installed))

    def set_ep_as_normal_mode(self):
        self.ep = ExecutePreprocessor()

    def set_ep_as_truncate_mode(self, start_index, end_index):
        self.ep = TruncateExecutePreprocessor(start_index, end_index)

    def set_ep_as_skip_mode(self, skip_idx_list):
        self.ep = SkipExecutePreprocessor(skip_idx_list)

    def set_ep_as_link_mode(self, link_idx_list):
        self.ep = LinkExecutePreprocessor(link_idx_list)

    def set_ep_as_OEO_mode(self):
        self.ep = OEOPreprocessor()

    def set_ep_check_idempotent_mode(self, check_cell_idx, is_duplicate):
        self.ep = IdempotentCheckPreprocessor(check_cell_idx, is_duplicate)

    def execute_nb(self):
        self.ep.preprocess(self.nb, {'metadata': {'path': './'}})

    def store_nb(self, prefix=''):
        with open('Saved'+prefix+self.target_nb_name, 'w', encoding='utf-8') as f:
            nbformat.write(self.nb, f)

    def auto_execute_normal(self):
        self.load_nb()
        self.set_ep_as_normal_mode()
        self.execute_nb()
        self.store_nb()

    def auto_execute_truncate(self, start_index=0, end_index=None):
        self.load_nb()
        self.set_ep_as_truncate_mode(start_index, end_index)
        self.execute_nb()
        self.store_nb()

    def auto_execute_skip(self, skip_idx_list=[]):
        self.load_nb()
        self.set_ep_as_skip_mode(skip_idx_list)
        self.execute_nb()
        self.store_nb()

    def auto_execute_link(self, link_idx_list=[]):
        self.load_nb()
        self.set_ep_as_link_mode(link_idx_list)
        self.execute_nb()
        self.store_nb()

    def auto_execute_OEO(self):
        self.load_nb()
        self.set_ep_as_OEO_mode()
        self.execute_nb()
        self.store_nb()

    def check_idempotent_of_cells(self):
        self.load_nb()
        num_cells = len(self.nb.cells)
        copy_nb_lst = self.nb.cells.copy()
        idempotent_cell_idx = []

        for i in range(num_cells):
            check_cell_idx = i + 1

            # Get status variables if execute once
            is_duplicate = False
            self.nb.cells = copy_nb_lst.copy()
            self.set_ep_check_idempotent_mode(check_cell_idx, is_duplicate)
            self.execute_nb()
            check_cell_outputs = self.nb.cells[check_cell_idx].outputs
            var_status = check_cell_outputs[-1].data['text/plain']
            var_status_exe_once = var_status

            # DEBUG
            # self.store_nb(str(i)+'Once')

            # Get status variables if execute twice
            is_duplicate = True
            self.nb.cells = copy_nb_lst.copy()
            self.set_ep_check_idempotent_mode(check_cell_idx, is_duplicate)
            self.execute_nb()

            check_cell_outputs = self.nb.cells[check_cell_idx+1].outputs
            var_status = check_cell_outputs[-1].data['text/plain']
            var_status_exe_twice = var_status

            # DEBUG
            # self.store_nb(str(i)+'Twice')

            # Check whether a cell is idempotent & Print
            idemp_result = (var_status_exe_once == var_status_exe_twice)
            print("Check the {cell_idx}th cell among {num_cells} cells. Idempotent result: {Idemp_result}".format(
                cell_idx=check_cell_idx, num_cells=num_cells, Idemp_result=idemp_result))

            # Store results for further return
            if idemp_result:
                idempotent_cell_idx.append(i)

        # Return
        Idempotent_ratio = len(idempotent_cell_idx) / num_cells
        print("Idempoent ratio: {Idemp_ratio}; Index of Idempotent cells: {idempotent_cell_idx}".format(
            Idemp_ratio=Idempotent_ratio, idempotent_cell_idx=idempotent_cell_idx))

    def check_reproductibity_of_cells(self):
        self.load_nb()
        # Extract original outputs
        original_outputs = self.extract_outputs_based_on_OEO(self.nb.cells)

        # Extract executed outputs
        self.set_ep_as_OEO_mode()
        self.execute_nb()
        executed_outputs = []
        for cell in self.nb.cells:
            if len(cell.outputs) > 0:
                executed_outputs.append(cell.outputs[0].text)
            else:
                executed_outputs.append('')

        # Compare two outputs
        reproductive_cell_idx = []
        num_of_reproductive_cells = 0
        num_of_cells = len(original_outputs)
        for i in range(num_of_cells):
            if original_outputs[i] == executed_outputs[i]:
                num_of_reproductive_cells += 1
                reproductive_cell_idx.append(i)

        # Return (print) the results
        print("{num_of_reproductive_cells} / {num_of_cells} are reproductive, which is {reproductivity_ratio} %".format(
            num_of_reproductive_cells=num_of_reproductive_cells, num_of_cells=num_of_cells, reproductivity_ratio=(num_of_reproductive_cells/num_of_cells)))

        '''
        Also record some observations/findings about check_reproductivity
        1. If a cell is without outputs, should we ignore this cell for checking reproductivity or judge this cell as 'reproductive'?
           Ans: Both approaches seems to be feasiable. My opinion is to mark as reproductive. 
        2. another issue?
        '''

    def extract_outputs_based_on_OEO(self, cells):
        original_outputs = []
        cells = cells.copy()
        execution_count_lst = [cell.execution_count for cell in cells]
        OEO = sorted(range(len(execution_count_lst)),
                     key=lambda k: execution_count_lst[k])
        parsed_nb_cells = [cells[idx] for idx in OEO]
        for cell in parsed_nb_cells:
            if len(cell.outputs) > 0:
                original_outputs.append(cell.outputs[0].text)
            else:
                original_outputs.append('')

        return original_outputs

    def extract_meta_info(self):
        self.load_nb()
        return self.nb.metadata

