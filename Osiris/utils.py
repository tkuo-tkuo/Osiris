import os 

import nbformat
import collections
import numpy as np

from .dependency_graph import DependencyGraph
from .dependency_graph import get_code_list, detect, get_path_by_extension

'''
The following utils functions are high-level usage of Jarix's implementation
'''
def return_traverse_path(root_path, num_of_required_paths):
    return get_path_by_extension(root_path, num_of_required_paths)

def risk_detect(path):
    return detect(path)

def bfs(graph, root):
    visited, queue = set(), collections.deque([root])
    visited.add(root)
    path = []
    path.append(root)
    while queue:
        vertex = queue.popleft()
        for neighbour in graph[vertex]:
            if neighbour not in visited:
                visited.add(neighbour)
                path.append(neighbour)
                queue.append(neighbour)

    return path

def dep_matrix_to_dep_lst(matrix):
    graph = {}
    for i, node in enumerate(matrix):
        adj = []
        for j, connected in enumerate(node):
            if connected:
                adj.append(j)
        graph[i] = adj

    return graph

def get_dependency_matrix(path):
    code_list = get_code_list(path)
    dep_graph = DependencyGraph()
    dep_matrix = dep_graph.build(code_list)
    return dep_matrix

def get_execution_order(path):
    name_of_virtual_node_for_forest = 'forest_root'
    dep_matrix = get_dependency_matrix(path)
    adjacent_lst = dep_matrix_to_dep_lst(dep_matrix)
    dependency_lst = dep_matrix_to_dep_lst(np.transpose(dep_matrix))

    # Connect trees in forest with a virtual node called 'forest_root'
    key_for_root_of_tree = []
    for key in dependency_lst.keys():
        if dependency_lst[key] == []:
            key_for_root_of_tree.append(key)
    adjacent_lst[name_of_virtual_node_for_forest] = key_for_root_of_tree

    # Note that it's just one of the potential execution order generated according dependency between cells
    execution_order = bfs(adjacent_lst, name_of_virtual_node_for_forest)

    # Remove our virtual node, 'forest_root'
    execution_order.remove(name_of_virtual_node_for_forest)
    print('According to dependency of cells, the execution order is', execution_order)
    return execution_order

'''
This utils function, move_to_appropriate_location, aims to cope with relative path issue
'''
def move_to_appropriate_location(path):
    path_split_lst = path.split('/')
    # We need to cd to the same directory as the notebook
    if len(path_split_lst) > 1:
        cd_path_lst = path_split_lst[:-1]
        cd_path = '/'.join(cd_path_lst)
        os.chdir(cd_path)


'''
This utils function, store_nb, is just for debugging purpose
'''
def store_nb(nb, relative_path):
    with open(relative_path, 'w') as f:
        nbformat.write(nb, f)


'''
Following utils functions with 'extract_' as prefix aim to parse Jupyter Notebook files and extract useful information for further analyses 
'''
def extract_outputs_based_on_normal_order(cells):
    outputs = []
    for cell in cells:
        if len(cell.outputs) > 0:
            thorough_output_for_the_cell = ''
            for output in cell.outputs:
                if 'text' in output.keys():
                    thorough_output_for_the_cell += output.text
                elif 'data' in output.keys():
                    image_data = output.data
                    if 'image/png' in image_data.keys():
                        thorough_output_for_the_cell += image_data['image/png']
                    elif 'text/plain' in image_data.keys():
                        thorough_output_for_the_cell += image_data['text/plain']
                    else:
                        pass
            outputs.append(thorough_output_for_the_cell)
        else:
            outputs.append('')

    return outputs

def extract_outputs_based_on_OEC_order(cells):
    outputs = []
    cells = cells.copy()

    execution_count_lst = [cell.execution_count for cell in cells]
    OEC = sorted(range(len(execution_count_lst)),
                    key=lambda k: execution_count_lst[k])
    parsed_nb_cells = [cells[idx] for idx in OEC]
    for cell in parsed_nb_cells:
        if len(cell.outputs) > 0:
            thorough_output_for_the_cell = ''
            for output in cell.outputs:
                if 'text' in output.keys():
                    thorough_output_for_the_cell += output.text
                elif 'data' in output.keys():
                    image_data = output.data
                    if 'image/png' in image_data.keys():
                        thorough_output_for_the_cell += image_data['image/png']
                    elif 'text/plain' in image_data.keys():
                        thorough_output_for_the_cell += image_data['text/plain']
                    else:
                        pass
            outputs.append(thorough_output_for_the_cell)
        else:
            outputs.append('')

    return outputs

def extract_outputs_based_on_dependency_order(cells, execution_order):
    outputs = []
    cells = cells.copy()

    parsed_nb_cells = [cells[idx] for idx in execution_order]
    for cell in parsed_nb_cells:
        if len(cell.outputs) > 0:
            thorough_output_for_the_cell = ''
            for output in cell.outputs:
                if 'text' in output.keys():
                    thorough_output_for_the_cell += output.text
                elif 'data' in output.keys():
                    image_data = output.data
                    if 'image/png' in image_data.keys():
                        thorough_output_for_the_cell += image_data['image/png']
                    elif 'text/plain' in image_data.keys():
                        thorough_output_for_the_cell += image_data['text/plain']
                    else:
                        pass
            outputs.append(thorough_output_for_the_cell)
        else:
            outputs.append('')

    return outputs


def extract_source_code_from_unmatched_cells(cells, index_lst):
    cells = cells.copy()

    execution_count_lst = [cell.execution_count for cell in cells]
    OEC = sorted(range(len(execution_count_lst)),
                 key=lambda k: execution_count_lst[k])
    parsed_nb_cells = [cells[idx] for idx in OEC]

    unmatched_cells = [cell for (idx, cell) in enumerate(
        parsed_nb_cells) if idx in index_lst]
    unmatched_cells = unmatched_cells.copy()
    source_code_of_unmatched_cells = [
        cell['source'] for cell in unmatched_cells]

    return source_code_of_unmatched_cells


'''
All remaining utils functions below are for printing purpose 
'''
def print_source_code_of_unmatched_cells(cells, index_lst, unmatched_original_outputs, unmtached_executed_outputs):
    cells = cells.copy()

    execution_count_lst = [cell.execution_count for cell in cells]
    OEC = sorted(range(len(execution_count_lst)), key=lambda k: execution_count_lst[k])
    parsed_nb_cells = [cells[idx] for idx in OEC]
    
    unmatched_cells = [cell for (idx, cell) in enumerate(parsed_nb_cells) if idx in index_lst]
    unmatched_cells = unmatched_cells.copy() # in case we would modify any content

    for (cell_idx, cell, original_output, executed_output) in zip(index_lst, unmatched_cells, unmatched_original_outputs, unmtached_executed_outputs):
        if 'source' in cell.keys():
            print('-------------------------------------------')
            print('Source Code of a Unmatched Cell', cell_idx)
            print('-------------------------------------------')
            print(cell['source'])

            print()
            print('-----------------')
            print('Original output:')
            print(original_output)
            print('Executed output:')
            print(executed_output)


