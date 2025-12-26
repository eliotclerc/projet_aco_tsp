from typing import List, Tuple, Optional
import numpy as np

from src.model.graph import Graph
from sklearn.manifold import MDS


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
        self.positions: List[Tuple[int, int]] = positions

    def get_count(self) -> int:
        """Total number of warehouses (nodes)."""
        return self.nb_warehouses

    def get_positions(self) -> List[Tuple[int, int]]:
        """List of all warehouse positions (x, y)."""
        return list(self.positions)

    def get_position(self, warehouse_id: int) -> Tuple[int, int]:
        """Position (x, y) for the requested warehouse id."""
        return self.positions[warehouse_id]

    def _generate_positions_from_distances(self, distance_matrix) -> List[Tuple[int, int]]:
        n = len(distance_matrix)
        if n == 0:
            return []
        
        if n == 1:
            return self._normalize_to_square([(0.0, 0.0)])
        
        if not isinstance(distance_matrix, np.ndarray):
            D = np.array(distance_matrix)
        else:
            D = distance_matrix
        
        mds = MDS(
            n_components=2,
            dissimilarity='precomputed',
            random_state=42
        )
        positions_2d = mds.fit_transform(D)
        
        positions = [(float(x), float(y)) for x, y in positions_2d]
        
        return self._normalize_to_square(positions)
    
    def _normalize_to_square(self, positions: List[Tuple[float, float]]) -> List[Tuple[int, int]]:
        if not positions:
            return []
        
        xs, ys = zip(*positions)
        min_x, max_x = min(xs), max(xs)
        min_y, max_y = min(ys), max(ys)
        
        span_x = max_x - min_x if max_x != min_x else 1
        span_y = max_y - min_y if max_y != min_y else 1
        
        square_size = 800
        scale = min(square_size / span_x, square_size / span_y) if span_x > 0 and span_y > 0 else 1
        
        offset_x = (1000 - (max_x - min_x) * scale) / 2 - min_x * scale
        offset_y = (1000 - (max_y - min_y) * scale) / 2 - min_y * scale
        
        return [
            (int(x * scale + offset_x), int(y * scale + offset_y))
            for x, y in positions
        ]

