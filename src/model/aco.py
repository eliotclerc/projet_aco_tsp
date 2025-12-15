from src.model.ant import Ant
from src.model.graph import Graph

from random import randint

def create_ants(nb_ants, graph_nb_node):
    #create ants at random starting position
    return [Ant(randint(0, graph_nb_node - 1), graph_nb_node) for i in range(graph_nb_node)]

def aco(graph : Graph, nb_step, nb_ant, alpha, beta):
    pheromone = graph.pheromone
    distance = graph.distance
    graph_nb_node = len(distance[0])
    ants = create_ants(nb_ant, graph_nb_node)
    
    shortest_cycle_len = float('inf')
    shortest_cycle = None

    for step in range(nb_step):

        #create ants cycle
        for cycle_node_id in range(graph_nb_node - 1):
            for ant in ants:
                ant.go_to(graph, alpha, beta)

        #once the cycle is created

        # pheromone deposit & reset tours
        for ant in ants:
            ant.pheromone_deposit(graph)

            # keep the shortest cycle if found
            ant_cycle_length = ant.current_cycle.compute_distance(graph.distance)
            if(ant_cycle_length < shortest_cycle_len):
                shortest_cycle_len = ant_cycle_length
                shortest_cycle = ant.current_cycle.cycle_node_ids.copy()

            # reset cycle before next iteration
            ant.reset_cycle()
    
    return shortest_cycle, shortest_cycle_len

