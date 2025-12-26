from typing import List, Tuple, Optional
import numpy as np

from src.model.graph import Graph


class ViewModelWarehouse:
    """
    ViewModel exposing warehouses (graph nodes) to the UI.

    - Provides the node count.
    - Provides screen coordinates for each node to initialize the view.
    - Lets the UI fetch a specific position by node id.
    
    """

    def __init__(
        self,
        graph: Graph,
        csv_path: Optional[str] = None,  
    ):
        self.graph = graph
        self.nb_warehouses = len(graph.distance)

        positions = self._generate_positions_from_distances(graph.distance)
        self.positions: List[Tuple[float, float]] = positions

    def get_count(self) -> int:
        """Total number of warehouses (nodes)."""
        return self.nb_warehouses

    def get_positions(self) -> List[Tuple[int, int]]:
        """List of all warehouse positions (x, y)."""
        return list(self.positions)

    def get_position(self, warehouse_id: int) -> Tuple[float, float]:
        """Position (x, y) for the requested warehouse id."""
        return self.positions[warehouse_id]

    def _generate_positions_from_distances(self, distance_matrix) -> List[Tuple[float, float]]:
        n = len(distance_matrix)
        if n == 0:
            return []
        
        if n == 1:
            return [(0.0, 0.0)]
        
        if not isinstance(distance_matrix, np.ndarray):
            D = np.array(distance_matrix, dtype=float)
        else:
            D = distance_matrix.astype(float)
     
        D_squared = D ** 2
        
        row_means = np.mean(D_squared, axis=1, keepdims=True)
        col_means = np.mean(D_squared, axis=0, keepdims=True)
        grand_mean = np.mean(D_squared)
        
        B = -0.5 * (D_squared - row_means - col_means + grand_mean)
        
        eigenvalues, eigenvectors = np.linalg.eigh(B)
        
        idx = np.argsort(eigenvalues)[::-1]
        eigenvalues = eigenvalues[idx]
        eigenvectors = eigenvectors[:, idx]
        
        positive_idx = eigenvalues > 0
        eigenvalues_2d = eigenvalues[positive_idx][:2]
        eigenvectors_2d = eigenvectors[:, positive_idx][:, :2]
        
        positions_2d = eigenvectors_2d * np.sqrt(np.maximum(eigenvalues_2d, 0))
        
        if positions_2d.shape[1] < 2:
            padding = np.zeros((n, 2 - positions_2d.shape[1]))
            positions_2d = np.hstack([positions_2d, padding])
        
        positions = [(float(x), float(y)) for x, y in positions_2d]
        
        return positions

