from src.model.graph import Graph

def main():
    my_graph = Graph("test/test1.csv")

    print("Loaded distance matrix :")
    my_graph.display()

    print()
    print("Created pheromone matrix (supposed to be only 0)")
    my_graph.pheromone.display()

main()
