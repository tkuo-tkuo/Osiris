import nbformat
import copy
from nbconvert.preprocessors import ExecutePreprocessor
from .ExecutePreprocessors import OECPreprocessor, IdempotentCheckPreprocessor

from .utils import *

class Analysizer():

    def __init__(self, notebook_file):
        self._nb = nbformat.read(notebook_file, as_version=4)

        # ep is abbr for execute_preprocessor, which will be set later corresponding to different analyses
        self._ep = None
        self._py_version = None
        self._is_py_2 = None
        self._is_executable = None

        self._preceding_preapre()

        # copy.deepcopy() must be executed at the end of __init__
        # since we would like to store the deep_copy version of the given notebook after parsing and clearning
        self._deep_copy_nb = copy.deepcopy(self._nb)

    def _preceding_preapre(self):
        # extract python version & whether the version is python 2 or not 
        self._py_version, self._is_py_2 = self._extract_py_version()

        # evaluate the name of kernel -> avoid the usage of inappropriate kernels like 'Python [Root]' or 'conda-root-py'
        kernal_name = self._nb['metadata']['kernelspec']['name']
        if kernal_name not in ['python2', 'python3']:
            self._nb['metadata']['kernelspec']['name'] = 'python3'

        # clean redundant (unexecuted/markdown/raw) cells
        self._clean_redundant_cells()

    def _extract_py_version(self):
        meta_info = self._nb.metadata
        py_version_lst = meta_info['language_info']['version'].split('.')
        py_version = py_version_lst[0]+'.'+py_version_lst[1]

        # this assert may be replaced by some error-handling
        assert py_version in ['2.7', '3.4', '3.5', '3.6', '3.7']

        is_py_2 = False
        if py_version[0] == '2':
            is_py_2 = True

        return py_version, is_py_2

    def _clean_redundant_cells(self):
        invalid_cells_idx = []
        for (idx, cell) in enumerate(self._nb.cells):
            if not (cell.cell_type == 'code'):
                invalid_cells_idx.append(idx)
                continue
            elif cell.execution_count == None:
                invalid_cells_idx.append(idx)
                continue
            else:
                pass
        parsed_nb_cells = [item for (idx, item) in enumerate(
            self._nb.cells) if idx not in invalid_cells_idx]

        self._nb.cells = parsed_nb_cells

    def _set_ep_as_normal_mode(self):
        self._ep = ExecutePreprocessor()

    def _set_ep_as_OEC_mode(self):
        self._ep = OECPreprocessor()

    def _set_ep_check_idempotent_mode(self, check_cell_idx, is_duplicate):
        self._ep = IdempotentCheckPreprocessor(check_cell_idx, is_duplicate, self._py_version)

    def _execute_nb(self):
        self._ep.preprocess(self._nb, {'metadata': {'path': './'}})

    def _extract_dependency_graph(self):
        pass 

    def _extract_potential_execution_path_from_dependency_graph(self):
        pass 

    def return_py_version(self):
        return self._py_version

    def check_executability(self, verbose=True, analyze_strategy='OEC'):
        self._nb = copy.deepcopy(self._deep_copy_nb)
        is_executable = False
        try:
            if analyze_strategy == 'normal':
                self._set_ep_as_normal_mode()
            elif analyze_strategy == 'dependency':
                # PENDING
                pass 
            else:
                self._set_ep_as_OEC_mode()

            self._execute_nb()
            is_executable = True
        except Exception as e:
            print(e)
            pass

        if verbose:
            print('Executability'.ljust(40), ':', is_executable)

        self._is_executable = is_executable
        return is_executable

    def check_reproductivity(self, verbose, analyse_strategy, strong_match):
        original_outputs, executed_outputs = None, None
        if analyse_strategy == 'OEC':
            self.check_executability(verbose=False, analyze_strategy='OEC')
            if not self._is_executable:
                raise RuntimeError('This notebook is NOT executable')

            # Extract the original outputs 
            self._nb = copy.deepcopy(self._deep_copy_nb)
            if strong_match:
                original_outputs = extract_outputs_based_on_OEC_order(self._nb.cells)
            else: 
                self._set_ep_as_OEC_mode()
                self._execute_nb()
                original_outputs = extract_outputs_based_on_OEC_order(self._nb.cells)


            # Extract the executed outputs 
            self._nb = copy.deepcopy(self._deep_copy_nb)
            self._set_ep_as_OEC_mode()
            self._execute_nb()
            executed_outputs = extract_outputs_based_on_OEC_order(self._nb.cells)
        elif analyse_strategy == 'normal':
            self.check_executability(verbose=False, analyze_strategy='normal')
            if not self._is_executable:
                raise RuntimeError('This notebook is NOT executable')

            # Extract the original outputs
            self._nb = copy.deepcopy(self._deep_copy_nb)
            if strong_match:
                # extract outputs based on normal order -> implement this in utils (PENDING)
                original_outputs = extract_outputs_based_on_normal_order(self._nb.cells)
            else:
                self._set_ep_as_normal_mode()
                self._execute_nb()
                original_outputs = extract_outputs_based_on_normal_order(self._nb.cells)

            # Extract the executed outputs
            self._nb = copy.deepcopy(self._deep_copy_nb)
            self._set_ep_as_normal_mode()
            self._execute_nb()
            executed_outputs = extract_outputs_based_on_normal_order(self._nb.cells)
        elif analyse_strategy == 'dependency':
            pass 
        else:
            pass

        assert not (original_outputs is None)
        assert not (executed_outputs is None)
        assert len(original_outputs) == len(executed_outputs)

        # Compare two outputs
        reproductive_cell_idx = []
        non_reproductive_cell_idx = []
        non_reproductive_original_outputs = []
        non_reproductive_executed_outputs = []
        num_of_reproductive_cells, num_of_cells = 0, len(original_outputs)
        for i in range(num_of_cells):
            if original_outputs[i] == executed_outputs[i]:
                num_of_reproductive_cells += 1
                reproductive_cell_idx.append(i)
            else: 
                non_reproductive_cell_idx.append(i)
                non_reproductive_original_outputs.append(original_outputs[i])
                non_reproductive_executed_outputs.append(executed_outputs[i])

        # Return (print) the results
        reproductivity_ratio = 0
        if num_of_cells == 0:
            reproductivity_ratio = 1
        else:
            reproductivity_ratio = num_of_reproductive_cells/num_of_cells
        source_code_of_non_reproductive_cells = extract_source_code_from_non_reproductive_cells(self._nb.cells, non_reproductive_cell_idx)

        if verbose:
            print('Reproductivity'.ljust(40), ':', "number of reproductive cells: {num_of_reproductive_cells} ; number of cells: {num_of_cells}".format(
                num_of_reproductive_cells=num_of_reproductive_cells, num_of_cells=num_of_cells))
            print('Reproductivity'.ljust(40), ':', "reproductive ratio: {reproductivity_ratio} ; index of reproductive cells: {reproductive_cell_idx}".format(
                reproductivity_ratio=round(reproductivity_ratio, 3), reproductive_cell_idx=reproductive_cell_idx))

            # Debug & Experiment purpose 
            # Print cells which are non reproductive 
            
            self._nb = copy.deepcopy(self._deep_copy_nb)
            print_source_code_of_non_reproductive_cells(self._nb.cells, non_reproductive_cell_idx, non_reproductive_original_outputs, non_reproductive_executed_outputs)   
             

        return num_of_reproductive_cells, num_of_cells, reproductivity_ratio, reproductive_cell_idx, source_code_of_non_reproductive_cells          

    def check_idempotent_line_by_line(self):
        pass 

    def check_idempotent(self, verbose=True):
        self.check_executability(verbose=False)
        if not self._is_executable:
            raise RuntimeError('This notebook is NOT executable')

        self._nb = copy.deepcopy(self._deep_copy_nb)
        num_of_cells = len(self._nb.cells)

        copy_nb_lst = self._nb.cells.copy()

        idempotent_cell_idx = []
        for i in range(num_of_cells):
            check_cell_idx = i + 1

            # Get status variables if execute once
            is_duplicate = False
            if self._is_py_2:
                self._nb.cells = copy_nb_lst[:]
            else:
                self._nb.cells = copy_nb_lst.copy()

            self._nb = copy.deepcopy(self._deep_copy_nb)
            self._set_ep_check_idempotent_mode(check_cell_idx, is_duplicate)
            self._execute_nb()
            check_cell_outputs = self._nb.cells[check_cell_idx].outputs
            var_status = check_cell_outputs[-1].data['text/plain']
            var_status_exe_once = var_status

            # Get status variables if execute twice
            is_duplicate = True
            if self._is_py_2:
                self._nb.cells = copy_nb_lst[:]
            else:
                self._nb.cells = copy_nb_lst.copy()

            self._nb = copy.deepcopy(self._deep_copy_nb)
            self._set_ep_check_idempotent_mode(check_cell_idx, is_duplicate)
            self._execute_nb()
            check_cell_outputs = self._nb.cells[check_cell_idx+1].outputs
            var_status = check_cell_outputs[-1].data['text/plain']
            var_status_exe_twice = var_status

            # Check whether a cell is idempotent & Print
            idemp_result = (var_status_exe_once == var_status_exe_twice)
            if verbose:
                print("Check the {cell_idx} th cell among {num_of_cells} cells. Idempotent result: {Idemp_result}".format(
                    cell_idx=check_cell_idx, num_of_cells=num_of_cells, Idemp_result=idemp_result))

            # Store results for further return
            if idemp_result:
                idempotent_cell_idx.append(i)

        # Return
        num_of_idempotent_cells = len(idempotent_cell_idx)
        idempotent_ratio = len(idempotent_cell_idx) / num_of_cells
        if verbose:
            print('Idempotent'.ljust(40), ':', "number of idempotent cells: {num_of_idempotent_cells} ; number of cells: {num_of_cells}".format(
                num_of_idempotent_cells=num_of_idempotent_cells, num_of_cells=num_of_cells))
            print('Idempotent'.ljust(40), ':', "idempoent ratio: {Idemp_ratio} ; index of Idempotent cells: {idempotent_cell_idx}".format(
                Idemp_ratio=round(idempotent_ratio, 3), idempotent_cell_idx=idempotent_cell_idx))

        return num_of_idempotent_cells, num_of_cells, idempotent_ratio, idempotent_cell_idx


