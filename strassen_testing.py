from strassen import *
import time

save_path = 'datalogs'

def main():
    if (len(sys.argv) != 4):
        print("Usage: python3 strassen_testing.py flag dimension inputfile")
        return 1
    flag = int(sys.argv[1])
    dim = int(sys.argv[2])
    size = get_size(dim)
    inputfile = sys.argv[3]
    file = os.path.join("testfiles/", inputfile)
    print(" ")
    total = 0
    matrices = to_matrices(file, dim, size)
    n0s = [32 ,64, 128]
    now = datetime.now()
    current_time = now.strftime("%H%M")
    filename = "data" + current_time + ".txt"
    finalfile = os.path.join(save_path, filename)
    txt_file = open(finalfile, "w")

    for n0 in n0s:
        test(strassen_fin, matrices[0], matrices[1], size, n0, txt_file)
        test(strassen, matrices[0], matrices[1], size, n0, txt_file)
        test(standard, matrices[0], matrices[1], size, n0, txt_file)
        test(strassen_opt, matrices[0], matrices[1], size, n0, txt_file)

        print(' ')
    txt_file.close()


   #file = os.path.join("testfiles/", inputfile)
    '''
    Used for testing
    
    n0s = [32, 64]
    now = datetime.now()
    current_time = now.strftime("%H%M")
    filename = "data" + current_time + ".txt"
    finalfile = os.path.join(save_path, filename)
    txt_file = open(finalfile, "w")

    for n0 in n0s:
        test(standard, matrices[0], matrices[1], size, n0, txt_file)
        test(strassen, matrices[0], matrices[1], size, n0, txt_file)
        test(strassen, matrices[0], matrices[1], size, n0, txt_file)
        test(strassen_fin, matrices[0], matrices[1], size, n0, txt_file)
        print(' ')
    txt_file.close()
    '''


if __name__ == "__main__":
    main()