import csv

def massive_notebooks_analyze(target_nb_idx):
    target_nb_idx = int(target_nb_idx)
    csv_file = open('../tests/downloaded_notebooks.csv', 'r', encoding='utf-8')
    reader = csv.reader(csv_file) 

    path = ''
    for row_idx, row in enumerate(reader):
        nb_idx = row_idx + 1
        if nb_idx == target_nb_idx:
            original_repo_path, notebook_path = row[0], row[1]
            original_repo_path_lst = original_repo_path.split('/')
            folder_path = original_repo_path_lst[0]+'@'+original_repo_path_lst[1]

            path = '/mnt/fit-Knowledgezoo/jupyternotebooks/'+folder_path+'/'+notebook_path
            return path 

# Prepare a csv for writing results 
with open('results.csv', 'w') as writeFile:
    writer = csv.writer(writeFile)

    file_str = 'a.txt'

    f = open(file_str, "r")
    for name in f:
        # get nb_idx 
        nb_idx = name.strip()
        target_result_file_name = nb_idx + '.txt'

        # get path according to the given nb_idx
        path = massive_notebooks_analyze(nb_idx)

        # get content according to the given nb_idx
        tf = open(target_result_file_name, 'r')
        content = tf.read()

        # write to a csv file 
        row = [nb_idx, path, content]
        writer.writerow(row)

writeFile.close()
