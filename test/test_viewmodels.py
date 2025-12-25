from src.model.graph import Graph
from src.model.ant import Ant
from src.viewModel.viewModelWarehouse import ViewModelWarehouse
from src.viewModel.viewModelAnt import ViewModelAnt
from src.viewModel.viewModelEdge import ViewModelEdge


def test_viewmodels_expose_domain_data():
    graph = Graph("test/graph/test_0.csv")
    node_count = len(graph.distance)

    # Provide fixed positions to avoid randomness during the test.
    positions = [(i, i + 10) for i in range(node_count)]
    warehouse_vm = ViewModelWarehouse(graph, positions=positions)

    assert warehouse_vm.get_count() == node_count
    assert warehouse_vm.get_positions() == positions
    assert warehouse_vm.get_position(0) == positions[0]

    ants = [Ant(0, node_count), Ant(1, node_count)]
    ants[0].current_target_node_id = 2
    ants[1].current_target_node_id = 3
    ant_vm = ViewModelAnt(ants, warehouse_vm)

    assert ant_vm.get_count() == len(ants)
    assert ant_vm.get_positions() == [positions[0], positions[1]]
    assert ant_vm.get_target_coordinates() == [positions[2], positions[3]]

    edge_vm = ViewModelEdge(graph)
    pheromone_val = edge_vm.get_pheromone(0, 1)
    assert isinstance(pheromone_val, float)


