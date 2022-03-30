from sqlite3 import NotSupportedError
import numpy as np
import sys
import random
import time
from datetime import datetime
import os.path

save_path = 'datalogs'

def standard(matA, matB, size):
    out = [[0 for x in range(size)] for y in range(size)] 
    for x in range(size):
        for y in range(size):
            sum = 0
            for i in range(size):
                sum += matA[x][i] * matB[i][y]
            out[x][y] = sum
    return out

def standard_opt(matA, matB, size, xa, ya, xb, yb):
    out = [[0 for x in range(size)] for y in range(size)] 
    for x in range(size):
        for y in range(size):
            sum = 0
            for i in range(size):
                sum += matA[x + xa][i + ya] * matB[i + xb][y + yb]
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

def mat_sub_opt(a, b, xa, ya, xb, yb, size):
    out = [[0 for p in range(size)] for q in range(size)]
    for i in range(0, size):
        for j in range(0, size):
            out[i][j] = a[xa + i][ya + j] - b[i + xb][j + yb]
    return out

def mat_add_opt(a, b, xa, ya, xb, yb, size):
    out = [[0 for p in range(size)] for q in range(size)]
    for i in range(0, size):
        for j in range(0, size):
            out[i][j] = a[xa + i][ya + j] + b[xb + i][yb + j]
    return out

def print_submat(mat, x, y, size):
    for i in range(size):
        for j in range(size):
            print(mat[x + i][y + j], end = " ")
        print('')

def strassen_opt(matA, matB, size, n0, xa, ya, xb, yb):
    if size <= n0:
        return standard_opt(matA, matB, size, xa, ya, xb, yb)

    ns = int(size / 2)

    ax = cy = xa
    ay = bx = ya
    by = dx = xa + ns
    cx = dy = ya + ns

    ex = gy = xb
    ey = fx = yb
    fy = hx = xb + ns
    gx = hy = yb + ns

    p1 = strassen_opt(mat_sub_opt(matA, matA, bx, by, dx, dy, ns), mat_add_opt(matB, matB, gx, gy, hx, hy, ns), ns, n0, 0, 0, 0, 0) 
    p2 = strassen_opt(mat_add_opt(matA, matA, ax, ay, dx, dy, ns), mat_add_opt(matB, matB, ex, ey, hx, hy, ns), ns, n0, 0, 0, 0, 0) 
    p3 = strassen_opt(mat_sub_opt(matA, matA, ax, ay, cx, cy, ns), mat_add_opt(matB, matB, ex, ey, fx, fy, ns), ns, n0, 0, 0, 0, 0) 
    p4 = strassen_opt(mat_add_opt(matA, matA, ax, ay, bx, by, ns), matB, ns, n0, 0, 0, hx, hy)
    p5 = strassen_opt(matA, mat_sub_opt(matB, matB, fx, fy, hx, hy, ns), ns, n0, ax, ay, 0, 0) 
    p6 = strassen_opt(matA, mat_sub_opt(matB, matB, gx, gy, ex, ey, ns), ns, n0, dx, dy, 0, 0)  
    p7 = strassen_opt(mat_add_opt(matA, matA, cx, cy, dx, dy, ns), matB, ns, n0, 0, 0, ex, ey)    
        
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
    p3 = strassen(mat_sub(a, c, ns), mat_add(e, f, ns), ns, n0)  
    p4 = strassen(mat_add(a, b, ns), h, ns, n0)  
    p5 = strassen(a, mat_sub(f, h, ns), ns, n0) 
    p6 = strassen(d, mat_sub(g, e, ns), ns, n0)  
    p7 = strassen(mat_add(c, d, ns), e, ns, n0)    
        
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

def create_P(size, n0):
    size_copy = size
    counter = 0
    while size_copy > n0:
        counter += 1
        size_copy = int(size_copy / 2)
    out = []
    for i in range(counter):
        createSize = int(size / (2 ** (i + 1)))
        for j in range(7):
            out.append([[0 for x in range(createSize)] for y in range(createSize)])
    return out 

def create_C(size, n0):
    size_copy = size
    counter = 0
    while size_copy > n0:
        counter += 1
        size_copy = int(size_copy / 2)
    out = []
    for i in range(counter):
        createSize = int(size / (2 ** i + 1))
        for j in range(7):
            out.append([[0 for x in range(createSize)] for y in range(createSize)])
    return out 

def strassen_fin(matA, matB, size, n0, xa, ya, xb, yb, P, C, count):
    if size <= n0:
        return standard_opt(matA, matB, size, xa, ya, xb, yb)

    ns = int(size / 2)

    ax = cy = xa
    ay = bx = ya
    by = dx = xa + ns
    cx = dy = ya + ns

    ex = gy = xb
    ey = fx = yb
    fy = hx = xb + ns
    gx = hy = yb + ns
    newcount = count + 1
    index = count * 7
    P[index] = strassen_fin(mat_sub_opt(matA, matA, bx, by, dx, dy, ns), mat_add_opt(matB, matB, gx, gy, hx, hy, ns), ns, n0, 0, 0, 0, 0, P, C, newcount) 
    P[index + 1] = strassen_fin(mat_add_opt(matA, matA, ax, ay, dx, dy, ns), mat_add_opt(matB, matB, ex, ey, hx, hy, ns), ns, n0, 0, 0, 0, 0, P, C, newcount) 
    P[index + 2] = strassen_fin(mat_sub_opt(matA, matA, ax, ay, cx, cy, ns), mat_add_opt(matB, matB, ex, ey, fx, fy, ns), ns, n0, 0, 0, 0, 0, P, C, newcount) 
    P[index + 3] = strassen_fin(mat_add_opt(matA, matA, ax, ay, bx, by, ns), matB, ns, n0, 0, 0, hx, hy, P, C, newcount)
    P[index + 4] = strassen_fin(matA, mat_sub_opt(matB, matB, fx, fy, hx, hy, ns), ns, n0, ax, ay, 0, 0, P, C, newcount) 
    P[index + 5] = strassen_fin(matA, mat_sub_opt(matB, matB, gx, gy, ex, ey, ns), ns, n0, dx, dy, 0, 0, P, C, newcount)  
    P[index + 6] = strassen_fin(mat_add_opt(matA, matA, cx, cy, dx, dy, ns), matB, ns, n0, 0, 0, ex, ey, P, C, newcount)    
        
    C[index] = mat_sub(mat_add(P[index], mat_add(P[index + 1], P[index + 5], ns), ns), P[index + 3], ns)
    C[index + 1] = mat_add(P[index + 3], P[index + 4], ns)          
    C[index + 2] = mat_add(P[index + 5], P[index + 6], ns)           
    C[index + 3] = mat_sub(mat_sub(mat_add(P[index + 1], P[index + 4], ns), P[index + 6], ns), P[index + 2], ns)

    result = [[0 for x in range(size)] for y in range(size)]
    for i in range(0, ns):
        for j in range(0, ns):
            result[i][j] = C[index][i][j]
            result[i + ns][j] = C[index + 1][i][j]
            result[i][j + ns] = C[index + 2][i][j]
            result[i + ns][j + ns] = C[index + 3][i][j]
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
    sum = 0
    for i in range(1024):
        sum += result[i][i]
    return int(sum / 6)

def final_result(mat, dim):
    for i in range(dim):
        print(mat[i][i])

def run_triangles(flag):
    total = 0
    for i in range(flag):
        r = triangles(0.01, 16)
        print(r)
        total += r
    print("Average: ", end = "")
    print(total / flag)

def main():
    if (len(sys.argv) != 4):
        print("Usage: python3 strassen.py flag dimension inputfile")
        return 1
    flag = int(sys.argv[1])
    dim = int(sys.argv[2])
    file = sys.argv[3]

    size = get_size(dim)
    n0 = 64
    matrices = to_matrices(file, dim, size)
    n0s = [16, 32, 64, 128]


    now = datetime.now()
    current_time = now.strftime("%H%M")
    filename = "data" + current_time + ".txt"
    finalfile = os.path.join(save_path, filename)
    txt_file = open(finalfile, "w")

    

    for n0 in n0s:
        startstandard = time.perf_counter()
        a = standard(matrices[0], matrices[1], size)
        endstandard = time.perf_counter()
        text = "STANDARD.    Size: " + str(size) + ", n0:  " + str(n0) + ", time: " + str(endstandard - startstandard)
        print(text)
        txt_file.write(text + "\n")

        startstrassen = time.perf_counter()
        result = strassen(matrices[0], matrices[1], size, n0)
        endstrassen = time.perf_counter()
        text = "STRASSEN.    Size: " + str(size) + ", n0:  " + str(n0) + ", time: " + str(endstrassen - startstrassen)
        print(text)
        txt_file.write(text + "\n")

        startstrassenopt = time.perf_counter()
        result = strassen_opt(matrices[0], matrices[1], size, n0, 0, 0, 0, 0)
        endstrassenopt = time.perf_counter()
        text = "STRASSENOPT. Size: " + str(size) + ", n0:  " + str(n0) + ", time: " + str(endstrassenopt - startstrassenopt)
        print(text)
        txt_file.write(text + "\n")
    
        startstrassenfin = time.perf_counter()
        P = create_P(size, n0)
        C = create_C(size, n0)
        result = strassen_fin(matrices[0], matrices[1], size, n0, 0, 0, 0, 0, P, C, 0)
        endstrassenfin = time.perf_counter()
        text = "STRASSENFIN. Size: " + str(size) + ", n0:  " + str(n0) + ", time: " + str(endstrassenfin - startstrassenfin)
        print(text)
        print('')
        txt_file.write(text + "\n")
        txt_file.write("\n")

    txt_file.close()
    #print(result)
    #final_result(result, dim)



if __name__ == "__main__":
    main()