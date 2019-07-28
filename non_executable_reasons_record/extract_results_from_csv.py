import csv, sys
csv.field_size_limit(sys.maxsize)

with open("results.csv", "r") as f:
    reader = csv.reader(f, delimiter=',')
    for line in reader:
        idx, content = line[0], line[1]
        print(idx)
        print(content)
