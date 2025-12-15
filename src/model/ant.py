from typing import List

class Ant:

    def __init__(self):

        self.current_node_id: int = 0
        self.current_cycle: List[int] = []
        self.visited_nodes: List[bool] = []
        
    def go_to(self, next_node_id: int) -> None:

        self.current_node_id = next_node_id
        self.current_cycle.append(next_node_id)
        self.visited_nodes[next_node_id] = True
