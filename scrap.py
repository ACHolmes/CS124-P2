def standard_old(file, dim):
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