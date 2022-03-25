import numpy as np
import sys

def standard(file, dim):
    row = [0] * dim
    col = [0] * dim
    offset = dim**2
    out = [[0 for x in range(dim)] for y in range(dim)] 
    with open(file) as input:
        lines = input.readlines()
        for r in range(dim):
            for i in range(dim):
                sum = 0
                for k in range(dim):
                    row[k] = int(lines[k + r * dim])
                    col[k] = int(lines[k * dim + i + offset])
                    sum += row[k] * col[k]
                out[r][i] = sum
    '''
    for k in out:
        for j in k:
            print(j)
    '''
    return out

''' Desired output:
6 2 16
18 15 27 
9 9 18 '''

def to_matrices(file, dim, size):
    matA = [[0 for x in range(size)] for y in range(size)] 
    matB = [[0 for x in range(size)] for y in range(size)] 
    offset = dim**2
    with open(file) as input:
        lines = input.readlines()
        for i in range(dim):
            for j in range(dim):
                matA[j][i] = int(lines[i + j*dim])
                matB[j][i] = int(lines[i + j*dim + offset])
    return (matA, matB)

def get_size (dim):
    dim_use = dim
    counter = 0
    while dim_use > 1:
        dim_use = dim_use / 2
        counter = counter + 1
    pad = 2**(counter) - dim
    size = dim + pad
    return size

def main():
    if (len(sys.argv) != 4):
        print("Usage: python3 strassen.py flag dimension inputfile")
        return 1
    flag = sys.argv[1]
    dim = int(sys.argv[2])
    size = get_size(dim)
    print(size)
    file = sys.argv[3]
    print(to_matrices(file, dim, size))
    print(standard(file, 3))
        

if __name__ == "__main__":
    main()