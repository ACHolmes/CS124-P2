import numpy as np
import sys

def standard(file, dim):
    row = [0] * dim
    col = [0] * dim
    out = [[0 for x in range(dim)] for y in range(dim)] 
    with open(file) as input:
        lines = input.readlines()
        for i in range(dim):



def main():
    if sys.argc != 4:
        print("Usage: python3 strassen.py flag dimension inputfile")
        return 1
    flag = sys.argv[1]
    dim = sys.argv[2]
    file = sys.argv[3]
    with open(file) as input:
        

if __name__ == "__main__":
    main()