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
    a1 = Ant(0,node_count)
    a2 = Ant(1,node_count)

    #create warehouses
    vmw = ViewModelWarehouse(graph,radius=25)

    #creates edges between those warehouses
    vme = ViewModelEdge(graph)
    pheromone_val = vme.get_pheromone(0, 1)

    #creates ants
    ants = [Ant(0, node_count), Ant(1, node_count)]
    ants[0].current_target_node_id = 2
    ants[1].current_target_node_id = 3
    vma = ViewModelAnt(ants,warehouse_vm=vmw)

    #print(vma.get_positions())



    #create tkinter app & frame and lists 
    app = Frame_app()
    whs,ants_list,edge_screen,edge_id = lists_from_view_model_to_view(whs_vm= vmw.get_positions(),screen_geom= app.get_geom())
    frame = Main_frame(app,warehouses=whs,ants = ants_list,edges=edge_screen)


    #act upon windows and lists
    frame.init_container_on_canva()
    frame.spawn_ants()
    frame.save_initial_state()
 


    app.mainloop()

main()