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

def strassen(matA, matB, size, n0):

    if size == n0:
        return standard(matA, matB, size)

    ns = int(size / 2)
    print(ns)
    helper = matA[0: ns]
    a = [row[0: ns] for row in helper]
    b = [row[ns: size] for row in helper]
    helper = matA[ns: size]
    c = [row[0: ns] for row in helper]
    d = [row[ns: size] for row in helper]

    helper = matB[0: ns]
    e = [row[0: ns] for row in helper]
    f = [row[ns: size] for row in helper]
    helper = matB[ns: size]
    g = [row[0: ns] for row in helper]
    h = [row[ns: size] for row in helper]

    print(a)
    p1 = strassen(a, mat_sub(f, h, ns), ns, n0) 
    p2 = strassen(mat_add(a, b, ns), h, ns, n0)       
    p3 = strassen(mat_add(c, d, ns), e, ns, n0)       
    p4 = strassen(d, mat_sub(g, e, ns), ns, n0)       
    p5 = strassen(mat_add(a, d, ns), mat_add(e, h, ns), ns, n0)       
    p6 = strassen(mat_sub(b, d, ns), mat_add(g, h, ns), ns, n0) 
    p7 = strassen(mat_sub(a, c, ns),mat_add(e, f, ns), ns, n0) 
 
    # Computing the values of the 4 quadrants of the final matrix c
    c11 = mat_add(mat_sub(mat_add(p5, p4), p2), p6)
    c12 = mat_add(p1, p2)          
    c21 = mat_add(p3, p4)           
    c22 = mat_sub(mat_sub(mat_add(p1, p5), p3), p7) 

    #make full matrix and go home
    C = []
    for row in c11:
        for r in c12:
            C.append(row.append(r))
    C_bottom = []
    for row in c21:
        for r in c22:
            C_bottom.append(row.append(r))
    C.append(C_bottom)
    return C

def main():
    if (len(sys.argv) != 4):
        print("Usage: python3 strassen.py flag dimension inputfile")
        return 1
    flag = sys.argv[1]
    dim = int(sys.argv[2])
    size = get_size(dim)
    file = sys.argv[3]
    matrices = to_matrices(file, dim, size)
    print(standard(file, 3))
    print(strassen(matrices[0], matrices[1], size, 2))

if __name__ == "__main__":
    main()