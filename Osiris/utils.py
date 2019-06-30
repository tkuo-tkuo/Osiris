import nbformat

def store_nb(nb, relative_path):
    with open(relative_path, 'w') as f:
        nbformat.write(nb, f)

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

# PENDING
def extract_outputs_based_on_dependency_order(cells):
    pass 

def print_source_code_of_non_reproductive_cells(cells, index_lst, non_reproductive_original_outputs, non_reproductive_executed_outputs):
    cells = cells.copy()

    execution_count_lst = [cell.execution_count for cell in cells]
    OEC = sorted(range(len(execution_count_lst)), key=lambda k: execution_count_lst[k])
    parsed_nb_cells = [cells[idx] for idx in OEC]
    
    non_reproductive_cells = [cell for (idx, cell) in enumerate(parsed_nb_cells) if idx in index_lst]
    non_reproductive_cells = non_reproductive_cells.copy() # in case we would modify any content

    for (cell_idx, cell, original_output, executed_output) in zip(index_lst, non_reproductive_cells, non_reproductive_original_outputs, non_reproductive_executed_outputs):
        if 'source' in cell.keys():
            print('-------------------------------------------')
            print('Source Code of Non reproductive Cell', cell_idx)
            print('-------------------------------------------')
            print(cell['source'])

            print()
            print('-----------------')
            print('Original output:')
            print(original_output)
            print('Executed output:')
            print(executed_output)

def extract_source_code_from_non_reproductive_cells(cells, index_lst):
    cells = cells.copy()

    execution_count_lst = [cell.execution_count for cell in cells]
    OEC = sorted(range(len(execution_count_lst)),
                    key=lambda k: execution_count_lst[k])
    parsed_nb_cells = [cells[idx] for idx in OEC]

    non_reproductive_cells = [cell for (idx, cell) in enumerate(
        parsed_nb_cells) if idx in index_lst]
    # in case we would modify any content
    non_reproductive_cells = non_reproductive_cells.copy()
    source_code_of_non_reproductive_cells = [
        cell['source'] for cell in non_reproductive_cells]

    return source_code_of_non_reproductive_cells
