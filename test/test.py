from src.model.graph import Graph
from src.model.aco import aco

def main():
    RESET = "\033[0m"
    RED   = "\033[31m"
    GREEN = "\033[32m"
    BOLD  = "\033[1m"

    alpha = 1
    beta = 3
    nb_step = 100
    nb_ant = 10

    tested_graph_name = []
    tested_graph = []
    expected_result = []

    # ------ Test 0 -----
    graph_name = "test/graph/test_0.csv"
    graph = Graph(graph_name)
    test_shortest_path = 23

    tested_graph_name.append(graph_name)
    tested_graph.append(graph)
    expected_result.append(test_shortest_path)

    # ------ Test 1 -----
    graph_name = "test/graph/test_1.csv"
    graph = Graph(graph_name)
    test_shortest_path = 99

    tested_graph_name.append(graph_name)
    tested_graph.append(graph)
    expected_result.append(test_shortest_path)

    # ------ Test 2 -----
    graph_name = "test/graph/test_2.csv"
    graph = Graph(graph_name)
    test_shortest_path = 23

    tested_graph_name.append(graph_name)
    tested_graph.append(graph)
    expected_result.append(test_shortest_path)

    # ------ Test 3 -----
    graph_name = "test/graph/test_3.csv"
    graph = Graph(graph_name)
    test_shortest_path = 29

    tested_graph_name.append(graph_name)
    tested_graph.append(graph)
    expected_result.append(test_shortest_path)

    # ------ Test 4 -----
    graph_name = "test/graph/test_4.csv"
    graph = Graph(graph_name)
    test_shortest_path = 33

    tested_graph_name.append(graph_name)
    tested_graph.append(graph)
    expected_result.append(test_shortest_path)

    # ------ Test 5 -----
    graph_name = "test/graph/test_5.csv"
    graph = Graph(graph_name)
    test_shortest_path = 30

    tested_graph_name.append(graph_name)
    tested_graph.append(graph)
    expected_result.append(test_shortest_path)

    sucess = 0
    for i, graph in enumerate(tested_graph):
        _, result = aco(graph, nb_step, nb_ant, alpha, beta)

        print(f"Graph {BOLD}{tested_graph_name[i]}{RESET} tested")

        if(result == expected_result[i]):
            print(f"{GREEN}Shortest path found for graph{RESET}")
            sucess += 1
        else:
            distance_from_best = result - expected_result[i]

            print(f"{RED}Shortest path not found (distance from best : {distance_from_best}){RESET}")

        print()

    print("----- Test summary ------")
    print(f"Sucess : {sucess}")
    print(f"Fail : {len(tested_graph_name) - sucess}")
    print(f"{sucess}/{len(tested_graph_name)}")
    print("-------------------------")
main()