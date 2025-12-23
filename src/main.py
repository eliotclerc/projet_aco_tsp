import tkinter as tk
from tkinter import ttk
from view.Frame_app import Frame_app
from view.Main_frame import Main_frame
from view.viewWarehouse import viewWarehouse
from view.viawAnt import viewAnt
from view.viewEdge import viewEdge


def main():
    whs = [viewWarehouse(100, 100),viewWarehouse(700, 100),viewWarehouse(100, 500),viewWarehouse(700, 500)]
    edge_screen = []
    vA1 = viewAnt(100,100)
    vA2 = viewAnt(700,100)
    ants_list = [vA1,vA2]
    for i in whs : 
        for j in range(0, len(whs)):
            if (j <= whs.index(i)) : 
                continue 
            else : 
                edge_screen.append(viewEdge(i,whs[j]))


    app = Frame_app()
    frame = Main_frame(app,warehouses=whs,ants = ants_list,edges=edge_screen)
    frame.init_container_on_canva()
    frame.spawn_ants()
    frame.save_initial_state()
    

    
    app.mainloop()

main()