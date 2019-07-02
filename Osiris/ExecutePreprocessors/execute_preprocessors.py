from __future__ import absolute_import
from nbconvert.preprocessors import ExecutePreprocessor


'''
Customized ExecutePreprocessor 1, Truncate mode
- A user needs to specify the start_index and end_index
- Truncate mode acts like substring in string class 
'''
class TruncateExecutePreprocessor(ExecutePreprocessor):

    def __init__(self, start_index, end_index):
        super(ExecutePreprocessor, self).__init__()
        self.start_index = start_index
        self.end_index = end_index

    def preprocess(self, nb, resources):
        nb.cells = nb.cells[self.start_index:self.end_index]
        return super(TruncateExecutePreprocessor, self).preprocess(nb, resources)


'''
Customized ExecutePreprocessor 2, Skip mode
- A user needs to specify the cell indexes should be omitted
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
        return super(SkipExecutePreprocessor, self).preprocess(nb, resources)


'''
Customized ExecutePreprocessor 3, Link mode
- A user needs to specify the order (index) of cells should be executed
'''
class LinkExecutePreprocessor(ExecutePreprocessor):

    def __init__(self, link_idx_list):
        super(ExecutePreprocessor, self).__init__()
        self.link_idx_list = link_idx_list

    def preprocess(self, nb, resources):
        copy_nb_cells = nb.cells
        parsed_nb_cells = [copy_nb_cells[idx] for idx in self.link_idx_list]
        nb.cells = parsed_nb_cells
        return super(LinkExecutePreprocessor, self).preprocess(nb, resources)


'''
Customized ExecutePreprocessor 4, OEC (Original Execution Count) mode
- This mode is used under the assumption that the target Jupyter Notebook has been executed
- The Jupyter Notebook file will be executed according to ascending execution_count order
'''
class OECPreprocessor(ExecutePreprocessor):

    def __init__(self):
        super(ExecutePreprocessor, self).__init__()

    def preprocess(self, nb, resources):
        copy_nb_cells = nb.cells

        execution_count_lst = [cell.execution_count for cell in copy_nb_cells]
        OEO = sorted(range(len(execution_count_lst)),
                     key=lambda k: execution_count_lst[k])
        parsed_nb_cells = [copy_nb_cells[idx] for idx in OEO]

        parsed_nb_cells[0].source = "import warnings\nwarnings.filterwarnings('ignore')\n" + parsed_nb_cells[0].source

        nb.cells = parsed_nb_cells
        return super(OECPreprocessor, self).preprocess(nb, resources)


class DependencyPreprocessor(ExecutePreprocessor):
    def __init__(self, execution_order):
        super(ExecutePreprocessor, self).__init__()
        self._execution_order = execution_order

    def preprocess(self, nb, resources):
        copy_nb_cells = nb.cells

        parsed_nb_cells = [copy_nb_cells[idx] for idx in self._execution_order]
        parsed_nb_cells[0].source = "import warnings\nwarnings.filterwarnings('ignore')\n" + parsed_nb_cells[0].source

        nb.cells = parsed_nb_cells
        return super(DependencyPreprocessor, self).preprocess(nb, resources)


'''
ReproducibilityCheckPreprocessor is used to check whether cells of a given notebook possess reproducible characteristic
'''
class ReproducibilityCheckPreprocessor(ExecutePreprocessor):

    def __init__(self, check_cell_idx, analyse_strategy, is_duplicate):
        super(ExecutePreprocessor, self).__init__()
        self.check_cell_idx = check_cell_idx
        self.analyse_strategy = analyse_strategy
        self.is_duplicate = is_duplicate
        self.execution_order = None

    def set_execution_order(self, execution_order):
        self.execution_order = execution_order

    def preprocess(self, nb, resources):
        copy_nb_cells = nb.cells

        # Adjust the order of cells for different analyse strategies 
        if self.analyse_strategy == 'normal':
            parsed_nb_cells = copy_nb_cells.copy()
        elif self.analyse_strategy == 'OEC':
            execution_count_lst = [cell.execution_count for cell in copy_nb_cells]
            OEO = sorted(range(len(execution_count_lst)),
                        key=lambda k: execution_count_lst[k])
            parsed_nb_cells = [copy_nb_cells[idx] for idx in OEO]
        else: # dependency 
            parsed_nb_cells = [copy_nb_cells[idx] for idx in self.execution_order]

        # Insert an function at the beginning of the notebook to inspect the status 
        extractVar_fun_str = "def extractVars():\n    variables_set = {}\n    tmp = globals().copy()\n    for k, v in tmp.items():\n        con_1 = not k.startswith('_')\n        con_2 = not k in ['In', 'Out', 'get_ipython', 'exit', 'quit']\n        con_3 = type(v) in [int, complex, bool, float, str, list, set, dict, tuple]\n        if con_1 and con_2 and con_3:\n            variables_set[k] = v\n    \n    return variables_set"
        var_extract_fun_cell = parsed_nb_cells[0].copy()

        var_extract_fun_cell.source = extractVar_fun_str
        parsed_nb_cells.insert(0, var_extract_fun_cell)

        # Modify source code of cells to monitor status of self-defined variables 
        if self.is_duplicate:
            copy_cell = parsed_nb_cells[self.check_cell_idx]
            copy_cell = copy_cell.copy()
            parsed_nb_cells.insert(self.check_cell_idx+1, copy_cell)
            parsed_nb_cells[self.check_cell_idx+1].source += "\nextractVars()"
            parsed_nb_cells[0].source = "import warnings\nwarnings.filterwarnings('ignore')\n" + parsed_nb_cells[0].source
            nb.cells = parsed_nb_cells[:self.check_cell_idx+2]
        else:
            parsed_nb_cells[self.check_cell_idx].source += "\nextractVars()"
            parsed_nb_cells[0].source = "import warnings\nwarnings.filterwarnings('ignore')\n" + parsed_nb_cells[0].source
            nb.cells = parsed_nb_cells[:self.check_cell_idx+1]

        return super(ReproducibilityCheckPreprocessor, self).preprocess(nb, resources)


'''
StatusInspectionPreprocessor is used for evalutate status difference line by line for a cell of given notebook 
'''
class StatusInspectionPreprocessor(ExecutePreprocessor):
    
    def __init__(self, analyse_strategy, check_cell_idx):
        super(ExecutePreprocessor, self).__init__()
        self.check_cell_idx = check_cell_idx
        self.analyse_strategy = analyse_strategy
        self.execution_order = None

    def set_execution_order(self, execution_order):
        self.execution_order = execution_order

    def get_number_of_statements(self, nb):
        copy_nb_cells = nb.cells

        # Adjust the order of cells for different analyse strategies
        if self.analyse_strategy == 'normal':
            parsed_nb_cells = copy_nb_cells.copy()
        elif self.analyse_strategy == 'OEC':
            execution_count_lst = [
                cell.execution_count for cell in copy_nb_cells]
            OEO = sorted(range(len(execution_count_lst)),
                         key=lambda k: execution_count_lst[k])
            parsed_nb_cells = [copy_nb_cells[idx] for idx in OEO]
        else:  # dependency
            parsed_nb_cells = [copy_nb_cells[idx] for idx in self.execution_order]

        # Insert an function at the beginning of the notebook to inspect the status
        extractVar_fun_str = "def extractVars():\n    variables_set = {}\n    tmp = globals().copy()\n    for k, v in tmp.items():\n        con_1 = not k.startswith('_')\n        con_2 = not k in ['In', 'Out', 'get_ipython', 'exit', 'quit']\n        con_3 = type(v) in [int, complex, bool, float, str, list, set, dict, tuple]\n        if con_1 and con_2 and con_3:\n            variables_set[k] = v\n    \n    return variables_set"
        var_extract_fun_cell = parsed_nb_cells[0].copy()

        var_extract_fun_cell.source = extractVar_fun_str
        parsed_nb_cells.insert(0, var_extract_fun_cell)

        # Modify source code of cells to monitor status of self-defined variables line by line
        copy_cell = parsed_nb_cells[self.check_cell_idx]
        copy_cell = copy_cell.copy()
        statements = (copy_cell.source).split('\n')

        return len(statements)

    def preprocess_for_inspecting_status_of_certain_line(self, nb, resources, target_line_index):
        copy_nb_cells = nb.cells

        # Adjust the order of cells for different analyse strategies 
        if self.analyse_strategy == 'normal':
            parsed_nb_cells = copy_nb_cells.copy()
        elif self.analyse_strategy == 'OEC':
            execution_count_lst = [cell.execution_count for cell in copy_nb_cells]
            OEO = sorted(range(len(execution_count_lst)),
                        key=lambda k: execution_count_lst[k])
            parsed_nb_cells = [copy_nb_cells[idx] for idx in OEO]
        else: # dependency 
            parsed_nb_cells = [copy_nb_cells[idx]
                               for idx in self.execution_order]


        # Insert an function at the beginning of the notebook to inspect the status 
        extractVar_fun_str = "def extractVars():\n    variables_set = {}\n    tmp = globals().copy()\n    for k, v in tmp.items():\n        con_1 = not k.startswith('_')\n        con_2 = not k in ['In', 'Out', 'get_ipython', 'exit', 'quit']\n        con_3 = type(v) in [int, complex, bool, float, str, list, set, dict, tuple]\n        if con_1 and con_2 and con_3:\n            variables_set[k] = v\n    \n    return variables_set"
        var_extract_fun_cell = parsed_nb_cells[0].copy()

        var_extract_fun_cell.source = extractVar_fun_str
        parsed_nb_cells.insert(0, var_extract_fun_cell)

        # Modify source code of cells to monitor status of self-defined variables line by line 
        copy_cell = parsed_nb_cells[self.check_cell_idx]
        copy_cell = copy_cell.copy()
        statements = (copy_cell.source).split('\n')

        # CASE 1: Check for status difference before executing this cell 
        if target_line_index == -1: 
            new_source_code_for_the_cell = []
            new_source_code_for_the_cell.append("extractVars()")

        # CASE 2: Check for status difference until certain statement 
        else:
            new_source_code_for_the_cell = [] 
            for line_index, statement in enumerate(statements):
                new_source_code_for_the_cell.append(statement)
                if line_index == target_line_index:
                    num_of_leading_spaces = len(statement) - len(statement.lstrip())
                    num_of_extract_vars_func = len("extractVars()")
                    new_source_code_for_the_cell.append("extractVars()".rjust(num_of_leading_spaces+num_of_extract_vars_func))
                    break

        new_source_code = '\n'.join(new_source_code_for_the_cell)

        parsed_nb_cells[self.check_cell_idx].source = new_source_code
        parsed_nb_cells[0].source = "import warnings\nwarnings.filterwarnings('ignore')\n" + parsed_nb_cells[0].source
        nb.cells = parsed_nb_cells[:self.check_cell_idx+1]
        return super(StatusInspectionPreprocessor, self).preprocess(nb, resources)

