import numpy as np
import sys
import random

def standard(matA, matB, size):
    out = [[0 for x in range(size)] for y in range(size)] 
    for x in range(size):
        for y in range(size):
            sum = 0
            for i in range(size):
                sum += matA[x][i] * matB[i][y]
            out[x][y] = sum
    return out


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
    out = [[0 for x in range(size)] for y in range(size)]
    for i in range(size):
        for j in range(size):
            out[i][j] = a[i][j] + b[i][j]
    return out

def mat_sub(a, b, size):
    out = [[0 for x in range(size)] for y in range(size)]
    for i in range(size):
        for j in range(size):
            out[i][j] = a[i][j] - b[i][j]
    return out

def strassen(matA, matB, size, n0):

    if size <= n0:
        return standard(matA, matB, size)

    ns = int(size / 2)
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

    p1 = strassen(mat_sub(b, d, ns), mat_add(g, h, ns), ns, n0) 
    p2 = strassen(mat_add(a, d, ns), mat_add(e, h, ns), ns, n0) 
    p3 = strassen(mat_sub(a, c, ns),mat_add(e, f, ns), ns, n0)  
    p4 = strassen(mat_add(a, b, ns), h, ns, n0)  
    p5 = strassen(a, mat_sub(f, h, ns), ns, n0) 
    p6 = strassen(d, mat_sub(g, e, ns), ns, n0)  
    p7 = strassen(mat_add(c, d, ns), e, ns, n0)    
        
    
    # Computing the values of the 4 quadrants of the final matrix c
    c11 = mat_sub(mat_add(p1, mat_add(p2, p6, ns), ns), p4, ns)
    c12 = mat_add(p4, p5, ns)          
    c21 = mat_add(p6, p7, ns)           
    c22 = mat_sub(mat_sub(mat_add(p2, p5, ns), p7, ns), p3, ns)

    result = [[0 for x in range(size)] for y in range(size)]
    for i in range(0, ns):
        for j in range(0, ns):
            result[i][j] = c11[i][j]
            result[i + ns][j] = c21[i][j]
            result[i][j + ns] = c12[i][j]
            result[i + ns][j + ns] = c22[i][j]

    return result

def print_mat(matA):
    for row in matA:
        for i in row:
            print(str(i), end = " ")
        print("")

def triangles(p, n0):
    A = [[0 for x in range(1024)] for y in range(1024)]
    for i in range(1024):
        for j in range(1024):
            if i == j:
                continue
            if random.random() < p:
                A[i][j] = 1
    result = strassen(strassen(A, A, 1024, n0), A, 1024, n0)
    print_mat(result)
    sum = 0
    for i in range(1024):
        sum += result[i][i]
    return int(sum / 6)



def main():
    if (len(sys.argv) != 4):
        print("Usage: python3 strassen.py flag dimension inputfile")
        return 1
    flag = sys.argv[1]
    dim = int(sys.argv[2])
    size = get_size(dim)
    file = sys.argv[3]
    matrices = to_matrices(file, dim, size)
    #print(matrices[0])
    #print(matrices[1])
    #print_mat(strassen(matrices[0], matrices[1], size, 2))
    print(" ")
    print(triangles(1.1, 8))

''' Desired output:
6 2 16
18 15 27 
9 9 18 '''


if __name__ == "__main__":
    main()