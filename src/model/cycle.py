import numpy as np

class Cycle:
    cycle_node_ids = None

    def __init__(self):
        #empty cycle
        self.cycle_node_ids = np.array([], dtype = int)

    def add_node(self, node_id):
        self.cycle_node_ids = np.append(self.cycle_node_ids, node_id)

    def compute_distance(self, distance_matrix):
        length = 0
        cycle = self.cycle_node_ids

        prec_node_id = cycle[0]
        for i in range(1, len(cycle) + 1):
            #% to also compute the last distance to come back to the starting node
            curr_node_id = cycle[i % len(cycle)]

            length += distance_matrix[prec_node_id][curr_node_id]
            prec_node_id = curr_node_id

        return length
