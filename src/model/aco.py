from random import randint

from src.model.ant import Ant
from src.model.graph import Graph

def create_ants(nb_ants, graph_nb_node):
    #create ants at the first node
    return [Ant(randint(0, graph_nb_node - 1), graph_nb_node) for i in range(nb_ants)]

class AcoModel:
    def __init__(self, graph: Graph, nb_ant, alpha, beta, evaporation):
        self.graph = graph
        self.nb_ant = nb_ant
        self.alpha = alpha
        self.beta = beta
        self.evaporation = evaporation

        self.graph_nb_node = len(graph.distance[0])
        self.ants = create_ants(nb_ant, self.graph_nb_node)

        self.current_step = 0
        self.shortest_cycle_len = float('inf')
        self.shortest_cycle = None

    def step(self):
        graph = self.graph

        # ant making their cycle
        for _ in range(self.graph_nb_node - 1):
            for ant in self.ants:
                ant.go_to(graph, self.alpha, self.beta)

        # pheromone deposit 
        for ant in self.ants:
            ant.pheromone_deposit(graph)

            # if shortest path found
            current_cycle = ant.current_cycle
            ant_cycle_length = current_cycle.compute_distance(graph.distance)
            if ant_cycle_length < self.shortest_cycle_len:
                self.shortest_cycle_len = ant_cycle_length
                self.shortest_cycle = current_cycle.cycle_node_ids.copy()

            ant.reset_cycle()

        # pheromone evaporation
        self.graph.pheromone.evaporate(self.evaporation)

        self.current_step += 1

    def run(self, nb_step):
        for _ in range(nb_step):
            self.step()
