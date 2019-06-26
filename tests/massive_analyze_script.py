import Osiris
import csv, time, argparse, sys
from threading import Thread

num_of_notebooks_per_thread = 10
num_of_threads = 5
assert int(num_of_notebooks_per_thread*num_of_threads) == 50

def auto_analysize(start_idx, end_idx):
    csv_file = open('nbs/downloaded_notebooks.csv', 'r', encoding='utf-8')
    reader = csv.reader(csv_file)

    for row_idx, row in enumerate(reader):
        idx = row_idx + 1
        if idx >= start_idx and idx <= end_idx:
            original_repo, notebook_path = row[0], row[1]
            original_repo_lst = original_repo.split('/')
            folder_path = original_repo_lst[0]+'@'+original_repo_lst[1]
            path = 'nbs/'+folder_path+'/'+notebook_path

            print(idx, path)
            try:
                interface = Osiris.UserInterface(path)
                interface.analyse()
            except Exception as e:
                print(e)
                pass 

threads = [Thread(target=auto_analysize, args=(int(i*num_of_notebooks_per_thread+1), int(i*num_of_notebooks_per_thread+10))) for i in range(num_of_threads)]

parser = argparse.ArgumentParser(
    description='analysize Jupyter Notebook files')
parser.add_argument('--start-index', type=int, required=True)
parser.add_argument('--end-index', type=int, required=True)
args = parser.parse_args()

auto_analysize(args.start_index, args.end_index)

# Multithread
'''
for i, t in enumerate(threads):
    time.sleep(1)
    print(i, 'th thread begins')
    t.start()

for t in threads:
    t.join()

print('main thread exits')
'''
