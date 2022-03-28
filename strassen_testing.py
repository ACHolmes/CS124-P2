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
    for i in range(flag):
        for j in range(11):
            t = time.perf_counter()
            a = triangles(0.01, 2**j)
            ta = time.perf_counter()
            print("n0 " + str(2**j) + " time: " + str(t - ta))


if __name__ == "__main__":
    main()