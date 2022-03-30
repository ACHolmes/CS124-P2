import random

def filemaker(matrix_size):
    inp = []
    nums_needed = 2 * matrix_size**2
    for i in range(nums_needed):
        inp.append(random.randint(0,2))
    return inp

def to_txt(lst, filename):
    txt_file = open(filename, "w")
    for el in lst:
        txt_file.write(str(el) + "\n")
    txt_file.close()


to_txt(filemaker(2048), "tester2.txt")