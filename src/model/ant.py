"""
Main author: Corentin Romano
"""
from src.model.cycle import Cycle
from src.model.graph import Graph
import numpy as np
from random import choices
from random import randint


#choose uniformely if all weight are 0
def safe_choices(population, weights=None, *, k=1):
    """
    Select element(s) from a population with optional weights.

    Falls back to uniform selection if weights are None or their sum is zero.

    Parameters
    ----------
    population : list
        Elements to sample from.
    weights : list[float] | None, optional
        Selection weights.
    k : int, optional
        Number of elements to select.

    Returns
    -------
    Any | list
        Selected element if k == 1, otherwise a list.
    """

    if len(population) == 1:
        result = [population[0]]
        return result[0] if k == 1 else result
    
    if weights is None:
        result = choices(population, k=k)
        return result[0] if k == 1 else result
    
    total = sum(weights)
    
    if total == 0:
        result = choices(population, k=k)
        return result[0] if k == 1 else result

    result = choices(population, weights=weights, k=k)
    return result[0] if k == 1 else result


class Ant:
    """
    Represents an ant in the Ant Colony Optimization algorithm.

    The ant builds a cycle, deposits pheromone, and can be reset for a new
    iteration.

    Attributes
    ----------
    current_cycle : Cycle
        Current cycle built by the ant.
    visited_node : bool[]
        Visited nodes mask.
    """

    current_cycle = None
    visited_node = None

    def __init__(self, starting_node_id, graph_nb_node):
        """
        Initialize the ant with a starting node and visitation state.

        Parameters
        ----------
        starting_node_id : int
            Starting node identifier.
        graph_nb_node : int
            Number of nodes in the graph.
        """

        self.current_cycle = Cycle()

        # create visited node array to mark it
        self.visited_node = np.array([False for i in range(graph_nb_node)])

        #add the starting node to the tour and mark it
        self.current_cycle.add_node(starting_node_id)
        self.visited_node[starting_node_id] = True

    def go_to(self, graph: Graph, alpha: float, beta: float):
        """
        Move the ant to the next node using pheromone and heuristic weights.

        Parameters
        ----------
        graph : Graph
            Graph containing distances and pheromones.
        alpha : float
            Pheromone influence factor.
        beta : float
            Heuristic influence factor.

        Raises
        ------
        RuntimeError
            If no unvisited nodes remain.
        """

        distance = graph.distance
        pheromone = graph.pheromone.pheromone_quantity

        current_node = self.current_cycle.cycle_node_ids[-1]

        potential_nodes = []
        weights = []

        # Build probabilities ONLY for unvisited nodes
        for node_id in range(len(distance)):
            if not self.visited_node[node_id]:
                tau = pheromone[current_node][node_id]
                eta = 1.0 / distance[current_node][node_id]

                weight = (tau ** alpha) * (eta ** beta)
                potential_nodes.append(node_id)
                weights.append(weight)

        # Safety check (should not happen in TSP, but prevents crashes)
        if not potential_nodes:
            raise RuntimeError("No unvisited nodes available")

        # Choose next node (uniform if all weights are zero)
        next_node_id = safe_choices(
            potential_nodes,
            weights=weights,
            k=1
        )

        # Update state
        self.visited_node[next_node_id] = True
        self.current_cycle.add_node(next_node_id)


    def pheromone_deposit(self, graph : Graph):
        """
        Deposit pheromone on the graph based on the current cycle.

        Parameters
        ----------
        graph : Graph
            Graph whose pheromone matrix is updated.
        """

        distance_matrix = graph.distance
        pheromone_matrix = graph.pheromone.pheromone_quantity

        cycle = self.current_cycle.cycle_node_ids
        cycle_length = self.current_cycle.compute_distance(distance_matrix)

        #pheromone quantity to deposit
        delta = 1 / cycle_length

        prec_node_id = cycle[0]
        for i in range (1, len(cycle) + 1):
            curr_node_id = cycle[i % len(cycle)]

            pheromone_matrix[prec_node_id][curr_node_id] += delta
            prec_node_id = curr_node_id

    def reset_cycle(self):
            """
            Reset the ant state and choose a new random starting node.
            """

            graph_nb_node = len(self.visited_node)

            # reset visited nodes
            self.visited_node = np.array([False for i in range(graph_nb_node)])

            # empty current cycle
            self.current_cycle = Cycle()

            # choose starting node randomly
            starting_node_id = randint(0, graph_nb_node - 1)

            # add the starting node to the tour and mark it
            self.current_cycle.add_node(starting_node_id)
            self.visited_node[starting_node_id] = True


