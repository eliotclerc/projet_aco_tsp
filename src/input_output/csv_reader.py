import numpy as np

def load_distance_matrix(path):
    """
    Reads a CSV file where:
    - line 1 contains an integer n (matrix dimension)
    - the next n lines contain comma-separated numeric values
    
    Return:
        np.ndarray of shape (n, n) (type int or float)
    """

    with open(path, "r") as f:
        lines = f.read().strip().splitlines()

    n = int(lines[0].strip())  # number of nodes
    matrix_lines = lines[1 : 1 + n]

    matrix = []
    for line in matrix_lines:
        row = [float(x) for x in line.split(",")]
        matrix.append(row)

    return np.array(matrix)
