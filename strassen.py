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

def mat_add(a, b, size):
    for i in range(size):
        for j in range(size):
            a[i][j] = a[i][j] + b[i][j]
    return a

def mat_sub(a, b, size):
    for i in range(size):
        for j in range(size):
            a[i][j] = a[i][j] - b[i][j]
    return a

def strassen(matA, matB, size):
    ns = size / 2
    helper = matA.slice(0 , ns)
    a = [row.slice(0, ns) for row in helper]
    b = [row.slice(ns, size) for row in helper]
    helper = matA.slice(ns, size)
    c = [row.slice(0, ns) for row in helper]
    d = [row.slice(ns, size) for row in helper]

    helper = matB.slice(0 , ns)
    e = [row.slice(0, ns) for row in helper]
    f = [row.slice(ns, size) for row in helper]
    helper = matB.slice(ns, size)
    g = [row.slice(0, ns) for row in helper]
    h = [row.slice(ns, size) for row in helper]


    p1 = strassen(a, f - h, ns) 
    p2 = strassen(a + b, h, ns)       
    p3 = strassen(c + d, e, ns)       
    p4 = strassen(d, g - e, ns)       
    p5 = strassen(a + d, e + h, ns)       
    p6 = strassen(b - d, g + h, ns) 
    p7 = strassen(a - c, e + f, ns) 
 
    # Computing the values of the 4 quadrants of the final matrix c
    c11 = mat_add(mat_sub(mat_add(p5, p4), p2), p6)
    c12 = mat_add(p1, p2)          
    c21 = mat_add(p3, p4)           
    c22 = mat_sub(mat_sub(mat_add(p1, p5), p3), p7) 

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