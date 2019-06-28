import csv, argparse, sys
from threading import Thread

sys.path.append('/home/dabao/Osiris')
import Osiris

def massive_notebooks_analyze(start_idx, end_idx, analyze_mode):
    csv_file = open('downloaded_notebooks.csv', 'r', encoding='utf-8')
    reader = csv.reader(csv_file) 

    for row_idx, row in enumerate(reader):
        nb_idx = row_idx + 1
        if nb_idx >= start_idx and nb_idx <= end_idx:
            original_repo_path, notebook_path = row[0], row[1]
            original_repo_path_lst = original_repo_path.split('/')
            folder_path = original_repo_path_lst[0]+'@'+original_repo_path_lst[1]

            path = '/mnt/fit-Knowledgezoo/jupyternotebooks/'+folder_path+'/'+notebook_path
            
            print(nb_idx, path)
            try:
                interface = Osiris.UserInterface(path)
                interface.analyse(verbose=True, store=True, analyze_mode=analyze_mode)
            except Exception as e:
                print(e)

parser = argparse.ArgumentParser(
    description='analysize Jupyter Notebook files')
parser.add_argument('--start-index', type=int, required=True)
parser.add_argument('--end-index', type=int, required=True)
parser.add_argument('-m', '--analyze-mode', type=str, default='OEC')
args = parser.parse_args()

massive_notebooks_analyze(args.start_index, args.end_index, args.analyze_mode)


# Multithread
'''
num_of_notebooks_per_thread = 10
num_of_threads = 5
assert int(num_of_notebooks_per_thread*num_of_threads) == 50

threads = [Thread(target=auto_analysize, args=(int(i*num_of_notebooks_per_thread+1), int(i*num_of_notebooks_per_thread+10))) for i in range(num_of_threads)]

for i, t in enumerate(threads):
    time.sleep(1)
    print(i, 'th thread begins')
    t.start()

for t in threads:
    t.join()

print('main thread exits')
'''
