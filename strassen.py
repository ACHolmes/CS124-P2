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

def strassen (a, b, dim):
    a_np = np.matrix(a)
    b_np = np.matrix(b)

    #size = np.sqrt(a_np.size)
    dim_use = dim
    counter = 0
    while size > 1:
        dim_use = dim_use / 2
        counter = counter + 1
    pad = dim - 2**(counter)
    size = dim + pad

    





def main():
    if (len(sys.argv) != 4):
        print("Usage: python3 strassen.py flag dimension inputfile")
        return 1
    flag = sys.argv[1]
    dim = sys.argv[2]
    file = sys.argv[3]
    print(standard(file, 3))
        

if __name__ == "__main__":
    main()