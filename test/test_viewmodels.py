from src.model.graph import Graph
from src.model.ant import Ant
from src.viewModel.viewModelWarehouse import ViewModelWarehouse
from src.viewModel.viewModelAnt import ViewModelAnt
from src.viewModel.viewModelEdge import ViewModelEdge


def test_viewmodels():
    """Test simple que les ViewModels fonctionnent correctement."""
    csv_path = "test/graph/test_0.csv"
    graph = Graph(csv_path)
    node_count = len(graph.distance)

    warehouse_vm = ViewModelWarehouse(graph, csv_path)
    positions = warehouse_vm.get_positions()

    assert warehouse_vm.get_count() == node_count
    assert len(positions) == node_count
    assert warehouse_vm.get_position(0) == positions[0]
    
    for pos in positions:
        x, y = pos
        assert 0 <= x <= 1000
        assert 0 <= y <= 1000

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
    assert pheromone_val >= 0


