import csv
'''
# Prepare a csv for writing results 
with open('results.csv', 'w') as writeFile:
    writer = csv.writer(writeFile)

    file_str = 'a.txt'

    f = open(file_str, "r")
    for name in f:
        target_result_file_name = name.strip() + '.txt'
        tf = open(target_result_file_name, 'r')
        content = tf.read()
        row = [name.strip(), content]
        writer.writerow(row)

writeFile.close()
'''

import csv

with open("results.csv", "r") as f:
    reader = csv.reader(f, delimiter="\t")
    for i, line in enumerate(reader):
        print(i, line)
