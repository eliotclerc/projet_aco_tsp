from random import randint

from model.ant import Ant
from model.graph import Graph

def create_ants(nb_ants, graph_nb_node):
    """
    Create a list of ants initialized at random starting nodes.

    Parameters
    ----------
    nb_ants : int
        Number of ants to create.
    graph_nb_node : int
        Number of nodes in the graph.

    Returns
    -------
    Ant[]
        List of initialized Ant instances.
    """

    #create ants at the first node
    return [Ant(randint(0, graph_nb_node - 1), graph_nb_node) for i in range(nb_ants)]

class AcoModel:
    """
    A model implementing the Ant Colony Optimization (ACO) algorithm.

    This class manages the population of ants, the interaction with the graph,
    the pheromone update rules, and the iterative optimization process.

    Attributes
    ----------
    graph : Graph
        Graph on which the optimization is performed.
    nb_ant : int
        Number of ants used in the simulation.
    alpha : float
        Influence factor of pheromone in the transition probability.
    beta : float
        Influence factor of heuristic information (e.g., distance).
    evaporation : float
        Pheromone evaporation rate applied after each iteration.
    graph_nb_node : int
        Number of nodes in the graph.
    ants : Ant[]
        List of ants participating in the simulation.
    current_step : int
        Current iteration index of the algorithm.
    shortest_cycle_len : float
        Length of the shortest cycle found so far.
    shortest_cycle : int[] | None
        Node indices representing the shortest cycle found so far.
    """

    def __init__(self, graph: Graph, nb_ant, alpha, beta, evaporation):
        """
        Initialize the ACO model with a graph and algorithm parameters.

        Parameters
        ----------
        graph : Graph
            Graph on which the optimization will be executed.
        nb_ant : int
            Number of ants to create.
        alpha : float
            Weight of pheromone in the decision rule.
        beta : float
            Weight of heuristic information in the decision rule.
        evaporation : float
            Pheromone evaporation rate.
        """

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
        """
        Perform a single iteration of the ACO algorithm.

        During this step:
        - Each ant builds a complete cycle on the graph.
        - Pheromone is deposited according to the ants' cycles.
        - The shortest cycle is updated if a better solution is found.
        - Pheromone evaporation is applied.
        - The internal step counter is incremented.
        """

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
        """
        Run the ACO algorithm for a given number of iterations.

        Parameters
        ----------
        nb_step : int
            Number of iterations to execute.
        """

        for _ in range(nb_step):
            self.step()
