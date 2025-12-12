from src.input_output.csv_reader import load_distance_matrix
from src.model.pheromoneMatrix import PheromoneMatrix
class Graph:
    """
    Graph structure containing a distance matrix and its associated pheromone matrix.
    """
    
    distance = None
    pheromone = None

    def __init__(self, path):
        #create a distance matrix from a csv file
        self.distance = load_distance_matrix(path)
        
        #create a corresponding empty pheromone matrix
        nb_node = len(self.distance)
        self.pheromone = PheromoneMatrix(nb_node)

    def display(self):
        """
        Display the adjacency matrix
        """
        for row in self.distance:
            for column in row:
                print(column, end=" ")
            
            print()