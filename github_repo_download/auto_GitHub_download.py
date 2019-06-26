import csv
import subprocess
import argparse

def downloaded_GitHub_repos(num_of_crawled_notebooks=None):
    f = open('all_urls.csv', 'r')
    reader = csv.reader(f)

    repo_names = []
    paths = []

    for idx, row in enumerate(reader):
        repo_names.append(row[2])
        paths.append(row[3])

    num_of_notebooks = len(repo_names)

    if num_of_crawled_notebooks is None:
        num_of_crawled_notebooks = num_of_notebooks

    repo_names = repo_names[0: num_of_crawled_notebooks]
    paths = paths[0: num_of_crawled_notebooks]
    assert num_of_crawled_notebooks <= num_of_notebooks

    downloaded_GitHub_repos = []
    for idx, (repo_name, path) in enumerate(zip(repo_names, paths)):
        print("{idx} / {total_num} notebooks is prepared for downloading".format(
            idx=idx+1, total_num=num_of_crawled_notebooks))
        repo_name_lst = repo_name.split('/')
        user_name, project_name = repo_name_lst[0], repo_name_lst[1]
        folder_name = user_name+'@'+project_name
        print('User name:'.ljust(15), user_name)
        print('Project name:'.ljust(15), project_name)
        CMD1 = 'git init'
        CMD2 = 'git clone ' + 'https://github.com/' + repo_name 
        CMD3 = 'mv ' + project_name + ' ' + folder_name
        CMDs = []
        CMDs.append(CMD1)
        CMDs.append(CMD2)
        CMDs.append(CMD3)
        CMD = ''
        for idx, command in enumerate(CMDs):
            if idx is not 0:
                CMD += ' && ' + command
            else:
                CMD += command

        if not (folder_name in downloaded_GitHub_repos):
            print(CMD)
            subprocess.call(CMD, shell=True)
            downloaded_GitHub_repos.append(folder_name)
        else:
            print('This repository has been installed.')

    f.close()

    with open('downloaded_notebooks.csv', 'w') as writeFile:
        writer = csv.writer(writeFile)
        for i in range(num_of_crawled_notebooks):
            row = []
            row.append(repo_names[i])
            row.append(paths[i])
            writer.writerow(row)

    writeFile.close()


parser = argparse.ArgumentParser(
    description='automatic GitHub downloading')

parser.add_argument('--num-of-notebooks', type=int, default=None,
                    help='Please specify the number of notebooks you would like to download')

args = parser.parse_args()

downloaded_GitHub_repos(args.num_of_notebooks)
