from strassen import *
import time

def main():
    if (len(sys.argv) != 4):
        print("Usage: python3 strassen_testing.py flag dimension inputfile")
        return 1
    flag = int(sys.argv[1])
    dim = int(sys.argv[2])
    size = get_size(dim)
    file = sys.argv[3]
    print(" ")
    total = 0
    (A,B) = to_matrices(file, dim, size)
    for i in range(flag):
        for j in range(12):
            i_use = 10
            print(i_use)
            t = time.perf_counter()
            a = strassen(A, B, size, i_use)
            ta = time.perf_counter()
            print("n0 " + str(i_use) + " time: " + str(ta - t))


if __name__ == "__main__":
    main()