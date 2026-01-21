"""
Main author: Eliot Clerc
"""
import numpy as np

class Cycle:
    """
    Represents a Hamiltonian cycle as an ordered array of node indices.

    Attributes
    ----------
    cycle_node_ids : int[]
        Ordered node identifiers defining the cycle.
    """

    cycle_node_ids = None

    def __init__(self):
        """
        Initialize an empty cycle.

        Returns
        -------
        None
        """

        #empty cycle
        self.cycle_node_ids = np.array([], dtype = int)

    def add_node(self, node_id):
        """
        Append a node identifier to the cycle.

        Parameters
        ----------
        node_id : int
            Node identifier to append.

        Returns
        -------
        None
        """

        self.cycle_node_ids = np.append(self.cycle_node_ids, node_id)

    def compute_distance(self, distance_matrix):
        """
        Compute the total length of the cycle, including the return edge.

        Parameters
        ----------
        distance_matrix : float[][]
            Square matrix of inter-node distances.

        Returns
        -------
        float
            Total length of the cycle.
        """

        length = 0
        cycle = self.cycle_node_ids

        prec_node_id = cycle[0]
        for i in range(1, len(cycle) + 1):
            #% to also compute the last distance to come back to the starting node
            curr_node_id = cycle[i % len(cycle)]

            length += distance_matrix[prec_node_id][curr_node_id]
            prec_node_id = curr_node_id


        return length
