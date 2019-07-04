import argparse
import sys, os

import Osiris

parser = argparse.ArgumentParser()
parser.add_argument('-n', '--notebook-name', type=str, required=True)
parser.add_argument('-e', '--execute', type=str, required=True)
parser.add_argument('-v', '--verbose', action='store_true', default=False)
parser.add_argument('-m', '--match-pattern', type=str, default=None)
parser.add_argument('-s', '--self-reproduce', action='store_true', default=False)
parser.add_argument('-d', '--debug', type=int, default=None)
args = parser.parse_args()

# Parameters (required)
path = args.notebook_name
execute = args.execute
assert execute in ['normal', 'OEC', 'dependency']

# Parameters (optional)
verbose = args.verbose
match_pattern = args.match_pattern
self_reproduce = args.self_reproduce
debug = args.debug
if match_pattern is not None:
    assert match_pattern in ['strong', 'weak', 'best_effort']


def analyse_nb(path, execute, verbose, match_pattern, self_reproduce, debug):
    interface = Osiris.UserInterface(path, verbose)
    is_executable = interface.analyse_executability(execute)

    if is_executable:
        # reproducibility 
        if match_pattern is not None:
            num_of_matched_cells, num_of_cells, match_ratio, matched_cell_idx, source_code_from_unmatched_cells = interface.analyse_reproducibility(
                execute, match_pattern)

        # self-reproducibility 
        if self_reproduce:
            num_of_reproducible_cells, num_of_cells, reproducible_ratio, reproducible_cell_idx = interface.analyse_self_reproducibility(
                execute)

        # debug 
        if debug is not None:
            problematic_statement_index = interface.analyse_status_difference_for_a_cell(
                execute, debug)

analyse_nb(path, execute, verbose, match_pattern, self_reproduce, debug)

