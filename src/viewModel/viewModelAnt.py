from typing import List, Optional, Tuple

from src.model.ant import Ant
from src.viewModel.viewModelWarehouse import ViewModelWarehouse


class ViewModelAnt:
    """
    ViewModel exposing ant state:
    - current positions
    - direction (target warehouse)
    - total count
    """

    def __init__(self, ants: List[Ant], warehouse_vm: ViewModelWarehouse):
        self.ants = ants
        self.warehouse_vm = warehouse_vm

    def get_count(self) -> int:
        return len(self.ants)

    def get_current_node_ids(self) -> List[int]:
        """Node ids where ants are currently located."""
        return [int(ant.current_cycle.cycle_node_ids[-1]) for ant in self.ants]

    def get_positions(self) -> List[Tuple[int, int]]:
        """Screen positions matching ants' current nodes."""
        return [self.warehouse_vm.get_position(node_id) for node_id in self.get_current_node_ids()]

    def get_target_node_ids(self) -> List[Optional[int]]:
        """Node ids each ant is currently targeting."""
        return [ant.current_target_node_id for ant in self.ants]

    def get_target_coordinates(self) -> List[Optional[Tuple[int, int]]]:
        """
        Target warehouse coordinates (x, y) for each ant.
        If the ant has no target yet (e.g., before first move), returns None.
        """
        targets: List[Optional[Tuple[int, int]]] = []
        for node_id in self.get_target_node_ids():
            if node_id is None:
                targets.append(None)
            else:
                targets.append(self.warehouse_vm.get_position(node_id))
        return targets

