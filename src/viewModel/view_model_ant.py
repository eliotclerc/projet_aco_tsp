from src.model.node import Node
from typing import Tuple, Dict
from src.viewModel.view_model_warehouse import ViewModelWarehouse


class ViewModelAnt:
    """
    ViewModel to represent an ant in the view with animation.
    """
    
    def __init__(
        self,
        prev_model_node: Node,
        curr_model_node: Node,
        animation_progress: float = 0.0
    ):
        """
        Initializes an ant ViewModel.
        
        Args:
            prev_model_node (Node): The previous node in the cycle
            curr_model_node (Node): The current node in the cycle
            animation_progress (float): Animation progress between 0.0 and 1.0
        """
        self.prev_model_node = prev_model_node
        self.curr_model_node = curr_model_node
        # Clamp animation progress between 0.0 and 1.0
        self.animation_progress = max(0.0, min(1.0, animation_progress))
    
    def get_position(self, warehouse_map: Dict[int, 'ViewModelWarehouse']) -> Tuple[int, int]:
        """
        Returns the current position of the ant based on animation progress.

        Args:
            warehouse_map: Dictionary {node_id: ViewModelWarehouse} to get coordinates

        Returns:
            Tuple[int, int]: The (x, y) coordinates of the ant
        """
        # Get the coordinates of both nodes
        prev_warehouse = warehouse_map.get(self.prev_model_node.node_id)
        curr_warehouse = warehouse_map.get(self.curr_model_node.node_id)

        # Return default position if nodes not found
        if prev_warehouse is None or curr_warehouse is None:
            return (0, 0)

        # Linear interpolation between the two nodes
        x1, y1 = prev_warehouse.screen_x, prev_warehouse.screen_y
        x2, y2 = curr_warehouse.screen_x, curr_warehouse.screen_y

        x = int(x1 + (x2 - x1) * self.animation_progress)
        y = int(y1 + (y2 - y1) * self.animation_progress)

        return (x, y)
    
    def update_position(self, delta_progress: float = 0.01) -> bool:
        """
        Updates the ant's position by incrementing the animation progress.
        
        Args:
            delta_progress (float): Progress increment (default: 0.01)
        
        Returns:
            bool: True if animation is complete, False otherwise
        """
        self.animation_progress = min(1.0, self.animation_progress + delta_progress)
        
        # Returns True if animation is complete
        return self.animation_progress >= 1.0
    
    @staticmethod
    def from_ant_cycle(ant_cycle_node_ids, current_edge_index: int, animation_progress: float = 0.0) -> 'ViewModelAnt':
        """
        Creates a ViewModelAnt from an ant cycle (list of node IDs).
        
        Args:
            ant_cycle_node_ids: List or numpy array of node IDs in the cycle
            current_edge_index: Index of the current edge in the cycle (0 = first edge)
            animation_progress: Animation progress between 0.0 and 1.0
        
        Returns:
            ViewModelAnt: Instance created from the cycle
        """
        if len(ant_cycle_node_ids) < 2:
            raise ValueError("The cycle must contain at least 2 nodes to create a ViewModelAnt")
        
        # Calculate indices for previous and current nodes
        # Using modulo to wrap around for circular cycles
        prev_index = current_edge_index % len(ant_cycle_node_ids)
        curr_index = (current_edge_index + 1) % len(ant_cycle_node_ids)
        
        # Create Node objects from the IDs
        prev_node = Node(ant_cycle_node_ids[prev_index])
        curr_node = Node(ant_cycle_node_ids[curr_index])
        
        return ViewModelAnt(prev_node, curr_node, animation_progress)
