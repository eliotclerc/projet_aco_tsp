import random
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
        positions: List[Tuple[int, int]] | None = None,
        center: Tuple[int, int] = (600, 400),
        radius: int = 300,
    ):
        self.graph = graph
        self.nb_warehouses = len(graph.distance)

        # If no positions are provided, scatter nodes randomly within the bounding square.
        self.positions: List[Tuple[int, int]] = positions or self._build_random_layout(
            count=self.nb_warehouses, center=center, radius=radius
        )

        if len(self.positions) != self.nb_warehouses:
            raise ValueError(
                "Provided positions must match the number of graph nodes"
            )

    @staticmethod
    def _build_random_layout(
        count: int, center: Tuple[int, int], radius: int
    ) -> List[Tuple[int, int]]:
        """
        Scatter nodes randomly inside a square centered on `center` with side
        length `2 * radius`.
        """
        if count == 0:
            return []

        cx, cy = center
        positions: List[Tuple[int, int]] = []
        for _ in range(count):
            x = random.randint(cx - radius, cx + radius)
            y = random.randint(cy - radius, cy + radius)
            positions.append((x, y))
        return positions

    def get_count(self) -> int:
        """Total number of warehouses (nodes)."""
        return self.nb_warehouses

    def get_positions(self) -> List[Tuple[int, int]]:
        """List of all warehouse positions (x, y)."""
        return list(self.positions)

    def get_position(self, warehouse_id: int) -> Tuple[int, int]:
        """Position (x, y) for the requested warehouse id."""
        return self.positions[warehouse_id]

