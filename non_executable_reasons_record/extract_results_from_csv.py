import csv, sys
csv.field_size_limit(sys.maxsize)

with open("results.csv", "r") as f:
    reader = csv.reader(f, delimiter=',')
    for line in reader:
        idx, path, content = line[0], line[1], line[2]
        print('ID:', idx)
        print('Path:', path)
        print('Content:', content)
