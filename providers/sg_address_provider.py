from pathlib import Path
import csv
import random

filename = 'sg_zipcode_mapper.csv'
cur_path = Path.cwd().joinpath(filename)
cur_path.resolve()

count = 10
lines = []

with open(cur_path) as f:
    # Find total number of rows
    row_total = sum(1 for line in f)
    # Generate random line number
    chosen = sorted(random.sample(range(1,row_total), count))
    
    f.seek(0)
    header = f.readline().strip().split(',')
        
    for offset in chosen:
        f.seek(offset)
        f.readline()
        line = f.readline().strip()
        lines.append(line.split(','))

result = []
for line in lines:
    j = zip(header,line)
    obj = {k: v for k, v in j}
    print(obj)
