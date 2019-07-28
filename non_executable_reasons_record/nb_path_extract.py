import csv, argparse, sys

def massive_notebooks_analyze(start_idx, end_idx):
    csv_file = open('tests/downloaded_notebooks.csv', 'r', encoding='utf-8')
    reader = csv.reader(csv_file) 

    path = ''
    for row_idx, row in enumerate(reader):
        nb_idx = row_idx + 1
        if nb_idx >= start_idx and nb_idx <= end_idx:
            original_repo_path, notebook_path = row[0], row[1]
            original_repo_path_lst = original_repo_path.split('/')
            folder_path = original_repo_path_lst[0]+'@'+original_repo_path_lst[1]
            '''
            if nb_idx is not 1:
                path += ','

            path += '/mnt/fit-Knowledgezoo/jupyternotebooks/'+folder_path+'/'+notebook_path
            '''

            path = '/mnt/fit-Knowledgezoo/jupyternotebooks/'+folder_path+'/'+notebook_path
            print(nb_idx, path)

    # print(path)

parser = argparse.ArgumentParser()
parser.add_argument('-n ', '--num-of-notebooks', type=int, required=True)
args = parser.parse_args()

massive_notebooks_analyze(1, args.num_of_notebooks)





