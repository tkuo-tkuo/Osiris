import argparse
from Osiris.utils import get_path_by_extension

parser = argparse.ArgumentParser(description='return python version of a notebook')
parser.add_argument('-n', '--num-of-required-paths', type=int, required=True)
args = parser.parse_args()

root_path = '/mnt/fit-Knowledgezoo/Github_repos_download/data/'
num_of_required_paths = args.num_of_required_paths

paths = get_path_by_extension(root_path, num_of_required_paths)
result_str = ''
for idx, path in enumerate(paths):
    if idx is not 0:
        result_str+=','
    result_str+=path

print(result_str)



