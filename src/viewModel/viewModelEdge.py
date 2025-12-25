from typing import List, Tuple

import numpy as np

from src.model.graph import Graph


class ViewModelEdge:
    """
    ViewModel dedicated to edges to expose pheromone coefficients.
    """

    def __init__(self, graph: Graph):
        self.graph = graph

    def get_pheromone(self, node_a: int, node_b: int) -> float:
        """Current pheromone coefficient for edge (a, b)."""
        return float(self.graph.pheromone.pheromone_quantity[node_a][node_b])

    def get_all_pheromones(self) -> np.ndarray:
        """Complete pheromone matrix (copy)."""
        return self.graph.pheromone.pheromone_quantity.copy()

    def get_symmetric_edges(self) -> List[Tuple[int, int, float]]:
        """Return (i, j, tau_ij) pairs for i < j."""
        matrix = self.graph.pheromone.pheromone_quantity
        edges: List[Tuple[int, int, float]] = []
        for i in range(matrix.shape[0]):
            for j in range(i + 1, matrix.shape[1]):
                edges.append((i, j, float(matrix[i][j])))
        return edges

    def get_normalized(self) -> np.ndarray:
        """
        Matrix normalized between 0 and 1 for direct color mapping.
        """
        matrix = self.graph.pheromone.pheromone_quantity
        if matrix.size == 0:
            return matrix

        min_val = float(matrix.min())
        max_val = float(matrix.max())
        amplitude = max_val - min_val
        if amplitude == 0:
            return np.zeros_like(matrix)

        return (matrix - min_val) / amplitude

