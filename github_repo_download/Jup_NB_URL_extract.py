import csv 

repo_URLs = []
file_URLs = []
repos = []
notebook_paths = []

with open('executed_notebooks.csv', 'r') as f:
    reader = csv.reader(f)
    headers = next(reader, None)

    row = next(reader, None)
    while row is not None:
        # filter out problematic data
        if len(row) is not 5:
            pass
        else:
            repo, commit, notebook_path = row[1], row[2], row[3]
            repo_URL = 'https://github.com/' + repo
            file_URL = 'https://github.com/' + repo + '/blob/' + commit + '/' + notebook_path
            repo_URLs.append(repo_URL)
            file_URLs.append(file_URL)
            # repos.append(repo)
            notebook_paths.append(notebook_path)
            print(repo_URL, file_URL)
        try:
            row = next(reader, None)
        except:
            pass 

f.close()

# with open('all_urls.csv', 'w', newline='') as writeFile:
#     writer = csv.writer(writeFile)
#     for i in range(len(repo_URLs)):
#         row = []
#         row.append(repo_URLs[i])
#         row.append(file_URLs[i])
#         row.append(repos[i])
#         row.append(notebook_paths[i])
#         writer.writerow(row)

# writeFile.close()
