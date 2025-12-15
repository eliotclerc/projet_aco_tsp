from src.model.cycle import Cycle
from src.model.graph import Graph
import numpy as np
from random import choices
from random import randint


#choose uniformely if all weight are 0
def safe_choices(population, weights=None, *, k=1):
    total = sum(weights)
    
    if len(population) == 1:
        return population[0]

    if weights is None or total == 0:
        return choices(population, k=k)

    return choices(population, weights=weights, k=k)


class Ant:
    current_cycle = None
    visited_node = None

    def __init__(self, starting_node_id, graph_nb_node):
        self.current_cycle = Cycle()

        # create visited node array to mark it
        self.visited_node = np.array([False for i in range(graph_nb_node)])

        #add the starting node to the tour and mark it
        self.current_cycle.add_node(starting_node_id)
        self.visited_node[starting_node_id] = True

    def go_to(self, graph: Graph, alpha: float, beta: float):
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


