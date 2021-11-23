from itertools import permutations
import pandas as pd
import os

file1 = open('./test_traces/uniform-0-1-00.dat', 'r').readlines()
file2 = open('./test_traces/uniform-0-1-01.dat', 'r').readlines()
file3 = open('./test_traces/uniform-0-1-02.dat', 'r').readlines()
file4 = open('./test_traces/uniform-0-1-03.dat', 'r').readlines()
file5 = open('./test_traces/uniform-0-1-04.dat', 'r').readlines()
file6 = open('./test_traces/uniform-0-1-05.dat', 'r').readlines()
file7 = open('./test_traces/uniform-0-1-06.dat', 'r').readlines()

#print(file1.read())

files = [file1, file2, file3, file4, file5, file6, file7]

perms = permutations(files, 2)

for i, perm in enumerate(perms):
    data = pd.DataFrame()
    data['x'] = perm[0]
    data['y'] = perm[1]
    data['x'] = data['x'].apply(lambda x: x[:-1])
    data['y'] = data['y'].apply(lambda x: x[:-1])
    #print(data)
    data.to_csv(f'./test_traces/combo_uniform{i}.dat', sep = ' ', header = False, index = False)
    del data


