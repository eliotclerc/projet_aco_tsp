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



def main():
    
    #create graph
    graph = Graph("test/graph/test_0.csv")

    #create ants
    node_count = len(graph.distance)
    

    #create warehouses (positions are automatically loaded from TSP file)
    vmw = ViewModelWarehouse(graph)

    #creates edges between those warehouses
    vme = ViewModelEdge(graph)

    #creates ants
    ants = [Ant(0, node_count), Ant(1, node_count)]
    vma = ViewModelAnt(ants = ants,warehouse_vm=vmw)



    #create tkinter app & frame and lists 
    app = Frame_app()
    whs,edge_screen = lists_from_view_model_to_view(whs_vm= vmw.get_positions(),screen_geom= app.get_geom())
    frame = Main_frame(app,warehouses=whs,ants = vma,edges=edge_screen)


    #act upon windows and lists
    frame.init_container_on_canva()
    frame.spawn_ants()
    frame.save_initial_state()

    current_target = 1

    def check_start():
        nonlocal current_target

        if frame.play and not frame.animating:
            frame.play = False
            frame.animating = True
            frame.anim_id += 1
            current_anim = frame.anim_id

            frame.move_ants(frame.view_ants[0],warehouse_id=current_target,anim_id=current_anim)
            
            
        app.after(50, check_start)


    check_start()
 


    app.mainloop()

main()