from numpy import zeros, nditer

class PheromoneMatrix:
    """
    A class used to represent the amount of pheromone
    on each edges of the graph

    Attributes
    ----------
    pheromone_quantity : float[][]
        The quantity of pheromone on each edges of the graph
    """
    pheromone_quantity = None

    def __init__(self, nb_node):
        shape = (nb_node, nb_node)

        #create a nb_node * nb_node matrix full of 0
        self.pheromone_quantity = zeros(shape = shape, dtype = float)

    def evaporate(self, rho):
        """
        Reduce the amount of pheromone on each edges to simulate evaporation

        This method takes rho, a numeric arguments, and multiply each edges
        pheromone amount by (1 - rho).

        Args:
            a (float): The evaporation factor (must be 0 < rho < 1)

        Returns:
            Nothing
        """
        #iterate over all elements efficiently
        for pheromone in nditer(self.pheromone_quantity):
            pheromone *= (1 - rho)

    def display(self):
        for row in self.pheromone_quantity:
            for column in row:
                print(column, end=" ")
            
            print()
