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

        #create a nb_node * nb_node matrix with initial pheromone
        self.pheromone_quantity = zeros(shape = shape, dtype = float)
        
        # Initialize with small positive pheromone to encourage exploration
        initial_pheromone = 1.0 / nb_node
        self.pheromone_quantity[:] = initial_pheromone

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
        self.pheromone_quantity *= (1 - rho)

    def display(self):
        """
        Print the pheromone matrix row by row.
        """
        for row in self.pheromone_quantity:
            for column in row:
                print(column, end=" ")
            
            print()
