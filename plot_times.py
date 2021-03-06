from re import S
import matplotlib.pyplot as plt
import os

save_path = 'datalogs'
opener = os.path.join(save_path, 'data2048.txt')
with open(opener) as f:
    lines = f.readlines()
    lines_clean = []
    for line in lines:
        if line.find('S') != -1:
            lines_clean.append(line)

    times = []
    n0s = []
    for el in lines_clean:
        #print(el)
        text = el.split(':')
        #print(text)
        intermediate = text[2].split(',')
        n0 = intermediate[0].strip()
        n0s.append(int(n0))
        number = text[3].strip()
        times.append(float(number))
        #print(number)

    t_standard = []
    t_strassen = []
    t_strassenopt = []
    t_strassenfin = []

    for el in times:
        idx = int((times.index(el)) / 5 )
        if idx == 0:
            t_standard.append(el)
        elif idx == 1:
            t_strassen.append(el)
        elif idx == 2:
            t_strassenopt.append(el)
        else:
            t_strassenfin.append(el)

    n0s_clean = list(dict.fromkeys(n0s))

    plt.scatter(n0s_clean, t_standard, color="Red", label="Standard")
    plt.scatter(n0s_clean, t_strassen, color="Blue", label="Strassen")
    plt.scatter(n0s_clean, t_strassenopt, color="Pink", label="Strassenopt")
    plt.scatter(n0s_clean, t_strassenfin, color="Black", label="Strassenfin")
    plt.legend(loc="upper right")
    plt.xlabel('Crossover matrix size (n0)')
    plt.ylabel('Algorithm run time (s)')
    plt.savefig('plottimesnew.png')
    plt.show()
    
