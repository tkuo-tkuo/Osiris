import argparse
import sys

# Adjust the file in this sys.path 
# sys.path.append('C:\\Users\\User\\Desktop\\Osiris')

from Osiris.analysizer import Analysizer

parser = argparse.ArgumentParser()
parser.add_argument('-n', '--notebook_name', type=str, required=True)
args = parser.parse_args()

with open(args.notebook_name, 'r', encoding='utf-8') as f:
    analysizer = Analysizer(f)
    analysizer.check_executability()
    analysizer.check_reproductivity()
    analysizer.check_idempotent()
f.close()
