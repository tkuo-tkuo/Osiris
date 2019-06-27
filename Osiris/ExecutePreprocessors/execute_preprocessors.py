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


'''
IdempotentCheckPreprocessor is used to check whether cells of a given notebook possess idempotent characteristic
-  Follow OEO execution path 
-  Insert variables extraction functions at the beginning of the noteook
'''
class IdempotentCheckPreprocessor(ExecutePreprocessor):

    def __init__(self, check_cell_idx, is_duplicate, py_version=3):
        super(ExecutePreprocessor, self).__init__()
        self.check_cell_idx = check_cell_idx
        self.is_duplicate = is_duplicate
        self.py_version = py_version

    def preprocess(self, nb, resources):
        copy_nb_cells = nb.cells

        # Requirement 1
        execution_count_lst = [cell.execution_count for cell in copy_nb_cells]
        OEO = sorted(range(len(execution_count_lst)),
                     key=lambda k: execution_count_lst[k])
        parsed_nb_cells = [copy_nb_cells[idx] for idx in OEO]

        # Requirement 2
        if self.py_version == 2:
            extractVar_fun_str = "def extractVars():\n    variables_set = {}\n    tmp = globals()[:]\n    for k, v in tmp.items():\n        con_1 = not k.startswith('_')\n        con_2 = not k in ['In', 'Out', 'get_ipython', 'exit', 'quit']\n        con_3 = type(v) in [int, complex, bool, float, str, list, set, dict, tuple]\n        if con_1 and con_2 and con_3:\n            variables_set[k] = v\n    \n    return variables_set"
            var_extract_fun_cell = parsed_nb_cells[0][:]
        else:
            extractVar_fun_str = "def extractVars():\n    variables_set = {}\n    tmp = globals().copy()\n    for k, v in tmp.items():\n        con_1 = not k.startswith('_')\n        con_2 = not k in ['In', 'Out', 'get_ipython', 'exit', 'quit']\n        con_3 = type(v) in [int, complex, bool, float, str, list, set, dict, tuple]\n        if con_1 and con_2 and con_3:\n            variables_set[k] = v\n    \n    return variables_set"
            var_extract_fun_cell = parsed_nb_cells[0].copy()

        var_extract_fun_cell.source = extractVar_fun_str
        parsed_nb_cells.insert(0, var_extract_fun_cell)

        if self.is_duplicate:
            if self.py_version == 2:
                copy_cell = parsed_nb_cells[self.check_cell_idx]
                copy_cell = copy_cell[:]
            else:
                copy_cell = parsed_nb_cells[self.check_cell_idx]
                copy_cell = copy_cell.copy()

            parsed_nb_cells.insert(self.check_cell_idx+1, copy_cell)
            parsed_nb_cells[self.check_cell_idx+1].source += "\nextractVars()"
        else:
            parsed_nb_cells[self.check_cell_idx].source += "\nextractVars()"

        nb.cells = parsed_nb_cells
        return super(IdempotentCheckPreprocessor, self).preprocess(nb, resources)
