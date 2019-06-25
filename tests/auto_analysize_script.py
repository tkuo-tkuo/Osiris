import argparse
import sys

# Adjust the file in this sys.path 
sys.path.append('C:\\Users\\User\\Desktop\\Osiris')

from Osiris.analysizer import Analysizer

parser = argparse.ArgumentParser()
parser.add_argument('-n', '--notebook_name', type=str, required=True)
parser.add_argument('-v', '--verbose', action='store_false', default=True)
args = parser.parse_args()

with open(args.notebook_name, 'r', encoding='utf-8') as f:
    analysizer = Analysizer(f)
    analysizer.check_executability(args.verbose)
    analysizer.check_reproductivity(args.verbose)
    analysizer.check_idempotent(args.verbose)
f.close()
