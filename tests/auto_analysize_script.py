import argparse
import sys, csv

sys.path.append('/home/dabao/Osiris')

from Osiris.analysizer import Analysizer

parser = argparse.ArgumentParser()
parser.add_argument('-n', '--notebook_name', type=str, required=True)
parser.add_argument('-v', '--verbose', action='store_false', default=True)
parser.add_argument('-s', '--store', action='store_true', default=False)
parser.add_argument('-t', '--top-to-down-execution', action='store_true', default=False)
args = parser.parse_args()

mode = 'OEC'
if args.top_to_down_execution:
    mode = 'normal'

# print('Boolean variable for storing results:', args.store)
# print('Boolean variable for verbose option:', args.verbose)

with open(args.notebook_name, 'r', encoding='utf-8') as f:
    analysizer = Analysizer(f)
    is_executable = analysizer.check_executability(args.verbose, mode)
    num_of_reproductive_cells, num_of_cells, reproductivity_ratio, reproductive_cell_idx, source_code_from_non_reproductive_cells = analysizer.check_reproductivity(args.verbose, mode)
    # print(analysizer.check_idempotent(args.verbose))

    if args.store:
        if mode == 'OEC':
            csv_path_for_storing_analyzed_results = '/home/dabao/Osiris/tests/analyzed_results_OEC.csv'
        else:
            csv_path_for_storing_analyzed_results = '/home/dabao/Osiris/tests/analyzed_results_normal.csv'
        
        csv_file_for_storing_analyzed_results = open(csv_path_for_storing_analyzed_results, 'a')
        writer_for_storing_analyzed_results = csv.writer(csv_file_for_storing_analyzed_results)
    
        if mode == 'OEC':
            csv_path_for_storing_source_code_of_non_reproductive_cells = '/home/dabao/Osiris/tests/source_code_of_non_reproductive_cells_OEC.csv'
            csv_file_for_storing_source_code_of_non_reproductive_cells = open(csv_path_for_storing_source_code_of_non_reproductive_cells, 'a') 
            writer_for_storing_source_code_of_non_reproductive_cells = csv.writer(csv_file_for_storing_source_code_of_non_reproductive_cells)

        row = []
        row.append(is_executable)
        row.append(num_of_reproductive_cells)
        row.append(num_of_cells)
        row.append(reproductivity_ratio)
        row.append(reproductive_cell_idx)
        # print('Results:', row)
        
        writer_for_storing_analyzed_results.writerow(row) 

        if mode == 'OEC':
            for source_code in source_code_from_non_reproductive_cells:
                writer_for_storing_source_code_of_non_reproductive_cells.writerow([source_code])   


f.close()
