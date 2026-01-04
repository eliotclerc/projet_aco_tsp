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

    # ACO parameters (will be used when ACO is created in Main_frame.start())
    alpha = 1.0
    beta = 2.0
    evaporation = 0.5

    # Create warehouses (positions are automatically loaded from TSP file)
    vmw = ViewModelWarehouse(graph)

    # Creates edges between those warehouses
    vme = ViewModelEdge(graph)

    # Create empty ants view model (will be populated when ACO is created in start())
    vma = ViewModelAnt(ants=[], warehouse_vm=vmw)


    # ACO step counter
    step_count = 0
    max_steps = 10
    last_step_time = time.time() - 3  # Allow immediate start

    # Create tkinter app & frame and lists
    app = Frame_app()
    whs, edge_screen = lists_from_view_model_to_view(whs_vm=vmw.get_positions(), vme=vme, screen_geom=app.get_geom())
    frame = Main_frame(app, warehouses=whs, ants=vma, edges=edge_screen, vme=vme, max_steps=max_steps, 
                       graph=graph, alpha=alpha, beta=beta, evaporation=evaporation)

    # Act upon windows and lists
    frame.init_container_on_canva()
    # Don't call spawn_ants() here - ants will be created when ACO is initialized in start()
    # frame.spawn_ants()  # Removed - no ants exist yet
    # frame.save_initial_state()  # Removed - will be called after ants are spawned

    # Set default number of ants in UI (e.g., 10)
    default_nb_ants = 10
    frame.ant.set(default_nb_ants)  # IntVar accepts integer directly
    frame.set()  # Update the internal nb_ants value

    # Set automated mode
    frame.automated = True
    frame.mode = "live"
    
    # Automatically start the ACO after a short delay (for automated mode)
    def auto_start():
        if frame.aco is None:  # Only start if ACO hasn't been created yet
            frame.start()
    app.after(100, auto_start)  # Start after 100ms to let UI initialize

    
    def run_aco_step():
        nonlocal step_count
        
        # Check if ACO has been created
        if frame.aco is None:
            return
            
        if step_count >= max_steps:
            print("ACO finished")
            frame.play = False  # Stop the animation loop
            return

        # Perform one ACO step without reset
        graph_local = frame.aco.graph
        for _ in range(frame.aco.graph_nb_node - 1):
            for ant in frame.aco.ants:
                ant.go_to(graph_local, frame.aco.alpha, frame.aco.beta)

        # pheromone deposit 
        for ant in frame.aco.ants:
            ant.pheromone_deposit(graph_local)

            # if shortest path found
            current_cycle = ant.current_cycle
            ant_cycle_length = current_cycle.compute_distance(graph_local.distance)
            if ant_cycle_length < frame.aco.shortest_cycle_len:
                frame.aco.shortest_cycle_len = ant_cycle_length
                frame.aco.shortest_cycle = current_cycle.cycle_node_ids.copy()

        # pheromone evaporation
        frame.aco.graph.pheromone.evaporate(frame.aco.evaporation)

        frame.aco.current_step += 1
        step_count += 1
        #print(f"ACO step {step_count} completed")

        # Get current cycles before reset
        current_cycles = [ant.current_cycle.cycle_node_ids.copy() for ant in frame.aco.ants]

        # Reset ants
        for ant in frame.aco.ants:
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
                    frame.move_ants(frame.view_ants[i], warehouse_id=warehouse_id, anim_id=current_anim, speed=20.0)


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