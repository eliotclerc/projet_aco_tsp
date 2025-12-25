from typing import List, Tuple

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
        positions: List[Tuple[int, int]],
    ):
        self.graph = graph
        self.nb_warehouses = len(graph.distance)

        if len(positions) != self.nb_warehouses:
            raise ValueError(
                "Provided positions must match the number of graph nodes"
            )
        
        self.positions: List[Tuple[int, int]] = positions

    def get_count(self) -> int:
        """Total number of warehouses (nodes)."""
        return self.nb_warehouses

    def get_positions(self) -> List[Tuple[int, int]]:
        """List of all warehouse positions (x, y)."""
        return list[Tuple[int, int]](self.positions)

    def get_position(self, warehouse_id: int) -> Tuple[int, int]:
        """Position (x, y) for the requested warehouse id."""
        return self.positions[warehouse_id]

