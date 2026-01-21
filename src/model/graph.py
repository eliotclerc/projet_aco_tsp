from src.input_output.csv_reader import load_distance_matrix
from src.model.pheromone_matrix import PheromoneMatrix
class Graph:
    """
    Graph containing a distance matrix and its associated pheromone matrix.

    Attributes
    ----------
    distance : float[][]
        Square matrix of distances between nodes.
    pheromone : PheromoneMatrix
        Pheromone matrix associated with the graph.
    """


    distance = None
    pheromone = None

    def __init__(self, path):
        """
        Initialize the graph from a CSV file.

        Parameters
        ----------
        path : str
            Path to the CSV file containing the distance matrix.

        Returns
        -------
        None
        """

        #create a distance matrix from a csv file
        self.distance = load_distance_matrix(path)
        
        #create a corresponding empty pheromone matrix
        nb_node = len(self.distance)
        self.pheromone = PheromoneMatrix(nb_node)

    def display(self):
        """
        Print the distance adjacency matrix to standard output.

        Returns
        -------
        None
        """

        for row in self.distance:
            for column in row:
                print(column, end=" ")
            
            print()