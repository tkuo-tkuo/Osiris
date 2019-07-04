import nbformat
import copy
from nbconvert.preprocessors import ExecutePreprocessor
from .ExecutePreprocessors import OECPreprocessor, SelfReproducibilityCheckPreprocessor, StatusInspectionPreprocessor, DependencyPreprocessor

from .utils import *

class Analysizer():

    def __init__(self, notebook_path, notebook_file):
        self._nb_path = notebook_path.split('/')[-1]
        self._nb = nbformat.read(notebook_file, as_version=4)

        # ep is abbr for execute_preprocessor, which will be set later corresponding to different analyses
        self._ep = None
        self._py_version = None
        self._is_executable = None

        self._preceding_preapre()

        # copy.deepcopy() must be executed at the end of __init__
        # since we would like to store the deep_copy version of the given notebook after parsing and clearning
        self._deep_copy_nb = copy.deepcopy(self._nb)

    

    def _preceding_preapre(self):
        # extract python version & whether the version is python 2 or not 
        self._py_version = self._extract_py_version()

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
        assert py_version in ['3.5', '3.6', '3.7']

        return py_version

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

    def _set_ep_as_dependency_mode(self, execution_order):
        self._ep = DependencyPreprocessor(execution_order)

    def _set_ep_check_self_reproducibility_mode(self, check_cell_idx, analyse_strategy, is_duplicate):
        self._ep = SelfReproducibilityCheckPreprocessor(check_cell_idx, analyse_strategy, is_duplicate)

    def _set_execution_order_for_ep_check_self_reproducibility_mode(self, execution_order):
        self._ep.set_execution_order(execution_order)

    def _set_ep_status_inspection_mode(self, analyse_strategy, check_cell_idx):
        self._ep = StatusInspectionPreprocessor(analyse_strategy, check_cell_idx)

    def _set_execution_order_for_ep_status_inspection_mode(self, execution_order):
        self._ep.set_execution_order(execution_order)

    def _execute_nb(self):
        self._ep.preprocess(self._nb, {'metadata': {'path': './'}})

    def _extract_dependency_graph(self):
        pass 

    def _extract_potential_execution_path_from_dependency_graph(self):
        pass 

    def return_py_version(self):
        return self._py_version

    def check_executability(self, verbose, analyse_strategy):
        self._nb = copy.deepcopy(self._deep_copy_nb)
        is_executable = False
        try:
            if analyse_strategy == 'normal':
                self._set_ep_as_normal_mode()
            elif analyse_strategy == 'dependency':
                execution_order = get_execution_order(self._nb_path)
                self._set_ep_as_dependency_mode(execution_order)
            else:
                self._set_ep_as_OEC_mode()

            self._execute_nb()
            is_executable = True
        except Exception as e:
            print(e)
            pass

        print('Executability'.ljust(40), ':', is_executable)

        self._is_executable = is_executable
        return is_executable

    def check_reproducibility(self, verbose, analyse_strategy, match_pattern):
        original_outputs, executed_outputs = None, None

        # Extract two outputs according to aanalyse_strategy and strong/weak match 
        if analyse_strategy == 'OEC':

            # Extract the original outputs 
            self._nb = copy.deepcopy(self._deep_copy_nb)
            if match_pattern == 'strong':
                original_outputs = extract_outputs_based_on_OEC_order(self._nb.cells)
            elif match_pattern == 'weak': 
                self._set_ep_as_OEC_mode()
                self._execute_nb()
                original_outputs = extract_outputs_based_on_OEC_order(self._nb.cells)
            else: # best-effort (PENDING)
                pass 

            # Extract the executed outputs 
            self._nb = copy.deepcopy(self._deep_copy_nb)
            self._set_ep_as_OEC_mode()
            self._execute_nb()
            executed_outputs = extract_outputs_based_on_OEC_order(self._nb.cells)
        elif analyse_strategy == 'normal':

            # Extract the original outputs
            self._nb = copy.deepcopy(self._deep_copy_nb)
            if match_pattern == 'strong':
                original_outputs = extract_outputs_based_on_normal_order(self._nb.cells)
            elif match_pattern == 'weak':
                self._set_ep_as_normal_mode()
                self._execute_nb()
                original_outputs = extract_outputs_based_on_normal_order(self._nb.cells)
            else: # best-effort (PENDING)
                pass 

            # Extract the executed outputs
            self._nb = copy.deepcopy(self._deep_copy_nb)
            self._set_ep_as_normal_mode()
            self._execute_nb()
            executed_outputs = extract_outputs_based_on_normal_order(self._nb.cells)
        elif analyse_strategy == 'dependency':

            execution_order = get_execution_order(self._nb_path)
            # Extract the original outputs
            self._nb = copy.deepcopy(self._deep_copy_nb)
            if match_pattern == 'strong':
                original_outputs = extract_outputs_based_on_dependency_order(self._nb.cells, execution_order)
            elif match_pattern == 'weak':
                self._set_ep_as_dependency_mode(execution_order)
                self._execute_nb()
                original_outputs = extract_outputs_based_on_normal_order(self._nb.cells)
            else:  # best-effort (PENDING)
                pass

            # Extract the executed outputs
            self._nb = copy.deepcopy(self._deep_copy_nb)
            self._set_ep_as_dependency_mode(execution_order)
            self._execute_nb()
            executed_outputs = extract_outputs_based_on_normal_order(self._nb.cells)
        else:
            pass

        assert not (original_outputs is None)
        assert not (executed_outputs is None)
        assert len(original_outputs) == len(executed_outputs)

        # Compare two outputs
        matched_cell_idx = []
        unmatched_cell_idx = []
        unmatched_original_outputs = []
        unmatched_executed_outputs = []
        num_of_matched_cells, num_of_cells = 0, len(original_outputs)
        for i in range(num_of_cells):
            if original_outputs[i] == executed_outputs[i]:
                num_of_matched_cells += 1
                matched_cell_idx.append(i)
            else: 
                unmatched_cell_idx.append(i)
                unmatched_original_outputs.append(original_outputs[i])
                unmatched_executed_outputs.append(executed_outputs[i])

        # Return (print) the results
        match_ratio = 0
        if num_of_cells == 0:
            match_ratio = 1
        else:
            match_ratio = num_of_matched_cells/num_of_cells
        source_code_of_unmatched_cells = extract_source_code_from_unmatched_cells(self._nb.cells, unmatched_cell_idx)

        print('Reproducibility'.ljust(40), ':', "number of matched cells: {num_of_matched_cells} ; number of cells: {num_of_cells}".format(
            num_of_matched_cells=num_of_matched_cells, num_of_cells=num_of_cells))
        print('Reproducibility'.ljust(40), ':', "matched ratio: {match_ratio} ; index of matched cells: {matched_cell_idx}".format(
            match_ratio=round(match_ratio, 3), matched_cell_idx=matched_cell_idx))

        # Debug & Experiment purpose 
        # Print cells which are unmatched 
        if verbose:
            self._nb = copy.deepcopy(self._deep_copy_nb)
            print_source_code_of_unmatched_cells(self._nb.cells, unmatched_cell_idx, unmatched_original_outputs, unmatched_executed_outputs)   

        return num_of_matched_cells, num_of_cells, match_ratio, matched_cell_idx, source_code_of_unmatched_cells          

    def check_self_reproducibility(self, verbose, analyse_strategy):

        execution_order = None
        if analyse_strategy == 'dependency':
            execution_order = get_execution_order(self._nb_path)
        
        self._nb = copy.deepcopy(self._deep_copy_nb)
        num_of_cells = len(self._nb.cells)

        self_reproducible_cell_idx = []
        for i in range(num_of_cells):
            # +1 cuz we will insert a status inspection function as the first cell (with index 0)
            check_cell_idx = i + 1 

            # Get status variables if execute once
            is_duplicate = False
            self._nb = copy.deepcopy(self._deep_copy_nb)
            self._set_ep_check_self_reproducibility_mode(check_cell_idx, analyse_strategy, is_duplicate)
            if execution_order is not None:
                self._set_execution_order_for_ep_check_self_reproducibility_mode(execution_order)
            self._execute_nb()
            check_cell_outputs = self._nb.cells[check_cell_idx].outputs
            var_status_exe_once = check_cell_outputs[-1].data['text/plain']

            # Get status variables if execute twice
            self._nb = copy.deepcopy(self._deep_copy_nb)
            is_duplicate = True
            self._set_ep_check_self_reproducibility_mode(check_cell_idx, analyse_strategy, is_duplicate)
            if execution_order is not None:
                self._set_execution_order_for_ep_check_self_reproducibility_mode(execution_order)
            self._execute_nb()
            check_cell_outputs = self._nb.cells[check_cell_idx+1].outputs
            var_status_exe_twice = check_cell_outputs[-1].data['text/plain']

            # Check whether a cell is reproducible & Print
            is_self_reproducible = (var_status_exe_once == var_status_exe_twice)
            if verbose:
                print("Check the {cell_idx} th cell among {num_of_cells} cells. Self-reproducibility result: {Self_reproduciblity_result}".format(
                    cell_idx=check_cell_idx, num_of_cells=num_of_cells, Self_reproduciblity_result=is_self_reproducible))

            # Store results for further return
            if is_self_reproducible:
                self_reproducible_cell_idx.append(i)

        # Return
        num_of_self_reproducible_cells = len(self_reproducible_cell_idx)
        self_reproducibility_ratio = len(self_reproducible_cell_idx) / num_of_cells

        print('Self reproducibility'.ljust(40), ':', "number of self-reproducible cells: {num_of_self_reproducible_cells} ; number of cells: {num_of_cells}".format(
            num_of_self_reproducible_cells=num_of_self_reproducible_cells, num_of_cells=num_of_cells))
        print('Self reproducibility'.ljust(40), ':', "self-reproduciblity ratio: {self_reproducibility_ratio} ; index of self-reproducible cells: {self_reproducible_cell_idx}".format(
            self_reproducibility_ratio=round(self_reproducibility_ratio, 3), self_reproducible_cell_idx=self_reproducible_cell_idx))

        return num_of_self_reproducible_cells, num_of_cells, self_reproducibility_ratio, self_reproducible_cell_idx

    def _ep_get_number_of_statements(self):
        return self._ep.get_number_of_statements(self._nb)

    def _execute_nb_for_inspecting_status_of_certain_line(self, target_line_index):
        self._ep.preprocess_for_inspecting_status_of_certain_line(
            self._nb, {'metadata': {'path': './'}}, target_line_index)

    def check_status_difference_for_a_cell(self, analyse_strategy, check_cell_idx):

        # +1 cuz we will insert a status inspection function as the first cell (with index 0)
        check_cell_idx += 1
        first_var_status, second_var_status = None, None

        execution_order = None
        if analyse_strategy == 'dependency':
            execution_order = get_execution_order(self._nb_path)

        self._nb = copy.deepcopy(self._deep_copy_nb)
        self._set_ep_status_inspection_mode(analyse_strategy, check_cell_idx)
        if execution_order is not None:
            self._set_execution_order_for_ep_status_inspection_mode(execution_order)
        num_of_statements = self._ep_get_number_of_statements()

        # Check if the status of self-defined variables has been different before this cell
        self._nb = copy.deepcopy(self._deep_copy_nb)
        self._set_ep_status_inspection_mode(analyse_strategy, check_cell_idx)
        if execution_order is not None:
            self._set_execution_order_for_ep_status_inspection_mode(execution_order)
        try:
            self._execute_nb_for_inspecting_status_of_certain_line(-1)
            check_cell_outputs = self._nb.cells[check_cell_idx].outputs
            first_var_status = check_cell_outputs[-1].data['text/plain']
        except:
            first_var_status = None
            
        self._nb = copy.deepcopy(self._deep_copy_nb)
        self._set_ep_status_inspection_mode(analyse_strategy, check_cell_idx)
        if execution_order is not None:
            self._set_execution_order_for_ep_status_inspection_mode(execution_order)
        try:
            self._execute_nb_for_inspecting_status_of_certain_line(-1)
            check_cell_outputs = self._nb.cells[check_cell_idx].outputs
            second_var_status = check_cell_outputs[-1].data['text/plain']
        except:
            second_var_status = None

        if not (first_var_status == second_var_status):
            return -1 

        # Check if the status of self-defined variables has been different upon certain statement
        for i in range(num_of_statements):
            self._nb = copy.deepcopy(self._deep_copy_nb)
            self._set_ep_status_inspection_mode(analyse_strategy, check_cell_idx)
            if execution_order is not None:
                self._set_execution_order_for_ep_status_inspection_mode(execution_order)
            try:
                self._execute_nb_for_inspecting_status_of_certain_line(i)
                check_cell_outputs = self._nb.cells[check_cell_idx].outputs
                first_var_status = check_cell_outputs[-1].data['text/plain']
            except:
                first_var_status = None

            self._nb = copy.deepcopy(self._deep_copy_nb)
            self._set_ep_status_inspection_mode(analyse_strategy, check_cell_idx)
            if execution_order is not None:
                self._set_execution_order_for_ep_status_inspection_mode(execution_order)
            try:
                self._execute_nb_for_inspecting_status_of_certain_line(i)
                check_cell_outputs = self._nb.cells[check_cell_idx].outputs
                second_var_status = check_cell_outputs[-1].data['text/plain']
            except:
                second_var_status = None

            if not (first_var_status == second_var_status):
                return i

        # What if the status of self-defined variables remains the same through execution of this cell
        # return None to indicate unfound 
        return None


