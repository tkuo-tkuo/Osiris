import argparse
import sys

sys.path.append('/home/dabao/Osiris')

from Osiris.analysizer import Analysizer

parser = argparse.ArgumentParser()
parser.add_argument('-n', '--notebook_name', type=str, required=True)
parser.add_argument('-v', '--verbose', action='store_false', default=True)
parser.add_argument('-s', '--store', action='store_true', default=False)
args = parser.parse_args()

# print('Boolean variable for storing results:', args.store)
# print('Boolean variable for verbose option:', args.verbose)

with open(args.notebook_name, 'r', encoding='utf-8') as f:
    analysizer = Analysizer(f)
    print(analysizer.check_executability(args.verbose))
    print(analysizer.check_reproductivity(args.verbose))
    # print(analysizer.check_idempotent(args.verbose))
f.close()
