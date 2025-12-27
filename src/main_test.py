import time
import tkinter as tk
from tkinter import ttk
from view.Frame_app import Frame_app
from view.Main_frame import Main_frame
from view.viewWarehouse import viewWarehouse
from view.viawAnt import viewAnt
from view.viewEdge import viewEdge
from view.view_main import lists_from_view_model_to_view
from viewModel.viewModelAnt import ViewModelAnt
from viewModel.viewModelWarehouse import ViewModelWarehouse
from viewModel.viewModelEdge import ViewModelEdge
from model.graph import Graph
from model.ant import Ant
from model.aco import AcoModel

def main():
    # Create graph
    graph = Graph("test/graph/test_0.csv")  # Using a small test file

    # Create ACO model
    nb_ants = 50
    alpha = 1.0
    beta = 2.0
    evaporation = 0.5
    aco = AcoModel(graph, nb_ants, alpha, beta, evaporation)

    # Create warehouses (positions are automatically loaded from TSP file)
    vmw = ViewModelWarehouse(graph)

    # Creates edges between those warehouses
    vme = ViewModelEdge(graph)

    # Creates ants view model
    vma = ViewModelAnt(ants=aco.ants, warehouse_vm=vmw)

    # Create tkinter app & frame and lists
    app = Frame_app()
    whs, edge_screen = lists_from_view_model_to_view(whs_vm=vmw.get_positions(), vme=vme, screen_geom=app.get_geom())
    frame = Main_frame(app, warehouses=whs, ants=vma, edges=edge_screen, vme=vme)

    # Act upon windows and lists
    frame.init_container_on_canva()
    frame.spawn_ants()
    frame.save_initial_state()

    # Set automated mode
    frame.automated = True
    frame.mode = "live"

    # ACO step counter
    step_count = 0
    max_steps = 100
    last_step_time = time.time() - 3  # Allow immediate start

    def run_aco_step():
        nonlocal step_count
        if step_count >= max_steps:
            print("ACO finished")
            frame.play = False  # Stop the animation loop
            return

        # Perform one ACO step without reset
        graph_local = aco.graph
        for _ in range(aco.graph_nb_node - 1):
            for ant in aco.ants:
                ant.go_to(graph_local, aco.alpha, aco.beta)

        # pheromone deposit 
        for ant in aco.ants:
            ant.pheromone_deposit(graph_local)

            # if shortest path found
            current_cycle = ant.current_cycle
            ant_cycle_length = current_cycle.compute_distance(graph_local.distance)
            if ant_cycle_length < aco.shortest_cycle_len:
                aco.shortest_cycle_len = ant_cycle_length
                aco.shortest_cycle = current_cycle.cycle_node_ids.copy()

        # pheromone evaporation
        aco.graph.pheromone.evaporate(aco.evaporation)

        aco.current_step += 1
        step_count += 1
        print(f"ACO step {step_count} completed")

        # Get current cycles before reset
        current_cycles = [ant.current_cycle.cycle_node_ids.copy() for ant in aco.ants]

        # Reset ants
        for ant in aco.ants:
            ant.reset_cycle()

        # Animate ants along their cycles
        frame.anim_id += 1
        current_anim = frame.anim_id
        frame.animating = True  # Set animating to prevent interruptions
        for i, cycle in enumerate(current_cycles):
            if len(cycle) > 1:
                # Move ant along its cycle
                for j in range(1, len(cycle)):
                    warehouse_id = cycle[j]
                    frame.move_ants(frame.view_ants[i], warehouse_id=warehouse_id, anim_id=current_anim, speed=5.0)

        # Next step will be triggered by check_start when animation finishes

    def check_start():
        nonlocal last_step_time
        if frame.play and not frame.animating and time.time() - last_step_time > 2:
            last_step_time = time.time()
            run_aco_step()
        app.after(50, check_start)

    # Start checking for start button
    check_start()

    app.mainloop()

if __name__ == "__main__":
    main()