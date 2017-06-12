def equi(A):
    lsum = 0
    rsum = sum(A)
    solution = []
    for index, element in enumerate(A):
        rsum -= element
        if lsum == rsum:
            solution.append(index)
        lsum += element
    return solution

def find_equal_indexes(A):
    equi_for_rows = [equi(l) for l in A]
    equi_for_cols = [equi(l) for l in zip(*A)]

    solution = []
    for col_index, ecol in enumerate(equi_for_cols):
        for row_index in ecol:
            if col_index in equi_for_rows[row_index]:
                solution.append((col_index, row_index))
    return solution

A = [
    [0,0,1],
    [0,1,0],
    [0,1,0],
    [0,0,0],
]

print(find_equal_indexes(A))
