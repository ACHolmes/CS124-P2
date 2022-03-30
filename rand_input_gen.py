import random
import os.path
import sys

def filemaker(matrix_size):
    inp = []
    nums_needed = 2 * matrix_size**2
    for i in range(nums_needed):
        inp.append(random.randint(0,2))
    return inp

def to_txt(lst, filename):
    file = os.path.join("testfiles/", filename)
    print(file)
    txt_file = open(file, "w")
    for el in lst:
        txt_file.write(str(el) + "\n")
    txt_file.close()

def main():
    if (len(sys.argv) != 2):
        print("Usage: python3 rand_input_gen.py size")
        return 1
    size = int(sys.argv[1])
    to_txt(filemaker(size), "test" + str(size) + ".txt")

if __name__ == "__main__":
    main()